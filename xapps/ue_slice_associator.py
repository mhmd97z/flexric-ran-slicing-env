import time
import os
import sys
import logging
import threading
import sys
from configs import ASSOCIATOR_UPDATE_PERIOD
from utils import get_imsi, get_imsi_slice, get_ue_slice_indication, ue_slice_associator, init_ric_wrapper
import xapp_sdk as ric



logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def runner():
    logging.info("rnti-slice mapping investigation")
    ue_slice_indication = get_ue_slice_indication()
    target_imsi_slice = get_imsi_slice()

    conn = ric.conn_e2_nodes()
    for ue_item in ue_slice_indication['ues']:
        imsi = get_imsi(ue_item['rnti'], tolerant=False)
        if imsi is None:
            continue
        try:
            curr_slice_id = int(ue_item['assoc_dl_slice_id'])
        except:
            curr_slice_id = None

        if curr_slice_id != int(target_imsi_slice[str(imsi)]):
            item = [(str(ue_item['rnti']), imsi, target_imsi_slice[str(imsi)], hex(int(ue_item['rnti'])))]
            logging.info("\n\nissuing a new mapping command: {}".format(item))
            ue_slice_associator(conn, item)
            logging.info("\n")


def ue_slice_associator_loop():
    init_ric_wrapper()
    while True:
        try:
            runner()
        except Exception as e:
            logging.exception(e)
        time.sleep(ASSOCIATOR_UPDATE_PERIOD)


def run_ue_slice_associator():
    threading.Thread(target=ue_slice_associator_loop).start()

if __name__ == "__main__":
    run_ue_slice_associator()
