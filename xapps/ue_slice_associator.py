import time, threading, json
import xapp_sdk as ric
import sys, logging
logging.getLogger().setLevel(logging.DEBUG)

rnti_imsi_path = "/home/mzi/ran_slicing_flexric/flexric/build/examples/xApp/python3/stats/rnti_imsi.json"
imsi_slice_path ="/home/mzi/ran_slicing_flexric/flexric/build/examples/xApp/python3/imsi_slice_mapping_dict.json"

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


def fill_slice_ctrl_msg(items):
    msg = ric.slice_ctrl_msg_t()
    msg.type = ric.SLICE_CTRL_SM_V0_UE_SLICE_ASSOC
    msg.u.ue_slice.len_ue_slice = len(items)
    assoc = ric.ue_slice_assoc_array(len(items))
    for i in range(len(items)):
        a = ric.ue_slice_assoc_t()
        a.rnti = int(items[i][0])
        a.dl_id = int(items[i][2])
        assoc[i] = a

    msg.u.ue_slice.ues = assoc
    return msg

def associator(conn):
    try: 
        f = open(imsi_slice_path, 'r')
        imsi_slice_mapping = json.load(f)
    except:
        print("rnti_imsi json file not found")
        print("skipping ...")
        sys.exit(1)

    items = [(get_rnti(imsi), imsi, slice_id) for imsi, slice_id in imsi_slice_mapping.items() if get_rnti(imsi) is not None]
    logging.debug("in associator: items: {}".format(items))

    # generate the message
    if len(items) > 0:        
        msg = fill_slice_ctrl_msg(items)
        try:
            ric.control_slice_sm(conn[0].id, msg)
        except:
            logging.info("skipping association!")
    else: 
        logging.info("no items to enforce")
        
    
if __name__ == "__main__":
    ric.init()
    conn = ric.conn_e2_nodes()
    assert(len(conn) > 0)

    while True:
        try:
            associator(conn)
            time.sleep(0.5)
        except:
            sys.exit(1)