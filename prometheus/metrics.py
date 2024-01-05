import prometheus_client as prom

metrics = {'mac': {}, 'rlc': {}, 'pdcp': {}}

metrics['mac']['dl_aggr_tbs'] = prom.Gauge('dl_aggr_tbs', 'downlink aggregated transfer block size', ['imsi'])
metrics['mac']['ul_aggr_tbs'] = prom.Gauge('ul_aggr_tbs', 'uplink aggregated transfer block size', ['imsi'])
metrics['mac']['dl_aggr_sdus'] = prom.Gauge('dl_aggr_sdus', 'downlink aggregated transfer block size', ['imsi'])
metrics['mac']['ul_aggr_sdus'] = prom.Gauge('ul_aggr_sdus', 'uplink aggregated transfer block size', ['imsi'])
metrics['mac']['bsr'] = prom.Gauge('bsr', 'buffer state report', ['imsi'])
metrics['mac']['pusch_snr'] = prom.Gauge('pusch_snr', 'channel quality', ['imsi'])
metrics['mac']['ul_mcs1'] = prom.Gauge('ul_mcs1', 'coding scheme', ['imsi'])
metrics['mac']['phr'] = prom.Gauge('phr', 'power head room', ['imsi'])
metrics['mac']['wb_cqi'] = prom.Gauge('wb_cqi', 'channel quality', ['imsi'])


metrics['pdcp']['rxpdu_bytes'] = prom.Gauge('rxpdu_bytes', 'aggregated bytes of rx packets', ['imsi'])
metrics['pdcp']['rxpdu_pkts'] = prom.Gauge('rxpdu_pkts', 'aggregated number of rx packets', ['imsi'])
metrics['pdcp']['txpdu_bytes'] = prom.Gauge('txpdu_bytes', 'aggregated number of tx packets', ['imsi'])
metrics['pdcp']['txpdu_pkts'] = prom.Gauge('txpdu_pkts', 'aggregated bytes of tx packets', ['imsi'])

metrics['rlc']['rxbuf_occ_bytes'] = prom.Gauge('rxbuf_occ_bytes', 'current rx buffer occupancy in terms of amount of bytes', ['imsi'])
metrics['rlc']['txbuf_occ_bytes'] = prom.Gauge('txbuf_occ_bytes', 'current rx buffer occupancy in terms of amount of packets', ['imsi'])
metrics['rlc']['rxbuf_occ_pkts'] = prom.Gauge('rxbuf_occ_pkts', 'current tx bufer occupancy in terms of number of bytes', ['imsi'])
metrics['rlc']['txbuf_occ_pkts'] = prom.Gauge('txbuf_occ_pkts', 'current tx bufer occupancy in terms of number of packets', ['imsi'])
