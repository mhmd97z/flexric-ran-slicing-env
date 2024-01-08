import json, time
from xapps.configs import rnti_imsi_path, metrics_path
from xapps.metrics import metrics

def get_imsi(rnti):
    try:
        f = open(rnti_imsi_path, 'r')
        rnti_imsi = json.load(f)
    except:
        print("rnti_imsi json file not found")
        print("skipping ...")
        return None

    cntr = 0
    while not rnti in rnti_imsi:
        time.sleep(0.2)
        try: 
            f = open(rnti_imsi_path, 'r')
            rnti_imsi = json.load(f)
        except:
            print("rnti_imsi json file not found")
            print("skipping ...")
            return None

        cntr += 1
        if cntr > 10:
            # raise "cannot find the corresponding imsi for rnti {}".format(rnti)
            return None 

    return rnti_imsi[rnti]

def get_rnti(imsi):
    try:
        f = open(rnti_imsi_path, 'r')
        rnti_imsi = json.load(f)
    except:
        print("rnti_imsi json file not found")
        print("skipping ...")
        return None

    rntis = [k for k, v in rnti_imsi.items() if v == imsi]

    if len(rntis) > 0:
        return rntis[-1]
    else:
        return None

def get_metrics(sm="mac"):
    try: 
        f = open(metrics_path[sm], 'r')
        data = json.load(f)
        rntis = list(data.keys())
    except:
        print("{} metrics json file not found".format(sm))
        print("skipping ...")
        return None
    
    returned_metrics = {}
    if len(rntis) > 0:
        for rnti in rntis:
            # get imsi
            imsi = get_imsi(rnti)
            if imsi is None:
                continue
            returned_metrics[imsi] = []

            # set the variables
            for metric in metrics[sm]:
                value = data[rnti][sm][metric]
                returned_metrics[imsi].append(value)

    return returned_metrics