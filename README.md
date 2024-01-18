DESCRIPTION OF THE ENV

![ran-slicing-flexric-env](https://github.com/mhmd97z/ran-slicing-flexric-gym/assets/38925299/4496a75c-377b-4a5f-911f-b3bb0ddc1097)

# Installation
## 
### ran-slicing-flexric-env
```bash
git clone git@github.com:mhmd97z/ran-slicing-flexric-gym.git
# install the required python
pip3 install -r requirements.txt
```

### srsLTE
```bash
git clone https://github.com/srsRAN/srsRAN.git
git checkout release_21_10

# apply the patch
cd srsRAN_4G
git am <path-to-flexric-ran-slicing-env>/srsRan_patch.patch --whitespace=nowarnapply patch

# build the project
# install the necessary requirements according to the instructions of the origial repo
mkdir build && cd build
cmake ..
make

# copy the srsran config files in srs-ran-config to /root/.config/srsran/
sudo cp <path-to-flexric-ran-slicing-env>/srs-ran-config/* /root/.config/srsran/

# add the simcars' information to your /root/.config/srsran/user_db.csv

# create an access point on the phone under simcard settings, with the following specifications:
## Name: srsapn, APN: srsapn, MCC: 999, MNC: 70, APN Type: default,mms,supl,hipri,fota,cbs,xcap

# set iptables rules to forward ue's traffic
sudo iptables --policy FORWARD ACCEPT
sudo iptables -I FORWARD 1 -s 172.16.0.0/24 -j ACCEPT
sudo iptables -t nat -I POSTROUTING 1 -s 172.16.0.0/24 -o enx2c16dbab4418 -j MASQUERADE
```

### flexric
```bash
git clone git@gitlab.eurecom.fr:mosaic5g/flexric.git
git checkout b4b1aefe0fed28c757d8b9698c8ee3db084a4b82

# apply the patch
cd flexric
git am path-to-flexric-ran-slicing-env/flexric_patch.patch --whitespace=nowarnapply patch

# build the project
# install the necessary requirements according to the instructions of the origial repo

```

### ue ssh setup
1. root the phone
2. install ``SSH Server.apk'' on the phone
3. add a user to the ``SSH Server.apk''
4. copy a precompiled iperf binary to the phone using [this repo](https://github.com/KnightWhoSayNi/android-iperf)

# Example Usage
## running 

