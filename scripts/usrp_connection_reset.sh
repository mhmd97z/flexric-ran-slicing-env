#!/bin/bash
sudo ifconfig eno1 down
sudo ifconfig eno1 up
nmcli connection up id "USRP"

