import time
import json
import threading
import logging
from configs import rnti_imsi_path, rnti_teid_path, imsi_teid_path, TEID_IMSI_UPDATE_PERIOD, RNTI_TEID_UPDATE_PERIOD
logging.basicConfig(level=logging.INFO) # DEBUG INFO


rnti_imsi_dict = {}
teid_imsi_dict = {}
rnti_teid_dict = {}

wait = True


def dump_mapping():
    logging.debug("dump_mapping is invoked")
    print('rnti_imsi_dict: ', rnti_imsi_dict)
    rnti_imsi_json = json.dumps(rnti_imsi_dict)
    with open(rnti_imsi_path, "w") as outfile:
        outfile.write(rnti_imsi_json)
    

def build_rnti_imsi_mapping():
    logging.debug("build_rnti_imsi_mapping is invoked")
    for rnti, teid in rnti_teid_dict.items():
        while not teid in teid_imsi_dict:
            time.sleep(TEID_IMSI_UPDATE_PERIOD * 3)
            print("teid_imsi_dict not up to date")
        rnti_imsi_dict[rnti] = teid_imsi_dict[teid]

    dump_mapping()


class RntiTeid(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def update_rnti_teid_dict(self, line):
        line_items = line.split(" ")
        
        if line_items[0] == "new_tunn":
            suffix = '\n' 
            rnti_teid_dict[line_items[2][:-len(suffix)]] = line_items[1]

        elif line_items[0] == "update_rnti":
            if line_items[1] in rnti_teid_dict:
                teid = rnti_teid_dict[line_items[1]]
                rnti_teid_dict.pop(line_items[1])
                suffix = '\n'
                rnti_teid_dict[line_items[2][:-len(suffix)]]= teid            

            else:
                print("rnti:{} was not found!".format(line_items[1]))
        
        elif line_items[0] == "remove_tunnel":
            pass
        
        else:
            logging.warning("skipping the line: {}".format(line))

    def read_file(self, file):
        updated = False
        while True:
            line = file.readline()
            if line is None or line == "":
                return updated
            if len(line.split(" ")) == 3:
                updated = True
                self.update_rnti_teid_dict(line)
    
    def run(self):
        # iterate through the existing lines
        rnti_teid = open(rnti_teid_path, "r")
        self.read_file(rnti_teid)

        # build the rnti_imsi mapping
        build_rnti_imsi_mapping()

        # poll new lines and process them
        while True:
            updated = self.read_file(rnti_teid)
            if updated:
                build_rnti_imsi_mapping()
            time.sleep(RNTI_TEID_UPDATE_PERIOD)


class TeidImsi(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def update_teid_imsi_dict(self, line):
        line_items = line.split(" ")
        if line_items[0] == "imsi_teid":
            suffix = '\n'
            teid_imsi_dict[line_items[2][:-len(suffix)]] = line_items[1]
        else:
            raise Exception("file corrupted")

    def read_all_remaining_lines(self, file):
        # iterate through the existing lines
        while True:
            line = file.readline()
            if line is None or line == "":
                return
            if len(line.split(" ")) == 3:
                self.update_teid_imsi_dict(line)

    def run(self):
        # iterate through the existing lines
        teid_imsi_file = open(imsi_teid_path, "r")
        self.read_all_remaining_lines(teid_imsi_file)

        # start processing the other file
        global wait
        wait = False

        # poll new lines and process them
        while True:
            self.read_all_remaining_lines(teid_imsi_file)
            time.sleep(TEID_IMSI_UPDATE_PERIOD)


if __name__ == '__main__':
    TeidImsi().start()

    while wait:
        time.sleep(0.1)

    RntiTeid().start()

