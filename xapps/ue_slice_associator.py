import time
import sys
import logging
import sys
from configs import ASSOCIATOR_UPDATE_PERIOD
from utils import get_imsi, get_imsi_slice, get_ue_slice_indication, ue_slice_associator
import xapp_sdk as ric



logging.basicConfig(level=logging.INFO)


def runner(ric, conn):
    logging.info("rnti-slice mapping investigation")
    ue_slice_indication = get_ue_slice_indication()
    target_imsi_slice = get_imsi_slice()

    for ue_item in ue_slice_indication['ues']:
        imsi = get_imsi(ue_item['rnti'], tolerant=False)
        if imsi != None:
            try:
                curr_slice_id = int(ue_item['assoc_dl_slice_id'])
            except:
                curr_slice_id = None

            if curr_slice_id != int(target_imsi_slice[str(imsi)]):
                item = [(str(ue_item['rnti']), imsi, target_imsi_slice[str(imsi)], hex(int(ue_item['rnti'])))]
                logging.info("\n\nissuing a new mapping command: {}".format(item))
                ue_slice_associator(ric, conn, item)
                logging.info("\n")


if __name__ == "__main__":
    ric.init()
    conn = ric.conn_e2_nodes()
    assert(len(conn) > 0)

    while True:
        try:
            runner(ric, conn)
            time.sleep(ASSOCIATOR_UPDATE_PERIOD)
        except Exception as e:
            logging.exception(e)
            sys.exit()

