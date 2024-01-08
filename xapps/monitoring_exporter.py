import sys
from os import path
# print("sys.path: ", sys.path)
# sys.path.append(path.dirname( path.dirname( path.abspath(__file__))))
# print("sys.path: ", sys.path)
import prometheus_client as prom
import json, time
from metrics_exporter import metrics as metrics
from xapps.utils import get_imsi
from xapps.configs import EXPORTER_PORT, EXPORTER_UPDATE_PERIOD, metrics_path
import logging
logging.basicConfig(level=logging.INFO)

# get rid of prom bloat
prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)

def push_metrics(sm="mac"):
    try:
        f = open(metrics_path[sm], 'r')
        data = json.load(f)
        rntis = list(data.keys())
    except:
        print("{} metrics json file not found".format(sm))
        print("skipping ...")
        return

    if len(rntis) > 0:
        for rnti in rntis:
            # get imsi
            imsi = get_imsi(rnti)
            # imsi = "10"
            # set the variables
            metrics_keys = list(metrics[sm].keys())
            for iter_, metric in enumerate(metrics[sm].values()):
                value = data[rnti][sm][metrics_keys[iter_]]
                metric.labels(imsi=imsi).set(value)
        logging.info("{} metrics are pushed".format(sm))

if __name__ == "__main__":
    prom.start_http_server(EXPORTER_PORT)
    logging.info("server is up")
    while True:
        logging.info("-- taking an exporter iteration")
        push_metrics("mac")
        push_metrics("rlc")
        push_metrics("pdcp")
        time.sleep(EXPORTER_UPDATE_PERIOD)
