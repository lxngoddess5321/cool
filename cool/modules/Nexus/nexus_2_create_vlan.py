from cool.modules.Nexus.nexus_0_login_info import get_session, my_headers


# 文档：https://developer.cisco.com/docs/cisco-nexus-3000-and-9000-series-nx-api-rest-sdk-user-guide-and-api-reference-release-9-2x/#configuring-vlans/creating-a-vlan2
# 使用REST API创建VLAN
def add_vlan(vlanid, ip):
    nxos_api_url = "https://" + ip + "/api/mo/sys/bd.json"

    payload = {
        "bdEntity": {
            "children": [{
                "l2BD": {
                    "attributes": {
                        "fabEncap": "vlan-" + str(vlanid),
                        "pcTag": "1"
                        }
                    }
                }
            ]
        }
    }
    session = get_session(ip)
    session.post(nxos_api_url, headers=my_headers, json=payload, verify=False)
    print('创建成功')


if __name__ == "__main__":
    add_vlan(40, '192.168.20.3')

