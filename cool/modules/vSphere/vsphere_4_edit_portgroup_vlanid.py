from cool.modules.vSphere.vsphere_0_sshclient import sshclient_execmd


# 修改Port-Group的VLAN
def edit_pg_vlan_id(vlan_id):
    hostname = "192.168.0.110"
    port = 22
    username = "root"
    password = "YUting@123"
    execmd = "esxcli network vswitch standard portgroup set -p VLAN"+str(vlan_id)+" -v "+str(vlan_id)

    sshclient_execmd(hostname, port, username, password, execmd)


if __name__ == "__main__":
    edit_pg_vlan_id(178)

