import logging
import threading
import json, time
import prometheus_client as prom
from metrics import metrics_exporter as metrics
from utils import get_imsi
from configs import EXPORTER_PORT, EXPORTER_UPDATE_PERIOD, metrics_path


logging.basicConfig(level=logging.INFO)


# get rid of prom bloat
prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)


def push_metrics(sm: str):
    try:
        f = open(metrics_path[sm], 'r')
        data = json.load(f)
        rntis = list(data.keys())
    except:
        logging.info("{} metrics json file not found".format(sm))
        logging.info("skipping ...")
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
        else:
            logging.info("no imsi was found for rnti {}".format(rnti))


if __name__ == "__main__":
    prom.start_http_server(EXPORTER_PORT)
    logging.info("server is up")
    logging.info("EXPORTER_UPDATE_PERIOD: ".format(EXPORTER_UPDATE_PERIOD))

    while True:
        logging.info("-- taking an exporter iteration")

        threads = []
        for sm in ["mac", "rlc", "pdcp"]:  
            t = threading.Thread(target=push_metrics, args=(sm,))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

            
        time.sleep(EXPORTER_UPDATE_PERIOD)

