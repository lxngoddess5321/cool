from cool.modules.vSphere.vsphere_0_login_info import vcip, username, password
from pyVim.connect import SmartConnect, Disconnect, SmartConnectNoSSL
from pyVmomi import vim, vmodl
import sys


# 获取WEBCONSOLE的URL
def get_token_url(vmname):

    si = SmartConnectNoSSL(host=vcip, user=username, pwd=password)

    content = si.content
    objView = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vmList = objView.view
    objView.Destroy()

    vmobj = None
    for vm in vmList:
        if vm.name in vmname:
            vmobj = vm
            break

    if not vmobj:
        return None

    ticket = vmobj.AcquireTicket(ticketType='webmks')

    return 'wss://{0}:{1}/ticket/{2}'.format(ticket.host, ticket.port, ticket.ticket)


if __name__ == '__main__':
    print(get_token_url('CentOS_49'))

