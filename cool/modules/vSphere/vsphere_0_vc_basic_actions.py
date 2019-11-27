from cool.modules.vSphere.vsphere_0_login_info import vc_session, vcip


# 各种VC的基本操作
# 获取虚拟机清单,获取的是如下的列表
# [{'vm': 'vm-521', 'name': 'CentOS_14', 'power_state': 'POWERED_OFF'}]
def get_vms(vcip):
    url = 'https://' + vcip + '/rest/vcenter/vm'
    r = vc_session.get(url)
    return r.json()['value']


# 根据虚拟机唯一ID,获取CPU硬件配置
# {'value': {'hot_remove_enabled': False, 'count': 1, 'hot_add_enabled': False, 'cores_per_socket': 1}}
def get_vm_cpu(vcip, vmid):
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/cpu/'
    r = vc_session.get(url)
    return r.json()


# 根据虚拟机唯一ID,获取内存硬件配置
# {'value': {'size_MiB': 1024, 'hot_add_enabled': False}}
def get_vm_mem(vcip, vmid):
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/memory/'
    r = vc_session.get(url)
    return r.json()


# 获取虚拟机名字和唯一ID的映射字典
# {'CentOS_14': 'vm-521'}
def get_vms_name_id(vcip):
    url = 'https://' + vcip + '/rest/vcenter/vm'
    r = vc_session.get(url)
    # 将每个虚拟机的vm和name做映射
    return {x['name']: x['vm'] for x in r.json()['value']}


# 获取特定名字虚拟机的唯一ID
def get_vms_id_by_name(vcip, vmname):
    return get_vms_name_id(vcip).get(vmname)


# 基于虚拟机唯一ID获取当前电源状态
# {'state': 'POWERED_ON'}
def get_vm_power_status(vcip, vmid):
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/power'
    r = vc_session.get(url)
    return r.json()['value']


# 基于虚拟机唯一ID打开虚拟机电源
def poweron_vm(vcip, vmid):
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/power/start'
    r = vc_session.post(url)
    try:
        return r.json()
    except Exception:
        return 'vm has power on'


# 基于虚拟机名字打开虚拟机电源，嵌套了唯一ID转name函数
def poweron_vm_by_name(vcip, vmname):
    poweron_vm(vcip, get_vms_id_by_name(vcip, vmname))


# 基于虚拟机唯一ID关闭虚拟机电源
def poweroff_vm(vcip, vmid):
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/power/stop'
    r = vc_session.post(url)
    try:
        return r.json()
    except Exception:
        return 'vm has power off'


# 基于虚拟机名字关闭虚拟机电源
def poweroff_vm_by_name(vcip, vmname):
    poweroff_vm(vcip, get_vms_id_by_name(vcip, vmname))


# 基于虚拟机唯一ID,获取虚拟机网卡唯一ID
# {'value': [{'nic': '4000'}]}
def get_vm_nics(vcip, vmid):
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/ethernet'
    r = vc_session.get(url)
    return r.json()


# 基于虚拟机唯一ID, 网卡唯一ID,获取特定网卡详细信息
# {'value': {'start_connected': True, 'backing': {'network_name': 'VLAN14', 'type': 'STANDARD_PORTGROUP', 'network': 'network-522'}, 'mac_address': '00:50:56:b1:0c:04', 'mac_type': 'ASSIGNED', 'allow_guest_control': True, 'wake_on_lan_enabled': True, 'label': 'Network adapter 1', 'state': 'CONNECTED', 'type': 'VMXNET3', 'upt_compatibility_enabled': False}}
def get_vm_nic_detail(vcip, vmid, nic):
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/ethernet/' + nic
    r = vc_session.get(url)
    return r.json()


# 获取所有网络信息(Port-Group)
# {'value': [{'name': 'VLAN14', 'type': 'STANDARD_PORTGROUP', 'network': 'network-522'}, {'name': 'VM Network', 'type': 'STANDARD_PORTGROUP', 'network': 'network-30'}]}
def get_networks(vcip):
    url = 'https://' + vcip + '/rest/vcenter/network'
    r = vc_session.get(url)
    return r.json()


# 修改特定虚拟机(唯一ID),特定网卡(唯一ID)的Port-Group(唯一ID)
def update_vm_nic(vcip, vmid, nic, network_name):
    network_nic_json = {
        "spec": {
            "backing": {
                "type": "STANDARD_PORTGROUP",
                "network": network_name
            },
        }
    }
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/ethernet/' + nic
    r = vc_session.patch(url, json=network_nic_json)
    return r.text


# 获取ESXi主机信息
# {'value': [{'host': 'host-28', 'name': '172.16.1.201', 'connection_state': 'CONNECTED', 'power_state': 'POWERED_ON'}]}
def get_hosts(vcip):
    url = 'https://' + vcip + '/rest/vcenter/host'
    r = vc_session.get(url)
    return r.json()


# 获取存储信息
# {'value': [{'datastore': 'datastore-29', 'name': 'datastore1', 'type': 'VMFS', 'free_space': 78788952064, 'capacity': 99321118720}]}
def get_datastores(vcip):
    url = 'https://' + vcip + '/rest/vcenter/datastore'
    r = vc_session.get(url)
    return r.json()


# 获取各种类型文件夹的名字和唯一ID
# {'value': [{'folder': 'group-d1', 'name': 'Datacenters', 'type': 'DATACENTER'}, {'folder': 'group-h23', 'name': 'host', 'type': 'HOST'}, {'folder': 'group-n25', 'name': 'network', 'type': 'NETWORK'}, {'folder': 'group-s24', 'name': 'datastore', 'type': 'DATASTORE'}, {'folder': 'group-v110', 'name': 'vm_template', 'type': 'VIRTUAL_MACHINE'}, {'folder': 'group-v111', 'name': 'vm_cloned_from_template', 'type': 'VIRTUAL_MACHINE'}, {'folder': 'group-v22', 'name': 'vm', 'type': 'VIRTUAL_MACHINE'}, {'folder': 'group-v65', 'name': 'qytvm', 'type': 'VIRTUAL_MACHINE'}]}
def get_folders(vcip):
    url = 'https://' + vcip + '/rest/vcenter/folder'
    r = vc_session.get(url)
    return r.json()


# 创建虚拟机
# 需要指定文件夹(虚拟机类型),主机,存储
# 名字,操作系统,内存,CPU
def create_vm(vcip, vmname):
    vm_json = {
        "spec": {
            "placement": {
                "folder": "group-v825",
                "host": "host-684",
                "datastore": "datastore-686"
            },
            "name": vmname,
            "guest_OS": "RHEL_7_64",
            "memory": {
                "hot_add_enabled": True,
                "size_MiB": 2048
            },
            "cpu": {
                "count": 1,
                "hot_add_enabled": True,
                "hot_remove_enabled": True,
                "cores_per_socket": 1
            }
        }
    }
    url = 'https://' + vcip + '/rest/vcenter/vm/'
    r = vc_session.post(url, json=vm_json)
    return r.json()


# 基于虚拟机的唯一ID,删除一个虚拟机
def delete_vm(vcip, vmid):
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid
    r = vc_session.delete(url)
    return r.text


# 基于虚拟机的名字删除虚拟机,先关机在删除
def delete_vm_by_name(vcip, vmname):
    # Vmdb.objects.get(vm_name=vmname).delete()
    # 调用关闭电源函数，对虚拟机关机
    poweroff_vm(vcip, get_vms_id_by_name(vcip, vmname))
    delete_vm(vcip, get_vms_id_by_name(vcip, vmname))


# 为虚拟机添加网卡,关联Port-Group,返回添加网卡的唯一ID
# {"value":"4000"}
def add_vm_nic(vcip, vmid, network_name):
    add_nic_json = {
        "spec": {
            "backing": {
                "type": "STANDARD_PORTGROUP",
                "network": network_name
            },
            "allow_guest_control": True,
            "mac_type": "ASSIGNED",
            "wake_on_lan_enabled": True,
            "start_connected": True,
            "type": "VMXNET3"
        }
    }
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/ethernet'
    r = vc_session.post(url, json=add_nic_json)
    return r.text


# 增加CD-ROM
# {'value': '16000'}
def add_vm_cdrom(vcip, vmid):
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/cdrom'
    request_body = {
                    "spec": {
                        "sata": {
                            "unit": 0,
                            "bus": 0
                        },

                        "allow_guest_control": True,
                        "backing": {

                            "iso_file": "[data-esxi] IOS/ubuntu-18.04.3-desktop-amd64.iso",

                            "type": "ISO_FILE"
                        },
                        "start_connected": True,
                        "type": "SATA"
                    }
                }

    r = vc_session.post(url, json=request_body)
    return r.json()


# 增加SATA控制器，否则无法增加CD-ROM
# {'value': '16000'}
def add_vm_sata_control(vcip, vmid):
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/adapter/sata'
    request_body = {
                  "spec": {
                    "bus": 0,
                    "pci_slot_number": 0,
                    "type": "AHCI"
                  }
                }

    r = vc_session.post(url, json=request_body)
    return r.json()


if __name__ == '__main__':

    # 获取所有虚拟机数据
    print(get_vms(vcip))

    # 基于vm_id，获取vm_cpu数据
    # print(get_vm_cpu(vcip, 'vm-690'))

    # 获取vm_name和vm_id的映射关系
    # print(get_vms_name_id(vcip))

    # 基于vm_name，获取vm_id
    # print(get_vms_id_by_name(vcip, "CentOS_45"))

    # 基于vm_name，关闭vm电源
    # poweroff_vm_by_name(vcip, "kali linux")

    # 基于vm_name，开启vm电源
    # poweron_vm_by_name(vcip, "kali linux")

    # 基于vm_id，获取vm电源状态
    # print(get_vm_power_status(vcip, 'vm-741'))

    # 基于vm_id，开启vm电源
    # print(poweron_vm(vcip, 'vm-741'))

    # 基于vm_id，关闭vm电源
    # print(poweroff_vm(vcip, 'vm-741'))

    # 获取所有网络信息
    print(get_networks(vcip))

    # 基于vm_id，获取网卡_id
    # print(get_vm_nics(vcip, 'vm-690'))

    # 基于vm_od, 网卡_id，获取特定网卡详细信息
    # print(get_vm_nic_detail(vcip, 'vm-741', '4000'))

    # 基于vm_id，网卡_id，修改为指定的network
    # print(update_vm_nic(vcip, 'vm-741', '4000', 'network-688'))

    # 获取EXSI主机数据
    # print(get_hosts(vcip))

    # 获取storage数据
    # print(get_datastores(vcip))

    # 获取各种类型文件夹的名字和唯一ID
    # print(get_folders(vcip))

    # 创建vm，未关联ISO、网卡
    # print(create_vm(vcip, 'snow_newvm'))

    # 基于vm_id，增加网卡并关联网络
    # print(add_vm_nic(vcip, 'vm-851', 'network-852'))

    # 基于vm_id，增加CDROM并关联ISO
    # print(add_vm_cdrom(vcip, 'vm-842'))

    # 基于vm_id，增加SATA控制器
    # print(add_vm_sata_control(vcip, 'vm-842'))

    # 基于vm_id，删除vm
    # print(delete_vm(vcip, "vm-841"))

    # 基于vm_name，删除vm
    # print(delete_vm_by_name(vcip, 'CentOS_58'))


