import netmiko


# 登录用户名和密码
username = 'admin'
password = 'cisco'
enable_pwd = 'cisco'
# IOS设备的IP地址
dhcp_server_ip = "192.168.20.5"


# 文档：https://github.com/ktbyers/netmiko
def ssh_netmiko(vid, device_ip):
    vlanid = str(vid)
    # 使用VLANID产生子网
    network_sub = "172.16." + vlanid + "."
    # 下面是DHCP的具体CLI命令的列表
    dhcp_pool_command = ["ip dhcp pool Vlan" + vlanid,
                         "network " + network_sub + "0 /24",
                         "default-router " + network_sub + "1",
                         "dns-server 8.8.8.8",
                         "exit",
                         "ip dhcp excluded-address " + network_sub + "1 " + network_sub + "99",
                         "ip dhcp excluded-address " + network_sub + "101 " + network_sub + "254",
                         ]

    # 建立SSH连接
    cisco_ssh = netmiko.Netmiko(device_type='cisco_ios', ip=device_ip, username=username, password=password, secret=enable_pwd)
    # 启用enable进入特权模式
    cisco_ssh.enable()
    # 执行命令前会默认执行config term进入全局配置模式，netmiko收到设备的回应提示符后，会自动执行下一条命令
    result = cisco_ssh.send_config_set(dhcp_pool_command)
    print(result)
    print('=' * 100)
    print("DHCP Service for CentOS_" + vlanid + " is all ready")
    cisco_ssh.disconnect()


if __name__ == '__main__':
    ssh_netmiko(199, dhcp_server_ip)
