import prometheus_client as prom

metrics_exporter = {'mac': {}, 'rlc': {}, 'pdcp': {}, 'slice': {}}

metrics_exporter['mac']['dl_aggr_tbs'] = prom.Gauge('dl_aggr_tbs', 'downlink aggregated transfer block size', ['imsi'])
metrics_exporter['mac']['ul_aggr_tbs'] = prom.Gauge('ul_aggr_tbs', 'uplink aggregated transfer block size', ['imsi'])
metrics_exporter['mac']['dl_aggr_sdus'] = prom.Gauge('dl_aggr_sdus', 'downlink aggregated transfer block size', ['imsi'])
metrics_exporter['mac']['ul_aggr_sdus'] = prom.Gauge('ul_aggr_sdus', 'uplink aggregated transfer block size', ['imsi'])
metrics_exporter['mac']['bsr'] = prom.Gauge('bsr', 'buffer state report', ['imsi'])
metrics_exporter['mac']['pusch_snr'] = prom.Gauge('pusch_snr', 'channel quality', ['imsi'])
metrics_exporter['mac']['ul_mcs1'] = prom.Gauge('ul_mcs1', 'coding scheme', ['imsi'])
metrics_exporter['mac']['phr'] = prom.Gauge('phr', 'power head room', ['imsi'])
metrics_exporter['mac']['wb_cqi'] = prom.Gauge('wb_cqi', 'channel quality', ['imsi'])

metrics_exporter['pdcp']['rxpdu_bytes'] = prom.Gauge('rxpdu_bytes', 'aggregated bytes of rx packets', ['imsi'])
metrics_exporter['pdcp']['rxpdu_pkts'] = prom.Gauge('rxpdu_pkts', 'aggregated number of rx packets', ['imsi'])
metrics_exporter['pdcp']['txpdu_bytes'] = prom.Gauge('txpdu_bytes', 'aggregated number of tx packets', ['imsi'])
metrics_exporter['pdcp']['txpdu_pkts'] = prom.Gauge('txpdu_pkts', 'aggregated bytes of tx packets', ['imsi'])

metrics_exporter['rlc']['rxbuf_occ_bytes'] = prom.Gauge('rxbuf_occ_bytes', 'current rx buffer occupancy in terms of amount of bytes', ['imsi'])
metrics_exporter['rlc']['txbuf_occ_bytes'] = prom.Gauge('txbuf_occ_bytes', 'current rx buffer occupancy in terms of amount of packets', ['imsi'])
metrics_exporter['rlc']['rxbuf_occ_pkts'] = prom.Gauge('rxbuf_occ_pkts', 'current tx bufer occupancy in terms of number of bytes', ['imsi'])
metrics_exporter['rlc']['txbuf_occ_pkts'] = prom.Gauge('txbuf_occ_pkts', 'current tx bufer occupancy in terms of number of packets', ['imsi'])

metrics_exporter['slice']['rate(dl_aggr_tbs[10s])'] = prom.Gauge('slice_dl_throughput', 'Downlink Throughput (bytes) per slice', ['slice_id'])
metrics_exporter['slice']['rate(ul_aggr_tbs[10s])'] = prom.Gauge('slice_ul_throughput', 'Uplink Throughput (bytes) per slice', ['slice_id'])
metrics_exporter['slice']['phr'] = prom.Gauge('slice_phr', 'Power headroom', ['slice_id'])
metrics_exporter['slice']['wb_cqi'] = prom.Gauge('slice_cqi', 'Chennel Quality', ['slice_id'])
metrics_exporter['slice']['slice_active_users'] = prom.Gauge('slice_active_users', 'Chennel Quality', ['slice_id'])

metrics_exporter_slice_mapping = {
    'slice_dl_throughput': 'rate(dl_aggr_tbs[10s])',
    'slice_ul_throughput': 'rate(ul_aggr_tbs[10s])',
    'slice_phr': 'phr',
    'slice_cqi': 'wb_cqi',
    'slice_active_users': 'slice_active_users'
}

# to be pushed to the exporter
metrics_list = {
    'mac': [
        'dl_aggr_tbs',      # downlink aggregated transfer block size
        'ul_aggr_tbs',      # uplink aggregated transfer block size
        'dl_aggr_sdus',     # downlink aggregated sdus
        'ul_aggr_sdus',     # uplink aggregated sdus
        'bsr',              # buffer state report
        'pusch_snr',        # channel quality
        'ul_mcs1',          # coding scheme
        'phr',              # power head room
        'wb_cqi'            # channel quality
    ],
    'rlc': [
        'rxpdu_bytes',      # aggregated bytes of rx packets
        'rxpdu_pkts',       # aggregated number of rx packets
        'txpdu_bytes',      # aggregated number of tx packets
        'txpdu_pkts',       # aggregated bytes of tx packets
    ],
    'pdcp': [
        'rxbuf_occ_bytes',  # current rx buffer occupancy in terms of amount of bytes
        'txbuf_occ_bytes',  # current rx buffer occupancy in terms of amount of packets
        'rxbuf_occ_pkts',  # current tx bufer occupancy in terms of number of bytes
        'txbuf_occ_pkts',  # current tx bufer occupancy in terms of number of packets
    ]
}

# to read from indication messages
mac_kpi_list = ['dl_aggr_tbs', 'ul_aggr_tbs', 'dl_aggr_bytes_sdus', 'ul_aggr_bytes_sdus', 'dl_curr_tbs', 'ul_curr_tbs', 'dl_sched_rb', 'ul_sched_rb', 'pusch_snr', 'pucch_snr', 'dl_bler', 'ul_bler', 'dl_num_harq', 'ul_num_harq', 'rnti', 'dl_aggr_prb', 'ul_aggr_prb', 'dl_aggr_sdus', 'ul_aggr_sdus', 'dl_aggr_retx_prb', 'ul_aggr_retx_prb', 'bsr', 'frame', 'slot', 'wb_cqi', 'dl_mcs1', 'ul_mcs1', 'dl_mcs2', 'ul_mcs2', 'phr']
rlc_kpi_list = ['txpdu_pkts', 'txpdu_bytes', 'txpdu_wt_ms', 'txpdu_dd_pkts', 'txpdu_dd_bytes', 'txpdu_retx_pkts', 'txpdu_retx_bytes', 'txpdu_segmented', 'txpdu_status_pkts', 'txpdu_status_bytes', 'txbuf_occ_bytes', 'txbuf_occ_pkts', 'rxpdu_pkts', 'rxpdu_bytes', 'rxpdu_dup_pkts', 'rxpdu_dup_bytes', 'rxpdu_dd_pkts', 'rxpdu_dd_bytes', 'rxpdu_ow_pkts', 'rxpdu_ow_bytes', 'rxpdu_status_pkts', 'rxpdu_status_bytes', 'rxbuf_occ_bytes', 'rxbuf_occ_pkts', 'txsdu_pkts', 'txsdu_bytes', 'rxsdu_pkts', 'rxsdu_bytes', 'rxsdu_dd_pkts', 'rxsdu_dd_bytes', 'rnti', 'mode', 'rbid']
pdcp_kpi_list = ['txpdu_pkts', 'txpdu_bytes', 'txpdu_sn', 'rxpdu_pkts', 'rxpdu_bytes', 'rxpdu_sn', 'rxpdu_oo_pkts', 'rxpdu_oo_bytes', 'rxpdu_dd_pkts', 'rxpdu_dd_bytes', 'rxpdu_ro_count', 'txsdu_pkts', 'txsdu_bytes', 'rxsdu_pkts', 'rxsdu_bytes', 'rnti', 'mode', 'rbid']
