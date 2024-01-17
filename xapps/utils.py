import logging
import json, time, configparser
from configs import rnti_imsi_path, imsi_slice_path, slice_indication_path, slicing_scheme_path, srsran_config_path
from slice_ctrl_utils import fill_slice_scheme_ctrl_msg, fill_ue_slice_association_ctrl_msg
import xapp_sdk as ric
from threading import Lock

###################
## rnti-imsi
###################
def get_imsi(rnti, tolerant=False):
    rnti = str(rnti)
    try:
        f = open(rnti_imsi_path, 'r')
        rnti_imsi = json.load(f)
        f.close()
    except Exception as e:
        logging.exception(e)
        return None

    if not tolerant:
        cntr = 0
        while not rnti in rnti_imsi:
            time.sleep(0.2)
            try: 
                f = open(rnti_imsi_path, 'r')
                rnti_imsi = json.load(f)
                f.close()
            except Exception as e:
                logging.exception(e)
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


def get_rnti(imsi):
    try:
        f = open(rnti_imsi_path, 'r')
        rnti_imsi = json.load(f)
        f.close()
    except Exception as e:
        logging.exception(e)
        return None

    rntis = [k for k, v in rnti_imsi.items() if v == imsi]

    if len(rntis) > 0:
        return rntis[-1]
    else:
        return None


###################
# srsran config
###################
def get_prb_count():
    parser = configparser.RawConfigParser()
    parser.read(srsran_config_path+"/enb.conf")
    return int(parser.get("enb", "n_prb"))


###################
## Slicing 
###################
def get_imsi_slice():
    try: 
        f = open(imsi_slice_path, 'r')
        imsi_slice_mapping = json.load(f)
        f.close()
    except Exception as e:
        logging.exception(e)
        return {}
    
    return imsi_slice_mapping


def get_slicing_scheme():
    try:
        f = open(slicing_scheme_path, 'r')
        slicing_scheme = json.load(f)
        f.close()
    except Exception as e:
        logging.exception(e)
        return None

    return slicing_scheme


def get_ue_slice_indication():
    f = open(slice_indication_path, 'r')
    slice_indication_mapping = json.load(f)
    f.close()
    return slice_indication_mapping['UE']


def set_slice(decision=None, reset=False, conn=None):
    if conn is None:
        init_ric_wrapper()
        conn = ric.conn_e2_nodes()
        assert(len(conn) > 0)

    if reset:
        slicing_scheme = {"num_slices" : 0}
    else:
        slicing_scheme = get_slicing_scheme()
        if decision:
            base = 0
            for iter, (slice_id, prb) in enumerate(decision.items()):
                slicing_scheme["slices"][iter]["id"] = int(slice_id)
                slicing_scheme["slices"][iter]["slice_algo_params"]["pos_low"] = base
                slicing_scheme["slices"][iter]["slice_algo_params"]["pos_high"] = base + prb - 1
                base += prb - 1
            print("slicing scheme: ", slicing_scheme)

    msg = fill_slice_scheme_ctrl_msg(slicing_scheme)
    ric.control_slice_sm(conn[0].id, msg)

    

def ue_slice_associator(conn, item):
    node_idx = 0
    msg = fill_ue_slice_association_ctrl_msg(item)
    ric.control_slice_sm(conn[node_idx].id, msg)



class RicInitiator():
    initiated = False
    intitiation_lock = Lock()

    @staticmethod
    def init_ric_wrapper():
        with RicInitiator.intitiation_lock:
            if not RicInitiator.initiated:
                ric.init()
                RicInitiator.initiated = True

def init_ric_wrapper():
    RicInitiator.init_ric_wrapper()

