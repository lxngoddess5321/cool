from cool.modules.ASA.asa_0_login_info import ip, my_headers, auth_header
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 创建静态NAT
def create_nat(vid, ip):
    vlanid = str(vid)
    # 使用VLANID产生内部Object的名字
    inside_obj = "inside_" + vlanid + "_HOST"
    # 使用VLANID产生外部Object的名字
    outside_obj = "outside_" + vlanid
    # 构建NAT的JSON数据（删减了无效的field）
    json_data = {
              "originalSource": {
                "kind": "objectRef#NetworkObj",
                "objectId": inside_obj
              },
              "mode": "static",
              "translatedSource": {
                "kind": "objectRef#NetworkObj",
                "objectId": outside_obj
              },
              "originalInterface": {
                "kind": "objectRef#Interface",
                "name": "inside"
              },
              "translatedInterface": {
                "kind": "objectRef#Interface",
                "name": "outside"
              }
            }
    url = 'https://' + ip + '/api/nat/auto/' + inside_obj  # 请求的URL
    # 使用POST发起请求,添加头部,认证信息和JSON数据
    result = requests.post(url, headers=my_headers, auth=auth_header, json=json_data, verify=False)

    # 测试
    # print(result.status_code)


if __name__ == "__main__":
    create_nat(198, ip)

