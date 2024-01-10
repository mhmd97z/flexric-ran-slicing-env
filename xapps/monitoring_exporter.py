import sys
from os import path
# print("sys.path: ", sys.path)
# sys.path.append(path.dirname( path.dirname( path.abspath(__file__))))
# print("sys.path: ", sys.path)
import prometheus_client as prom
import json, time
from metrics import metrics_exporter as metrics
from utils import get_imsi
from configs import EXPORTER_PORT, EXPORTER_UPDATE_PERIOD, metrics_path
import logging, threading
logging.basicConfig(level=logging.INFO)
import threading

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
            if imsi:
                # imsi = "10"
                # set the variables
                metrics_keys = list(metrics[sm].keys())
                for iter_, metric in enumerate(metrics[sm].values()):
                    value = data[rnti][sm][metrics_keys[iter_]]
                    metric.labels(imsi=imsi).set(value)
                print("{} metrics are pushed for imsi {}".format(sm, imsi))
            else:
                logging.info("no imsi was found for rnti {}".format(rnti))

    else:
        logging.info("no {} metrics found".format(sm))


if __name__ == "__main__":
    prom.start_http_server(EXPORTER_PORT)
    logging.info("server is up")
    logging.info("EXPORTER_UPDATE_PERIOD: ", EXPORTER_UPDATE_PERIOD)

    while True:
        logging.info("-- taking an exporter iteration")

        for sm in ["mac", "rlc", "pdcp"]:  
            push_metrics_thread = threading.Thread(target=push_metrics, args=(sm,), daemon=True)
            push_metrics_thread.start()
            
        time.sleep(EXPORTER_UPDATE_PERIOD)
