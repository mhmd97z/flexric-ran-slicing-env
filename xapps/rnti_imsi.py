import time
import json
import threading
import logging
logging.basicConfig(level=logging.INFO) # DEBUG INFO

RNTI_TEID_PATH = "/home/mzi/tunnel_rnti.txt"
IMSI_TEID_PATH = "/home/mzi/imsi_teid.txt"

def dump_mapping():
    logging.debug("dump_mapping is invoked")
    global rnti_imsi_dict
    rnti_imsi_json = json.dumps(rnti_imsi_dict)
    with open("stats/rnti_imsi.json", "w") as outfile:
        outfile.write(rnti_imsi_json)
    
def build_rnti_imsi_mapping():
    logging.debug("build_rnti_imsi_mapping is invoked")
    global rnti_imsi_dict
    for rnti, teid in rnti_teid_dict.items():
        while not teid in teid_imsi_dict:
            time.sleep(0.5)
            print("teid_imsi_dict not up to date")
        rnti_imsi_dict[rnti] = teid_imsi_dict[teid]
    print('rnti_imsi_dict: ', rnti_imsi_dict)

####################
#### RNTI TO TEID 
####################
class RntiTeid(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.rnti_teid_path = RNTI_TEID_PATH

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

    
    def run(self):
        # iterate through the existing lines
        rnti_teid = open(self.rnti_teid_path, "r")
        for iter, line in enumerate(rnti_teid.readlines()):
            if len(line.split(" ")) == 3:
                self.update_rnti_teid_dict(line)
            else:
                pass
            last_line_count = iter+1    
        rnti_teid.close()

        # build the rnti_imsi mapping
        build_rnti_imsi_mapping()
        dump_mapping()

        # poll new lines and process them
        while True:
            rnti_teid = open(self.rnti_teid_path, "r")
            lines = rnti_teid.readlines()
            if len(lines) > last_line_count:
                for i in range(last_line_count, len(lines)):
                    last_line_count += 1
                    if len(lines[i].split(" ")) == 3:
                        self.update_rnti_teid_dict(lines[i])
                    else:
                        pass

                build_rnti_imsi_mapping()
                dump_mapping()

            rnti_teid.close()
            time.sleep(0.3)


####################
#### TEID TO IMSI
####################
class TeidImsi(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.teid_imsi_path = IMSI_TEID_PATH

    def update_teid_imsi_dict(self, line):
        line_items = line.split(" ")
        if line_items[0] == "imsi_teid":
            suffix = '\n'
            teid_imsi_dict[line_items[2][:-len(suffix)]] = line_items[1]
        else:
            raise "file corrupted"

    def run(self):
        # iterate through the existing lines
        teid_imsi = open(self.teid_imsi_path, "r")
        for iter, line in enumerate(teid_imsi.readlines()):
            if len(line.split(" ")) == 3:
                self.update_teid_imsi_dict(line)
            else:
                pass
            last_line_count = iter+1
        teid_imsi.close()

        # start processing the other file
        global wait
        wait = False

        # poll new lines and process them
        while True:
            teid_imsi = open(self.teid_imsi_path, "r")
            lines = teid_imsi.readlines()
            if len(lines) > last_line_count:
                for i in range(last_line_count, len(lines)):
                    last_line_count += 1
                    if len(lines[i].split(" ")) == 3:
                        self.update_teid_imsi_dict(lines[i])
                    else:
                        pass

            teid_imsi.close()
            time.sleep(0.1)

if __name__ == '__main__':
    # RNTI-IMSI
    global rnti_imsi_dict
    rnti_imsi_dict = dict()

    ## TEID-IMSI
    global teid_imsi_dict
    teid_imsi_dict = dict()

    teid_imsi_thread = TeidImsi()
    teid_imsi_thread.start()
    
    global wait
    wait = True

    while wait:
        time.sleep(0.1)

    ## RNTI-TEID
    global rnti_teid_dict
    rnti_teid_dict = dict()

    rnti_teid_thread = RntiTeid()
    rnti_teid_thread.start()
