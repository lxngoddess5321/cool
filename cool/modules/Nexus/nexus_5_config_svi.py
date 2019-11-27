from cool.modules.Nexus.nexus_0_login_info import get_session, my_headers


# 创建SVI,并no shutdown
# 具体配置如下:
# interface Vlan40
#   no shutdown
def create_svi(vlanid, ip):
    session = get_session(ip)
    nxos_api_url = "https://" + ip + "/api/node/mo/sys/intf/svi-[vlan" + str(vlanid) + "].json"

    payload = {
        "sviIf": {
            "attributes": {
                "id": "vlan" + str(vlanid),
                "adminSt": "up"
            }
        }
    }

    session.post(nxos_api_url, headers=my_headers, json=payload, verify=False)


# 配置SVI IP地址
# 具体配置如下:
# interface Vlan40
#   ip address 172.16.40.1/24
def config_svi_ip_address(vlanid, ip):
    session = get_session(ip)
    nxos_api_url = "https://" + ip + "/api/mo/sys.json"

    payload = {
        "topSystem": {
            "children": [{
                "ipv4Entity": {
                    "children": [{
                        "ipv4Inst": {
                            "children": [{
                                "ipv4Dom": {
                                    "attributes": {
                                        "name": "vxlan-100" + str(vlanid)
                                    },
                                    "children": [{
                                        "ipv4If": {
                                            "attributes": {
                                                "id": "vlan" + str(vlanid)
                                            },
                                            "children": [{
                                                "ipv4Addr": {
                                                    "attributes": {
                                                        "addr": "172.16." + str(vlanid) + ".1/24"
                                                    }
                                                }
                                            }]
                                        }
                                    }]
                                }
                            }]
                        }
                    }]
                }
            }]
        }
    }

    session.post(nxos_api_url, headers=my_headers, json=payload, verify=False)


if __name__ == "__main__":
    # create_svi(40, '192.168.1.103')
    config_svi_ip_address(40, '192.168.20.3')

