from cool.modules.vSphere.vsphere_0_login_info import vcip
from cool.modules.vSphere.vsphere_0_vc_basic_actions import get_vms, poweron_vm, poweroff_vm


# 根据VLANID找到VM_ID，打开指定的东西VLANID虚拟机
def poweron_vm_by_vlanid(VLANID):
    global vmid
    vm_list = get_vms(vcip)
    for vm in vm_list:
        if vm['name'] == 'CentOS_' + str(VLANID):
            vmid = vm['vm']

    poweron_vm(vcip, vmid)


# 根据VLANID找到VM_ID，关闭指定的东西VLANID虚拟机
def poweroff_vm_by_vlanid(VLANID):
    global vmid
    vm_list = get_vms(vcip)
    for vm in vm_list:
        if vm['name'] == 'CentOS_' + str(VLANID):
            vmid = vm['vm']

    poweroff_vm(vcip, vmid)


if __name__ == "__main__":
    poweron_vm_by_vlanid(178)
    # poweroff_vm_by_vlanid(178)

