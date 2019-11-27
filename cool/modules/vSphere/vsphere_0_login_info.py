import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from requests.auth import HTTPBasicAuth


# vCenter IP地址
vcip = '192.168.0.101'
# vCenter登录用户名和密码
username = 'administrator@vsphere.local'
password = 'YUting@123'
# vCenter登录并且获取Cookie的URL链接
login_url = 'https://' + vcip + '/rest/com/vmware/cis/session'  # 请求的URL


# 登录,获取Cookie并且维持会话
def get_session():
    client = requests.session()
    client.post(login_url, auth=HTTPBasicAuth(username, password), verify=False)

    return client


vc_session = get_session()

