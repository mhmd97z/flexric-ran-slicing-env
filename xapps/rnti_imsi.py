import time
import json
import threading
import logging
from configs import rnti_imsi_path, rnti_teid_path, imsi_teid_path, TEID_IMSI_UPDATE_PERIOD, RNTI_TEID_UPDATE_PERIOD
logging.basicConfig(level=logging.INFO)


rnti_imsi = {}
teid_imsi = {}
rnti_teid = {}

wait = True


def dump_mapping():
    logging.debug("dump_mapping is invoked")
    print('rnti_imsi_dict: ', rnti_imsi)
    rnti_imsi_json = json.dumps(rnti_imsi)
    with open(rnti_imsi_path, "w") as outfile:
        outfile.write(rnti_imsi_json)
    

def build_rnti_imsi_mapping():
    logging.debug("build_rnti_imsi_mapping is invoked")
    global rnti_imsi
    rnti_imsi = {}
    for rnti, teid in rnti_teid.items():
        while not teid in teid_imsi:
            time.sleep(TEID_IMSI_UPDATE_PERIOD * 3)
            print(f"teid_imsi_dict not up to date for {teid}")
        rnti_imsi[rnti] = teid_imsi[teid]
    dump_mapping()


class RntiTeid(threading.Thread):
    NEW_TUNN = "new_tunn"
    UPDATE_RNTI = "update_rnti"
    REMOVE_TUNNEL = "remove_tunnel"
    REMOVE_RNTI = "remove_rnti"

    def __init__(self):
        threading.Thread.__init__(self)
        self.commands = [
            RntiTeid.NEW_TUNN, 
            RntiTeid.UPDATE_RNTI, 
            RntiTeid.REMOVE_TUNNEL, 
            RntiTeid.REMOVE_RNTI,
        ]

    def update_rnti_teid_dict(self, line):
        line_items = line.split(" ")
        command = line_items[0]
        if command == RntiTeid.NEW_TUNN:
            rnti = line_items[2].strip()
            teid = line_items[1]
            rnti_teid[rnti] = teid

        elif command == RntiTeid.UPDATE_RNTI:
            old_rnti = line_items[1]
            if old_rnti in rnti_teid:
                teid = rnti_teid[old_rnti]
                rnti_teid.pop(old_rnti)
                new_rnti = line_items[2].strip()
                rnti_teid[new_rnti]= teid            
            else:
                logging.info("rnti:{} was not found!".format(old_rnti))

        elif command == RntiTeid.REMOVE_TUNNEL:
            rnti = line_items[1].strip()
            teid = line_items[2].strip()
            rnti_teid.pop(rnti)
        elif command == RntiTeid.REMOVE_RNTI:
            pass
        else:
            logging.warning("skipping the line: {}".format(line))

    def read_remaining_lines(self, file):
        updated = False
        while True:
            line = file.readline()
            if line is None or line == "":
                return updated

            valid_command = False
            for command in self.commands:
                if line.startswith(command):
                    valid_command = True
                    break

            if valid_command:
                updated = True
                self.update_rnti_teid_dict(line)
    
    def run(self):
        # iterate through the existing lines
        rnti_teid = open(rnti_teid_path, "r")
        self.read_remaining_lines(rnti_teid)

        # build the rnti_imsi mapping
        build_rnti_imsi_mapping()

        # poll new lines and process them
        while True:
            updated = self.read_remaining_lines(rnti_teid)
            if updated:
                build_rnti_imsi_mapping()
            time.sleep(RNTI_TEID_UPDATE_PERIOD)


class TeidImsi(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def update_teid_imsi_dict(self, line):
        line_items = line.split(" ")
        if line_items[0] == "imsi_teid":
            teid = line_items[2].strip()
            imsi = line_items[1].strip()
            teid_imsi[teid] = imsi
        else:
            raise Exception("file corrupted")

    def read_remaining_lines(self, file):
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
        self.read_remaining_lines(teid_imsi_file)

        # start processing the other file
        global wait
        wait = False

        # poll new lines and process them
        while True:
            self.read_remaining_lines(teid_imsi_file)
            time.sleep(TEID_IMSI_UPDATE_PERIOD)


if __name__ == '__main__':
    TeidImsi().start()

    while wait:
        time.sleep(0.1)

    RntiTeid().start()

