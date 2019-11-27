from cool.modules.vSphere.vsphere_0_sshclient import sshclient_execmd


# 使用paramiko SSH登录到ESXi创建标准交换机端口组
def create_pg(vlan_id):
    hostname = "192.168.0.110"
    port = 22
    username = "root"
    password = "YUting@123"
    execmd = "esxcli network vswitch standard portgroup add -p VLAN" + str(vlan_id) + " -v vSwitch1"

    try:
        sshclient_execmd(hostname, port, username, password, execmd)
    except Exception:
        sshclient_execmd(hostname, port, username, password, execmd)


# 使用paramiko SSH登录到ESXi删除标准交换机端口组
def remove_pg(vlan_name):
    hostname = "192.168.0.110"
    port = 22
    username = "root"
    password = "YUting@123"
    execmd = "esxcli network vswitch standard portgroup remove -p " + vlan_name + " -v vSwitch1"

    sshclient_execmd(hostname, port, username, password, execmd)


if __name__ == "__main__":
    # create_pg(178)
    remove_pg('VLAN58')


