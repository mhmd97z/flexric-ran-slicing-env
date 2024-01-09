import prometheus_client as prom
import requests
import pandas as pd
import json, logging, time
from configs import PROMETHEUS_URL

logging.basicConfig(level=logging.INFO)

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

PROM_PARAMS = {'query': 'rate(dl_aggr_tbs[1m])'}  # per-second derivative of range vector

# get rid of bloat
prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)

def send_queries():
    r = requests.get(url=PROMETHEUS_URL + '/api/v1/query', params=PROM_PARAMS)
    data = r.json()
    print(data)

def run_kpi_computation():
    df = send_queries()
    if df is None:
        console_logger.warning("No data available!")
        return
    groups = get_per_session_throughput_groups(df)
    export_to_prometheus(groups)
    console_logger.info("Exporter is running ...")




if __name__ == "__main__":
    send_queries()
    
    