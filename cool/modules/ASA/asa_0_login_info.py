from requests.auth import HTTPBasicAuth


# 登录用户名,密码和ASA的IP地址
username = 'admin'
password = 'cisco'
ip = "192.168.20.4"

# HTTP头部内容
my_headers = {"content-type": "application/json"}

# HTTP基本认证的认证信息
auth_header = HTTPBasicAuth(username, password)



