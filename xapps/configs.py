import configparser

def get_rnti_teid_path():
    parser = configparser.RawConfigParser()
    parser.read(srsran_config_path+"/enb.conf")
    return str(parser.get("log", "rnti_teid_path"))

def get_imsi_teid_path():
    parser = configparser.RawConfigParser()
    parser.read(srsran_config_path+"/epc.conf")
    return str(parser.get("log", "imsi_teid_path"))


# prometheus exporter
EXPORTER_PORT = 9000
SLICE_EXPORTER_PORT = 10001
EXPORTER_UPDATE_PERIOD = 1
PROMETHEUS_URL = "http://129.97.168.51:30090"


# ue-slice association
ASSOCIATOR_UPDATE_PERIOD = 0.5


# RNTI-IMSI Mapping
TEID_IMSI_UPDATE_PERIOD = 0.1
RNTI_TEID_UPDATE_PERIOD = 0.3


# srsran
srsran_config_path = "/root/.config/srsran"
rnti_teid_path = get_rnti_teid_path()   # /tmp/tunnel_rnti.txt
imsi_teid_path = get_imsi_teid_path()   # /tmp/imsi_teid.txt

BASE = "/home/amirmo/ran-slicing-flexric-gym/"

# metrics
metrics_path = {"mac": BASE + "xapps/stats/exporter_stats_mac.json",
                "rlc": BASE + "xapps/stats/exporter_stats_rlc.json",
                "pdcp": BASE + "xapps/stats/exporter_stats_pdcp.json"}

# slicing config
imsi_slice_path = BASE + "xapps/imsi_slice_mapping_dict.json"
slicing_scheme_path = BASE + "xapps/slicing_scheme.json"


# slicing indication
slice_indication_path = BASE + "/xapps/stats/exporter_indication_slice.json"
slice_stats_path = BASE + "/xapps/stats/exporter_stats_slice.csv"


# rnti-imsi
rnti_imsi_path = BASE + "/xapps/rnti_imsi.json"

# phones
phones_json_path = "/tmp/phones.json"
