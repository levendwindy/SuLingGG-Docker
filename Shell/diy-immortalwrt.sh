#!/usr/bin/bash

# 设定LAN口 ip dns
# sed -i "/exit 0/i\uci set network.lan.ipaddr='192.168.1.210'" package/lean/default-settings/files/zzz-default-settings 
# sed -i "uci set network.lan.proto='static'" package/base-files/files/bin/config_generate
# sed -i "uci set network.lan.type='bridge'" package/base-files/files/bin/config_generate
# sed -i "uci set network.lan.ifname='eth0'" package/base-files/files/bin/config_generate
# sed -i "uci set network.lan.netmask='255.255.255.0'" package/base-files/files/bin/config_generate

# sed -i "/exit 0/i\uci set network.lan.gateway='192.168.1.1'" package/lean/default-settings/files/zzz-default-settings 
# sed -i "/exit 0/i\uci set network.lan.dns='192.168.1.1'" package/lean/default-settings/files/zzz-default-settings 
# sed -i "/exit 0/i\uci commit network" package/lean/default-settings/files/zzz-default-settings 

