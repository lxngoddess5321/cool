from cool.modules.vSphere.vsphere_0_vc_basic_actions import get_vms, delete_vm, poweroff_vm, get_networks
from cool.modules.vSphere.vsphere_0_login_info import vcip
from cool.modules.vSphere.vsphere_3_create_and_remove_portgroup import remove_pg

import time


# 删除所有的虚拟机与端口组，由于环境中存在其他虚拟机，需要依据虚拟机的名字进行删除。
# 如果环境中不存在其他虚拟机，直接调用删除函数即可。
def recovery(vcip):
    # 删除所有name是CentOS_起始的虚拟机,先关机再删除
    try:
        for vm in get_vms(vcip):
            vm_name = vm['name']
            if 'CentOS_' in vm_name:
                poweroff_vm(vcip, vm['vm'])
                delete_vm(vcip, vm['vm'])

    # 依据虚拟机的名字删除所有的Port-Group
        for net in get_networks(vcip)['value']:
            net_name = net['name']
            if 'VLAN' in net_name:
                remove_pg(net_name)
            # 每次执行都等待一秒
            time.sleep(1)
    except Exception:
        pass


if __name__ == "__main__":
    recovery(vcip)

