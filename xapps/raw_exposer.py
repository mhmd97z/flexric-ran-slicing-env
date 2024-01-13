import sys
import time
import json
import logging 
import argparse
from collections import defaultdict
from configs import metrics_path, slice_indication_path
from metrics import mac_kpi_list, rlc_kpi_list, pdcp_kpi_list
import xapp_sdk as ric

logging.basicConfig(level=logging.DEBUG)


class MACCallback(ric.mac_cb):
    def __init__(self):
        ric.mac_cb.__init__(self)

    def handle(self, ind):
        logging.debug("mac handler is invoked")

        if len(ind.ue_stats) > 0:
            logging.debug("mac handler found {} users".format(len(ind.ue_stats)))

            kpi_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
            for _, item in enumerate(ind.ue_stats):
                for kpi in mac_kpi_list: 
                    kpi_stats[item.rnti]["mac"][kpi] = eval('item.{}'.format(kpi))
        else:
            kpi_stats = {}

        stats_json = json.dumps(kpi_stats)
        with open(metrics_path["mac"], "w") as outfile:
            outfile.write(stats_json)
            


class RLCCallback(ric.rlc_cb):
    def __init__(self):
        ric.rlc_cb.__init__(self)
    def handle(self, ind):
        logging.debug("rlc handler is invoked")

        if len(ind.rb_stats) > 0:
            logging.debug("rlc handler found {} users".format(len(ind.rb_stats)))

            kpi_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
            for _, item in enumerate(ind.rb_stats):
                for kpi in rlc_kpi_list: 
                    kpi_stats[item.rnti]["rlc"][kpi] = eval('item.{}'.format(kpi))
        else:
            kpi_stats = {}
            
        stats_json = json.dumps(kpi_stats)
        with open(metrics_path["rlc"], "w") as outfile:
            outfile.write(stats_json)



class PDCPCallback(ric.pdcp_cb):
    def __init__(self):
        ric.pdcp_cb.__init__(self)

    def handle(self, ind):
        logging.debug("pdcp handler is invoked")

        if len(ind.rb_stats) > 0:
            logging.debug("pdcp handler found {} users".format(len(ind.rb_stats)))

            kpi_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
            for _, item in enumerate(ind.rb_stats):
                for kpi in pdcp_kpi_list: 
                    kpi_stats[item.rnti]["pdcp"][kpi] = eval('item.{}'.format(kpi))
        else:
            kpi_stats = {}
        
        stats_json = json.dumps(kpi_stats)
        with open(metrics_path["pdcp"], "w") as outfile:
            outfile.write(stats_json)




class SLICECallback(ric.slice_cb):

    def __init__(self):
        ric.slice_cb.__init__(self)

    def handle(self, ind):
        logging.debug("slice handler is invoked")
        self.slice_ind_to_dict_json(ind)

    @staticmethod
    def slice_ind_to_dict_json(ind):
        slice_stats = {
            "RAN" : {
                "dl" : {}
                # TODO: handle the ul slice stats, currently there is no ul slice stats in database(SLICE table)
                # "ul" : {}
            },
            "UE" : {}
        }

        # RAN - dl
        dl_dict = slice_stats["RAN"]["dl"]
        if ind.slice_stats.dl.len_slices <= 0:
            dl_dict["num_of_slices"] = ind.slice_stats.dl.len_slices
            dl_dict["slice_sched_algo"] = "null"
            dl_dict["ue_sched_algo"] = ind.slice_stats.dl.sched_name[0]
        else:
            if ind.slice_stats.dl.len_slices > 0:
                logging.debug("slice handler found {} slices".format(ind.slice_stats.dl.len_slices))
            
            dl_dict["num_of_slices"] = ind.slice_stats.dl.len_slices
            dl_dict["slice_sched_algo"] = "null"
            dl_dict["slices"] = []
            slice_algo = ""
            for s in ind.slice_stats.dl.slices:
                if s.params.type == 1: # TODO: convert from int to string, ex: type = 1 -> STATIC
                    slice_algo = "STATIC"
                elif s.params.type == 2:
                    slice_algo = "NVS"
                elif s.params.type == 4:
                    slice_algo = "EDF"
                else:
                    slice_algo = "unknown"
                dl_dict.update({"slice_sched_algo" : slice_algo})

                slices_dict = {
                    "index" : s.id,
                    "label" : s.label[0],
                    "ue_sched_algo" : s.sched[0],
                }
                if dl_dict["slice_sched_algo"] == "STATIC":
                    slices_dict["slice_algo_params"] = {
                        "pos_low" : s.params.u.sta.pos_low,
                        "pos_high" : s.params.u.sta.pos_high
                    }
                elif dl_dict["slice_sched_algo"] == "NVS":
                    if s.params.u.nvs.conf == 0: # TODO: convert from int to string, ex: conf = 0 -> RATE
                        slices_dict["slice_algo_params"] = {
                            "type" : "RATE",
                            "mbps_rsvd" : s.params.u.nvs.u.rate.u1.mbps_required,
                            "mbps_ref" : s.params.u.nvs.u.rate.u2.mbps_reference
                        }
                    elif s.params.u.nvs.conf == 1: # TODO: convert from int to string, ex: conf = 1 -> CAPACITY
                        slices_dict["slice_algo_params"] = {
                            "type" : "CAPACITY",
                            "pct_rsvd" : s.params.u.nvs.u.capacity.u.pct_reserved
                        }
                    else:
                        slices_dict["slice_algo_params"] = {"type" : "unknown"}
                elif dl_dict["slice_sched_algo"] == "EDF":
                    slices_dict["slice_algo_params"] = {
                        "deadline" : s.params.u.edf.deadline,
                        "guaranteed_prbs" : s.params.u.edf.guaranteed_prbs,
                        "max_replenish" : s.params.u.edf.max_replenish
                    }
                else:
                    print("unknown slice algorithm, cannot handle params")
                dl_dict["slices"].append(slices_dict)

        # RAN - ul
        # TODO: handle the ul slice stats, currently there is no ul slice stats in database(SLICE table)
        # flexric only supports downlink slicing


        # UE
        # global assoc_rnti
        ue_dict = slice_stats["UE"]
        if ind.ue_slice_stats.len_ue_slice <= 0:
            ue_dict["num_of_ues"] = ind.ue_slice_stats.len_ue_slice
        else:
            ue_dict["num_of_ues"] = ind.ue_slice_stats.len_ue_slice
            ue_dict["ues"] = []
            for u in ind.ue_slice_stats.ues:
                ues_dict = {}
                dl_id = "null"
                if u.dl_id >= 0 and dl_dict["num_of_slices"] > 0:
                    dl_id = u.dl_id
                ues_dict = {
                    "rnti" : u.rnti,
                    "assoc_dl_slice_id" : dl_id
                    # TODO: handle the associated ul slice id, currently there is no ul slice id in database(UE_SLICE table)
                }
                ue_dict["ues"].append(ues_dict)

        ind_json = json.dumps(slice_stats)

        with open(slice_indication_path, "w") as outfile:
            outfile.write(ind_json)



def run_exposer(args):
    if not (args.all or args.kpi or args.slice):
        print("Are you serious?!")
        sys.exit(1)

    mac_hndlr = []
    rlc_hndlr = []
    pdcp_hndlr = []
    slice_hndlr = []

    ric.init()
    conn = ric.conn_e2_nodes()
    assert(len(conn) > 0)
    for i in range(0, len(conn)):
        logging.info("Global E2 Node [" + str(i) + "]: PLMN MCC = " + str(conn[i].id.plmn.mcc))
        logging.info("Global E2 Node [" + str(i) + "]: PLMN MNC = " + str(conn[i].id.plmn.mnc))

    if args.all or args.kpi:
        for i in range(0, len(conn)):
            mac_cb = MACCallback()
            hndlr = ric.report_mac_sm(conn[i].id, ric.Interval_ms_10, mac_cb)
            mac_hndlr.append(hndlr)     
            time.sleep(1) # just to be safe!

        logging.info('MAC handler is initialized')


    if args.all or args.kpi:
        for i in range(0, len(conn)):
            rlc_cb = RLCCallback()
            hndlr = ric.report_rlc_sm(conn[i].id, ric.Interval_ms_10, rlc_cb)
            rlc_hndlr.append(hndlr) 
            time.sleep(1)   # just to be safe!

        logging.info('RLC handler is initialized')

    
    if args.all or args.kpi:
        for i in range(0, len(conn)):
            pdcp_cb = PDCPCallback()
            hndlr = ric.report_pdcp_sm(conn[i].id, ric.Interval_ms_10, pdcp_cb)
            pdcp_hndlr.append(hndlr) 
            time.sleep(1) # just to be safe!

        logging.info('PDCP handler is initialized')


    if args.all or args.slice:
        for i in range(0, len(conn)):
            slice_cb = SLICECallback()
            hndlr = ric.report_slice_sm(conn[i].id, ric.Interval_ms_10, slice_cb)
            slice_hndlr.append(hndlr) 
            time.sleep(1) # just to be safe!

        logging.info('SLICE handler is initialized')


    try:
        while True:
            time.sleep(1)

    except:
        logging.info('stopping service models')

        # remove service models
        for hndlr in mac_hndlr:
            ric.rm_report_mac_sm(hndlr)

        for hndlr in rlc_hndlr:
            ric.rm_report_rlc_sm(hndlr)

        for hndlr in pdcp_hndlr:
            ric.rm_report_pdcp_sm(hndlr)

        for hndlr in slice_hndlr:
            ric.rm_report_slice_sm(hndlr)

        # Avoid deadlock. ToDo revise architecture 
        while ric.try_stop == 0:
            time.sleep(1)

        logging.info('exiting the program')


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", 
                    help="run all service models")
    parser.add_argument("--kpi", action="store_true", 
                    help="run mac pdcp rlc service models")
    parser.add_argument("--slice", action="store_true", 
                    help="run slice service model")
    args = parser.parse_args() 
    return args


if __name__ == "__main__":
    args = build_parser()
    run_exposer(args)

