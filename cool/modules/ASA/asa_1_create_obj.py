from cool.modules.ASA.asa_0_login_info import ip, my_headers, auth_header
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 创建内部Object
# rest-api image flash:/asa-restapi-131-lfbff-k8.SPA
# rest-api agent
# 文档：https://192.168.20.4/doc/#
def create_in_obj(vid, ip):
    vlanid = str(vid)
    # 使用VLANID产生内部地址
    ipaddress = "172.16." + vlanid + ".100"
    # 使用VLANID产生内部Object的名字
    object_name = "inside_" + vlanid + "_HOST"
    # 构建JSON数据
    json_data = {
                 "host": {
                          "kind": "IPv4Address",
                          "value": ipaddress
                         },
                 "kind": "object#NetworkObj",
                 "name": object_name
                 }
    url = 'https://' + ip + '/api/objects/networkobjects'  # 请求的URL
    # 使用POST发起请求,添加头部,认证信息和JSON数据
    result = requests.post(url, headers=my_headers, auth=auth_header, json=json_data, verify=False)

    # 测试
    # print(result.text)


# 创建外部Object
def create_out_obj(vid, ip):
    vlanid = str(vid)
    # 使用VLANID产生外部地址
    outside_ip = "202.100.1." + vlanid
    # 使用VLANID产生外部Object的名字
    object_name = "outside_" + vlanid
    # 构建JSON数据
    json_data = {
                 "host": {
                          "kind": "IPv4Address",
                          "value": outside_ip
                         },
                 "kind": "object#NetworkObj",
                 "name": object_name
                 }
    url = 'https://' + ip + '/api/objects/networkobjects'  # 请求的URL
    # 使用POST发起请求,添加头部,认证信息和JSON数据
    result = requests.post(url, headers=my_headers, auth=auth_header, json=json_data, verify=False)  # 使用POST发起请求,并且使用认证头部

    # 测试
    print(result.status_code)


if __name__ == "__main__":
    create_in_obj(57, ip)
    create_out_obj(57, ip)

