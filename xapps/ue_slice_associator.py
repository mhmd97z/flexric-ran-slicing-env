import time, json, sys, logging, sys
from configs import slice_indication_path, ASSOCIATOR_UPDATE_PERIOD
from utils import get_rnti, get_imsi, get_rnti_imsi_len, get_imsi_slice, get_ue_slice_indication

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


def associator(conn, item):
    # generate the message
    msg = fill_slice_ctrl_msg(item)
    try:
        ric.control_slice_sm(conn[0].id, msg)
    except:
        logging.info("skipping association message!")


# def runner(conn):
#     global curr_imsi_slice
#     global curr_rnti_imsi_len

#     new_imsi_slice = get_imsi_slice()
#     new_rnti_imsi_len = get_rnti_imsi_len()

#     if new_imsi_slice != curr_imsi_slice:
#         logging.debug("\n\n\nnew imsi slice mapping is detected!")
#         associator(conn)

#     if new_rnti_imsi_len != curr_rnti_imsi_len:
#         logging.debug("\n\n\nnew imsi-rnti!")
#         associator(conn)

def runner(conn):
    logging.info("rnti-slice mapping investigation")
    ue_slice_indication = get_ue_slice_indication()
    taget_imsi_slice = get_imsi_slice()

    for ue_item in ue_slice_indication['ues']:
        imsi = get_imsi(ue_item['rnti'], tolerant=False)
        # print(ue_item['rnti'], ue_item['assoc_dl_slice_id'], get_imsi(ue_item['rnti'], tolerant=False))
        if imsi != None:
            if int(ue_item['assoc_dl_slice_id']) != int(taget_imsi_slice[str(imsi)]):
                item = [(str(ue_item['rnti']), imsi, taget_imsi_slice[str(imsi)], hex(int(ue_item['rnti'])))]
                logging.info("\n\nissuing a new mapping command: {}".format(item))
                associator(conn, item)
                logging.info("\n")
if __name__ == "__main__":
    ric.init()
    conn = ric.conn_e2_nodes()
    assert(len(conn) > 0)

    while True:
        try:
            runner(conn)
            time.sleep(ASSOCIATOR_UPDATE_PERIOD)
        except:
            # Avoid deadlock. ToDo revise architecture 
            while ric.try_stop == 0:
                time.sleep(1)
