import json, time
slice_indication_path = "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_indication_slice.json"
from configs import rnti_imsi_path, imsi_slice_path, slice_indication_path

def get_imsi(rnti, tolerant=True):
    rnti = str(rnti)
    try:
        f = open(rnti_imsi_path, 'r')
        rnti_imsi = json.load(f)
    except:
        print("rnti_imsi json file not found")
        print("skipping ...")
        return None

    if tolerant:
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
    else:
        if rnti in rnti_imsi:
            return rnti_imsi[rnti]
        else:
            return None

def get_rnti_imsi_len():
    try:
        f = open(rnti_imsi_path, 'r')
        rnti_imsi = json.load(f)
    except:
        print("rnti_imsi json file not found")
        print("skipping ...")
        return 0
    
    return len(rnti_imsi)


def get_imsi_slice():
    try: 
        f = open(imsi_slice_path, 'r')
        imsi_slice_mapping = json.load(f)
    except:
        print("rnti_imsi json file not found")
        print("skipping ...")
        return {}
    
    return imsi_slice_mapping


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

def get_ue_slice_indication():
    try:
        f = open(slice_indication_path, 'r')
        slice_indication_mapping = json.load(f)
    except:
        print("rnti_imsi json file not found")
        print("skipping ...")
        return None
    
    return slice_indication_mapping['UE']