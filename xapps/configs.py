# Prometheus exporter
EXPORTER_PORT = 9000
EXPORTER_UPDATE_PERIOD = 1
PROMETHEUS_URL = "http://129.97.168.51:30090"

# ue-slice association
ASSOCIATOR_UPDATE_PERIOD = 0.5

# raw exposer
EXPOSER_UPDATE_PERIOD = 0.5

# RNTI-IMSI Mapping
TEID_IMSI_UPDATE_PERIOD = 0.1
RNTI_TEID_UPDATE_PERIOD = 0.3

# Paths
metrics_path = {"mac": "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_stats_mac.json",
                "rlc": "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_stats_rlc.json",
                "pdcp": "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_stats_pdcp.json"}

# slicing
slice_indication_path = "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/exporter_indication_slice.json"
imsi_slice_path ="/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/imsi_slice_mapping_dict.json"

# RNTI-IMSI stuff
rnti_imsi_path = "/home/mzi/ran-slicing-flexric-gym/flexric/build/examples/xApp/python3/stats/rnti_imsi.json"
rnti_teid_path = "/home/mzi/tunnel_rnti.txt"
imsi_teid_path = "/home/mzi/imsi_teid.txt"

# metrics
mac_kpi_list = ['dl_aggr_tbs', 'ul_aggr_tbs', 'dl_aggr_bytes_sdus', 'ul_aggr_bytes_sdus', 'dl_curr_tbs', 'ul_curr_tbs', 'dl_sched_rb', 'ul_sched_rb', 'pusch_snr', 'pucch_snr', 'dl_bler', 'ul_bler', 'dl_num_harq', 'ul_num_harq', 'rnti', 'dl_aggr_prb', 'ul_aggr_prb', 'dl_aggr_sdus', 'ul_aggr_sdus', 'dl_aggr_retx_prb', 'ul_aggr_retx_prb', 'bsr', 'frame', 'slot', 'wb_cqi', 'dl_mcs1', 'ul_mcs1', 'dl_mcs2', 'ul_mcs2', 'phr']
rlc_kpi_list = ['txpdu_pkts', 'txpdu_bytes', 'txpdu_wt_ms', 'txpdu_dd_pkts', 'txpdu_dd_bytes', 'txpdu_retx_pkts', 'txpdu_retx_bytes', 'txpdu_segmented', 'txpdu_status_pkts', 'txpdu_status_bytes', 'txbuf_occ_bytes', 'txbuf_occ_pkts', 'rxpdu_pkts', 'rxpdu_bytes', 'rxpdu_dup_pkts', 'rxpdu_dup_bytes', 'rxpdu_dd_pkts', 'rxpdu_dd_bytes', 'rxpdu_ow_pkts', 'rxpdu_ow_bytes', 'rxpdu_status_pkts', 'rxpdu_status_bytes', 'rxbuf_occ_bytes', 'rxbuf_occ_pkts', 'txsdu_pkts', 'txsdu_bytes', 'rxsdu_pkts', 'rxsdu_bytes', 'rxsdu_dd_pkts', 'rxsdu_dd_bytes', 'rnti', 'mode', 'rbid']
pdcp_kpi_list = ['txpdu_pkts', 'txpdu_bytes', 'txpdu_sn', 'rxpdu_pkts', 'rxpdu_bytes', 'rxpdu_sn', 'rxpdu_oo_pkts', 'rxpdu_oo_bytes', 'rxpdu_dd_pkts', 'rxpdu_dd_bytes', 'rxpdu_ro_count', 'txsdu_pkts', 'txsdu_bytes', 'rxsdu_pkts', 'rxsdu_bytes', 'rnti', 'mode', 'rbid']
