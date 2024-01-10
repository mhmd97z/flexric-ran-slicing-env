import prometheus_client as prom
import requests
import pandas as pd
import json, logging, time
from configs import PROMETHEUS_URL, SLICE_EXPORTER_PORT, EXPORTER_UPDATE_PERIOD, slice_stats_path
from metrics import metrics_exporter, metrics_exporter_slice_mapping
from utils import get_imsi_slice

logging.basicConfig(level=logging.INFO)

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

PROM_PARAMS = {'query': 'rate(dl_aggr_tbs[1m])'}  # per-second derivative of range vector

# get rid of bloat
prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)


def send_query():
    data_list = {}
    kpis_label = list(metrics_exporter['slice'].keys())
    kpis_label.remove("slice_active_users")
    for metric in kpis_label:
        r = requests.get(url=PROMETHEUS_URL + '/api/v1/query', params={'query': metric})
        data = r.json()
        if data['status'] == 'success':
            for item in data['data']['result']:
                if not item['metric']['imsi'] in data_list:
                    data_list[item['metric']['imsi']] = []
                data_list[item['metric']['imsi']].append(float(item['value'][1]))

    data = []
    for imsi, kpis in data_list.items():
        data.append([imsi] + kpis)

    if len(data) > 0:
        return pd.DataFrame(data, columns=['imsi'] + kpis_label)

    else:
        return None


def get_imsi_slice_df():
    get_imsi_slice_mapping = get_imsi_slice()
    return pd.DataFrame(get_imsi_slice_mapping.items(), columns=['imsi', 'slice_id'])

def exporter(df):
    metrics_labels = list(df.columns)
    metrics_labels.remove('slice_id')
    for _, row in df.iterrows():
        for metric_label in metrics_labels: 
            metrics_exporter['slice'][metrics_exporter_slice_mapping[metric_label]]\
                .labels(slice_id= int(row['slice_id'])).set(float(row[metric_label]))

def run_kpi_computation():
    kpi_df = send_query()
    imsi_slice_df = get_imsi_slice_df()

    if kpi_df is not None and imsi_slice_df is not None:
        df = pd.merge(kpi_df, imsi_slice_df, on='imsi')
        agg_df = df.groupby('slice_id').agg( \
            slice_dl_throughput= ('rate(ul_aggr_tbs[10s])', 'mean'),
            slice_ul_throughput= ('rate(dl_aggr_tbs[10s])', 'mean'),
            slice_phr= ('phr', 'mean'),
            slice_cqi= ('wb_cqi', 'mean'),
            slice_active_users= ('wb_cqi', 'count')
        ).reset_index()
        
        print(agg_df)

        print(slice_stats_path)
        agg_df.to_csv(slice_stats_path, index=False, encoding='utf-8')

        exporter(agg_df)

if __name__ == "__main__":
    prom.start_http_server(SLICE_EXPORTER_PORT)
    logging.info("server is up")
    logging.info("EXPORTER_UPDATE_PERIOD: {}".format(EXPORTER_UPDATE_PERIOD))
    
    while True:
        logging.info("-- taking an exporter iteration")
        run_kpi_computation()
            
        time.sleep(EXPORTER_UPDATE_PERIOD)