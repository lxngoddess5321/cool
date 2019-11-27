from cool.modules.Nexus.nexus_0_login_info import my_headers_rpc, username, password
from requests.auth import HTTPBasicAuth
import requests


# 使用JSON RPC执行命令获取结果,注意测试发现JSON RPC无法使用Session,只能使用HTTP基本认证
def nexus_get_vlan_lists(ip):
    payload = [
          {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
              "cmd": "show vlan brief",
              "version": 1
            },
            "id": 1
          }
        ]
    request_url = "https://" + ip + "/ins"

    r = requests.post(request_url, headers=my_headers_rpc, auth=HTTPBasicAuth(username, password), json=payload,
                      verify=False)

    response = r.json()
    vlan_response = response['result']['body']['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief']

    vlan_list = []

    # 判断返回的提取内容是不是一个列表，只有存在多个vlan信息才会是列表。
    if isinstance(vlan_response, list):
        for x in vlan_response:
            # 提取vlan号加入列表中
            vlan_list.append(x['vlanshowbr-vlanid-utf'])
        return vlan_list
    else:
        vlan_list.append(vlan_response['vlanshowbr-vlanid-utf'])
        return vlan_list


if __name__ == "__main__":
    print(nexus_get_vlan_lists('192.168.20.1'))
