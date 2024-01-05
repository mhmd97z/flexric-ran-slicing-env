import prometheus_client as prom
import json, time, sys
from metrics import metrics as metrics
import logging
EXPORTER_PORT = 9000
UPDATE_PERIOD = 3

metrics_path = {"mac": "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_stats_mac.json",
                "rlc": "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_stats_rlc.json",
                "pdcp": "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_stats_pdcp.json"}

rnti_imsi_path = "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/rnti_imsi.json"

# get rid of bloat
prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)

def get_imsi(rnti):
    try: 
        f = open(rnti_imsi_path, 'r')
        rnti_imsi = json.load(f)
    except:
        print("rnti_imsi json file not found")
        print("skipping ...")
        return 

    cntr = 0
    while not rnti in rnti_imsi:
        time.sleep(0.5)
        try: 
            f = open(rnti_imsi_path, 'r')
            rnti_imsi = json.load(f)
        except:
            print("rnti_imsi json file not found")
            print("skipping ...")
            return 
        cntr += 1
        if cntr > 40:
            # raise "cannot find the corresponding imsi for rnti {}".format(rnti)
            return None # 
    return rnti_imsi[rnti]


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

if __name__ == "__main__":
    prom.start_http_server(EXPORTER_PORT)
    while True:
        push_metrics("mac")
        push_metrics("rlc")
        push_metrics("pdcp")
        time.sleep(UPDATE_PERIOD)
