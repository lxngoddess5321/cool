from cool.modules.Nexus.nexus_0_login_info import get_session, my_headers

dhcp_ip_address = "172.16.254.254"


# 激活DHCP Relay
# 具体配置如下:
# ip dhcp relay
def enable_dhcp_relay(ip):
    session = get_session(ip)
    nxos_api_url = "https://" + ip + "/api/mo/sys/dhcp.json"

    payload = {
            "dhcpEntity": {
                "children": [{
                    "dhcpInst": {
                        "attributes": {
                            "v4RelayEnabled": "yes"
                            }
                        }
                    }]
                }
            }

    session.post(nxos_api_url, headers=my_headers, json=payload, verify=False)


# 配置DHCP Relay服务器地址
# 配置不出现在show run
# 可以使用show ip dhcp relay查看
#  Interface        Relay Address     VRF Name
#  -------------    -------------     --------
#  Vlan123           172.16.254.254
def config_dhcp_relay_server(vlanid, ip, dhcp_server_ip_address):
    session = get_session(ip)
    nxos_api_url = "https://" + ip + "/api/mo/sys/dhcp/inst.json"

    payload = {
        "dhcpInst": {
            "children": [{
                "dhcpRelayIf": {
                    "attributes": {
                        "id": "vlan" + str(vlanid)
                    },
                    "children": [{
                        "dhcpRelayAddr": {
                            "attributes": {
                                "address": dhcp_server_ip_address,
                                "counter": "2",
                                "vrf": "!unspecified"
                            }
                        }
                    }]
                }
            }]
        }
    }

    session.post(nxos_api_url, headers=my_headers, json=payload, verify=False)


if __name__ == '__main__':
    # enable_dhcp_relay('192.168.20.3')
    config_dhcp_relay_server(123, '192.168.20.3', dhcp_ip_address)

