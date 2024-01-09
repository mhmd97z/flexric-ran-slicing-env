import prometheus_client as prom
import requests
import pandas as pd
import json, logging, time
from configs import PROMETHEUS_URL, SLICE_EXPORTER_PORT, EXPORTER_UPDATE_PERIOD, slice_stats_path
from metrics import slice_throughput
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
    r = requests.get(url=PROMETHEUS_URL + '/api/v1/query', params=PROM_PARAMS)
    data = r.json()

    if data['status'] == 'success':
        data_list = []
        for item in data['data']['result']:
            data_list.append((item['metric']['imsi'], float(item['value'][0]), float(item['value'][1])))

        return pd.DataFrame(data_list, columns=['imsi', 'timestamp', 'throughput'])
        
    else:
        return None


def get_imsi_slice_df():
    get_imsi_slice_mapping = get_imsi_slice()
    return pd.DataFrame(get_imsi_slice_mapping.items(), columns=['imsi', 'slice_id'])

def exporter(df):
    
    for _, row in df.iterrows():
        slice_throughput.labels(slice_id= int(row['slice_id'])).set(float(row['slice_throughput']))

def run_kpi_computation():
    kpi_df = send_query()
    imsi_slice_df = get_imsi_slice_df()

    if kpi_df is not None and imsi_slice_df is not None:
        df = pd.merge(kpi_df, imsi_slice_df, on='imsi')
        agg_df = df.groupby('slice_id').agg( \
            slice_throughput= ('throughput', 'mean'),
            active_user_count= ('throughput', 'count')
        ).reset_index()

        agg_df.to_csv(slice_stats_path, encoding='utf-8')

        exporter(agg_df)

if __name__ == "__main__":
    prom.start_http_server(SLICE_EXPORTER_PORT)
    logging.info("server is up")
    logging.info("EXPORTER_UPDATE_PERIOD: {}".format(EXPORTER_UPDATE_PERIOD))
    
    while True:
        logging.info("-- taking an exporter iteration")
        run_kpi_computation()
            
        time.sleep(EXPORTER_UPDATE_PERIOD)