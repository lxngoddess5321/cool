from cool.modules.Nexus.nexus_0_login_info import get_session, my_headers, my_headers_rpc, username, password
from requests.auth import HTTPBasicAuth
import requests


# VLAN关联VXLAN
# 具体配置如下:
# vlan 123
#   vn-segment 100123
def create_vxlan(vlanid, ip):
    session = get_session(ip)

    nxos_api_url = "https://" + ip + "/api/mo/sys/bd.json"

    payload = {
        "bdEntity": {
            "children": [{
                "l2BD": {
                    "attributes": {
                        "accEncap": "vxlan-100" + str(vlanid),
                        "fabEncap": "vlan-" + str(vlanid),
                        "pcTag": "1"
                        }
                    }
                }
            ]
        }
    }

    session.post(nxos_api_url, headers=my_headers, json=payload, verify=False)


# interface nve下关联VXLAN,并且配置组播地址
# 具体配置如下:
# interface nve1
#   member vni 100123 mcast-group 225.0.0.123
def config_vxlan_nve(vlanid, ip):
    nxos_rpc_url = "https://" + ip + "/ins"
    payload = [
        {"jsonrpc": "2.0", "method": "cli", "params": {"cmd": "configure terminal", "version": 1}, "id": 1},
        {"jsonrpc": "2.0", "method": "cli", "params": {"cmd": "interface nve 1", "version": 1}, "id": 2},
        {"jsonrpc": "2.0", "method": "cli",
         "params": {"cmd": "member vni 100" + str(vlanid) + " mcast-group 225.0.0." + str(vlanid), "version": 1}, "id": 3},
    ]
    requests.post(nxos_rpc_url, headers=my_headers_rpc, auth=HTTPBasicAuth(username, password), json=payload, verify=False)


if __name__ == "__main__":
    create_vxlan(123, '192.168.20.3')
    config_vxlan_nve(123, '192.168.20.3')
