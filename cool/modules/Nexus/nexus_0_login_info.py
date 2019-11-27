import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 登录设备用户名和密码
username = "admin"
password = "YUting@123"

# JSON RPC的头部
my_headers_rpc = {"content-type": "application/json-rpc"}
# REST API的头部
my_headers = {"content-type": "application/json"}


# 获取REST API登录的会话
def get_session(ip):
    client = requests.session()
    login_url = 'http://' + ip + '/api/aaaLogin.json'
    name_pwd = {'aaaUser': {'attributes': {'name': username, 'pwd': password}}}
    client.post(login_url, json=name_pwd, headers=my_headers, verify=False)
    return client

