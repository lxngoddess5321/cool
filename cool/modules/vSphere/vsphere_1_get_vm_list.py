from cool.modules.vSphere.vsphere_0_vc_basic_actions import get_vms
from cool.modules.vSphere.vsphere_0_login_info import vcip


# 获取虚拟机对应的VLANID的清单
# [14]
def get_vm_id():
    vm_list = get_vms(vcip)

    vm_ids = []

    for vm in vm_list:
        try:  # 要防止没有虚拟机,或者名字里边没有kali_的情况
            if 'CentOS_' in vm['name']:
                # 对vm_name分片，取后面的数字放进list
                vm_ids.append(int(vm['name'].replace('CentOS_', '')))
        except Exception:
            pass

    return vm_ids


if __name__ == "__main__":
    print(get_vm_id())

