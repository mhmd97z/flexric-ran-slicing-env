import prometheus_client as prom

metrics_exporter = {'mac': {}, 'rlc': {}, 'pdcp': {}}

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

slice_throughput = prom.Gauge('slice_throughput', 'Throughput (bytes) per slice', ['slice_id'])

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
