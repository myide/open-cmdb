#!/usr/bin/python
#coding:utf-8

"""
采集机器自身信息
主机名
内存
ip与mac地址
cpu信息
硬盘分区信息
制造商信息
出厂日期
系统版本
"""
import socket
import psutil
import subprocess
import time
import platform
import json
import requests

device_white = ['eth0', 'eth1', 'eth2', 'eth3', 'bond0', 'bond1']


def get_hostname():
    return socket.gethostname()


def get_meminfo():
    with open("/proc/meminfo") as f:
        tmp = int(f.readline().split()[1])
        return tmp / 1024


def get_device_info():
    ret = []
    for device, device_info in psutil.net_if_addrs().iteritems():
        if device in device_white:
            tmp_device = {}
            for sinc in device_info:
                if sinc.family == 2:
                    tmp_device['ip'] = sinc.address
                if sinc.family == 17:
                    tmp_device['mac'] = sinc.address
            ret.append(tmp_device)
    return ret


def get_cpu_info():
    ret = {'cpu':'','num':0}
    with open('/proc/cpuinfo') as f:
        for line in f:
            tmp = line.split(":")
            key = tmp[0].strip()
            if key == "processor":
                ret['num'] += 1
            if key == "model name":
                ret['cpu'] = tmp[1].strip()
    return ret


def get_disk_info():
    cmd = """/sbin/fdisk -l|grep Disk|egrep -v 'identifier|mapper|Disk label'"""
    disk_data = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    patition_size = []
    for dev in disk_data.stdout.readlines():
        # size = int(dev.strip().split()[4]) / 1024 / 1024/ 1024
        size = int(dev.strip().split(',')[1].split()[0]) / 1024 / 1024/ 1024
        patition_size.append(str(size))
    return " + ".join(patition_size)


# 获取制造商信息
def get_manufacturer_info():
    ret = {}
    cmd = """/usr/sbin/dmidecode | grep -A6 'System Information'"""
    manufacturer_data = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in manufacturer_data.stdout.readlines():
        if 'Manufacturer' in line:
            ret['manufacturers'] = line.split(':')[1].strip()
        elif 'Product Name' in line:
            ret['server_type'] = line.split(':')[1].strip()
        elif 'Serial Number' in line:
            ret['st'] = line.split(':')[1].strip()
        elif 'UUID' in line:
            ret['uuid'] = line.split(':')[1].strip()
    return ret


# 获取出厂日期
def get_real_date():
    cmd = """/usr/sbin/dmidecode | grep -i release"""
    date_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    real_date = date_data.stdout.readline().split(':')[1].strip()
    return time.strftime('%Y-%m-%d', time.strptime(real_date, "%m/%d/%Y"))


def get_os_version():
    return ' '.join(platform.linux_distribution())


def get_innerip(ip_info):
    inner_device = ['eth1', 'bond0']
    ret = {}
    for info in ip_info:
        if info.has_key('ip') and info.get('device', None) in inner_device:
            ret['ip'] = info.get('ip')
            ret['mac_address'] = info.get('mac')
            return ret
    return {}


def run():
    data = {}
    data['name'] = get_hostname()
    device_info = get_device_info()
    data.update(get_innerip(device_info))
    data['ip_info'] = json.dumps(device_info)

    cpu_info = get_cpu_info()
    data['cpu'] = "{cpu} {num}".format(**cpu_info)
    data['disk'] = get_disk_info()
    data['memory'] = get_meminfo()
    data.update(get_manufacturer_info())
    data['manufacture_date'] = get_real_date()
    data['os'] = get_os_version()
    if 'virtualbox' == data['server_type']:
        data['vm_status'] = 0
    else:
        data['vm_status'] = 1
    # return data
    send(data)


def send(data):
    url = 'http://192.168.205.10:8090/api/category/servercollect/'
    r = requests.post(url, data=data)
    print(r)
    print(data)


if __name__ == "__main__":
    run()
