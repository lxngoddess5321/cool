from cool.modules.vSphere.vsphere_0_vc_basic_actions import get_networks
from cool.modules.vSphere.vsphere_0_login_info import vcip


# 获取端口组对应的VLANID的清单
# [14]
def get_network_id():
    result = get_networks(vcip)

    vlanid = []

    for x in result['value']:
        try:
            if 'VLAN' in x['name']:
                # 对vm_name分片，取后面的数字放进list
                vlanid.append(int(x['name'].replace('VLAN', '')))
        except Exception:
            pass

    return vlanid


if __name__ == "__main__":
    print(get_network_id())

