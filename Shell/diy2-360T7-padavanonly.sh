#!/usr/bin/bash
#
# Copyright (c) 2019-2020 P3TERX <https://p3terx.com>
#
# This is free software, licensed under the MIT License.
# See /LICENSE for more information.
#
# https://github.com/P3TERX/Actions-OpenWrt
# File name: diy-part1.sh
# Description: OpenWrt DIY script part 1 (Before Update feeds)
#

# Uncomment a feed source
#sed -i 's/^#\(.*helloworld\)/\1/' feeds.conf.default

# Add a feed source
#echo 'src-git helloworld https://github.com/fw876/helloworld' >>feeds.conf.default
#echo 'src-git passwall https://github.com/xiaorouji/openwrt-passwall' >>feeds.conf.default

#- name: 替换默认主题 luci-theme-argon
sed -i 's/luci-theme-bootstrap/luci-theme-argon/' feeds/luci/collections/luci/Makefile

# 默认ip 192.168.1.1
sed -i 's/192.168.[0-9]\{1,3\}.1/192.168.1.1/g' package/base-files/files/bin/config_generate

# 修改时区 UTF-8
sed -i 's/UTC/CST-8/g'  package/base-files/files/bin/config_generate

# 修改主机名 OP
sed -i 's/ImmortalWrt/OpenWrt/g'  package/base-files/files/bin/config_generate

# 时区
sed -i 's/time1.apple.com/time1.cloud.tencent.com/g'  package/base-files/files/bin/config_generate
sed -i 's/time1.google.com/ntp.aliyun.com/g'  package/base-files/files/bin/config_generate
sed -i 's/time.cloudflare.com/cn.ntp.org.cn/g'  package/base-files/files/bin/config_generate
sed -i 's/pool.ntp.org/cn.pool.ntp.org/g'  package/base-files/files/bin/config_generate

# 替换源 
sed -i 's,mirrors.vsean.net/openwrt,mirrors.pku.edu.cn/immortalwrt,g'  package/emortal/default-settings/files/99-default-settings-chinese

# ---------------------------------------------------------------------------------------
# :label;  这是一个标签，用来实现跳转处理，名字可以随便取(label),后面的b label就是跳转指令
# N;  N是sed的一个处理命令，追加文本流中的下一行到模式空间进行合并处理，因此是换行符可见
# s/\n/:/;   s是sed的替换命令，将换行符替换为冒号
# b label  或者 t label    b / t 是sed的跳转命令，跳转到指定的标签处
# ---------------------------------------------------------------------------------------
# 删除以中文字符开头的行
# sed -i '1d' target/linux/mediatek/files-5.4/arch/arm64/boot/dts/mediatek/mt7981-h3c-nx30pro.dts
LANG=C sed -i ':label;N;s/^[\x81-\xFE][\x40-\xFE].*\n//g' target/linux/mediatek/files-5.4/arch/arm64/boot/dts/mediatek/mt7981-h3c-nx30pro.dts
# sed -i ":label;N;s/^[\x81-\xFE][\x40-\xFE].*\n//g" target/linux/mediatek/files-5.4/arch/arm64/boot/dts/mediatek/mt7981-h3c-nx30pro.dts
# cat target/linux/mediatek/files-5.4/arch/arm64/boot/dts/mediatek/mt7981-h3c-nx30pro.dts
# rm -rf target/linux/mediatek/files-5.4/arch/arm64/boot/dts/mediatek/mt7981-h3c-*
# ls -al target/linux/mediatek/files-5.4/arch/arm64/boot/dts/mediatek/

