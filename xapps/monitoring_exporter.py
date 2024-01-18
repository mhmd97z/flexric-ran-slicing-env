import logging
import threading
import sys
import json
import time
import prometheus_client as prom
import sys
from metrics import metrics_exporter as metrics
from utils import get_imsi
from configs import EXPORTER_PORT, EXPORTER_UPDATE_PERIOD, metrics_path


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


# get rid of prom bloat
prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)


def push_metrics(sm: str):
    try:
        f = open(metrics_path[sm], 'r')
        data = json.load(f)
        f.close()
        rntis = list(data.keys())
    except Exception as e:
        logging.exception(e)
        return

    if len(rntis) == 0:
        logging.info("no {} metrics found".format(sm))
        return

    for rnti in rntis:
        imsi = get_imsi(rnti)
        if imsi:
            metrics_keys = list(metrics[sm].keys())
            for iter_, metric in enumerate(metrics[sm].values()):
                value = data[rnti][sm][metrics_keys[iter_]]
                metric.labels(imsi=imsi).set(value)
            logging.info("{} metrics are pushed for imsi {}".format(sm, imsi))


def export_metric_loop(sm: str):
    while True:
        logging.info(f"-- taking an exporter iteration for {sm}")
        try:
            push_metrics(sm)
        except Exception as e:
            logging.exception(e)
            sys.exit(1)

        time.sleep(EXPORTER_UPDATE_PERIOD)


def run_kpi_monitoring_exporter():
    prom.start_http_server(EXPORTER_PORT)
    threading.Thread(target=export_metric_loop, args=("mac", )).start()
    threading.Thread(target=export_metric_loop, args=("rlc", )).start()
    threading.Thread(target=export_metric_loop, args=("pdcp", )).start()


if __name__ == "__main__":
    run_kpi_monitoring_exporter()

