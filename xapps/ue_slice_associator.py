import time, json, sys, logging, sys
from configs import imsi_slice_path, ASSOCIATOR_UPDATE_PERIOD
from utils import get_rnti, get_rnti_imsi_len, get_imsi_slice

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
    imsi_slice_mapping = get_imsi_slice()
    items = [(get_rnti(imsi), imsi, slice_id, hex(int(get_rnti(imsi)))) for imsi, slice_id in imsi_slice_mapping.items() if get_rnti(imsi) is not None]
    logging.debug("target association: {}".format(items))

    global curr_imsi_slice
    global curr_rnti_imsi_len
    curr_rnti_imsi_len = get_rnti_imsi_len()
    curr_imsi_slice = imsi_slice_mapping


    # generate the message
    if len(items) > 0:
        for item in items:
            msg = fill_slice_ctrl_msg([item])
            try:
                ric.control_slice_sm(conn[0].id, msg)
            except:
                logging.info("skipping association message!")
    else: 
        logging.info("no items to enforce")


def runner(conn):
    global curr_imsi_slice
    global curr_rnti_imsi_len

    new_imsi_slice = get_imsi_slice()
    new_rnti_imsi_len = get_rnti_imsi_len()

    if new_imsi_slice != curr_imsi_slice:
        logging.debug("\n\n\nnew imsi slice mapping is detected!")
        associator(conn)

    if new_rnti_imsi_len != curr_rnti_imsi_len:
        logging.debug("\n\n\nnew imsi-rnti!")
        associator(conn)


if __name__ == "__main__":
    ric.init()
    conn = ric.conn_e2_nodes()
    assert(len(conn) > 0)

    associator(conn)

    while True:
        try:
            runner(conn)
            time.sleep(ASSOCIATOR_UPDATE_PERIOD)
        except:
            # Avoid deadlock. ToDo revise architecture 
            while ric.try_stop == 0:
                time.sleep(1)
