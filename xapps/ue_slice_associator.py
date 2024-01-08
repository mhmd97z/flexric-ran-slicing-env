import time, json, sys, logging, sys
from configs import imsi_slice_path, ASSOCIATOR_UPDATE_PERIOD
from utils import get_rnti 
import xapp_sdk as ric

logging.getLogger().setLevel(logging.DEBUG)

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
    logging.debug("target association: {}".format(items))

    # generate the message
    if len(items) > 0:        
        msg = fill_slice_ctrl_msg(items)
        try:
            ric.control_slice_sm(conn[0].id, msg)
        except:
            logging.info("skipping association message!")
    else: 
        logging.info("no items to enforce")


if __name__ == "__main__":
    ric.init()
    conn = ric.conn_e2_nodes()
    assert(len(conn) > 0)

    while True:
        try:
            associator(conn)
            time.sleep(ASSOCIATOR_UPDATE_PERIOD)
        except:
            # Avoid deadlock. ToDo revise architecture 
            while ric.try_stop == 0:
                time.sleep(1)

            sys.exit(1)