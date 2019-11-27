from cool.modules.ASA.asa_0_login_info import ip
from cool.modules.ASA.asa_1_create_obj import create_in_obj, create_out_obj
from cool.modules.ASA.asa_2_create_nat import create_nat
from cool.modules.ASA.asa_3_create_acl import create_acl


def asa_all_auto(vlanid, ip):
    # 第一步:创建内部外部的Object
    print('Creating ASA Object')
    create_in_obj(vlanid, ip)
    create_out_obj(vlanid, ip)
    print('ASA Object Created!')
    # 第二步:配置NAT
    print('Creating ASA NAT')
    create_nat(vlanid, ip)
    print('ASA Nat Created!')
    # 第三部:ACL放行去往内部服务器的ICMP和TCP流量
    print('Creating ASA ACL')
    create_acl(vlanid, ip)
    print('ASA ACL Created!')


if __name__ == "__main__":
    asa_all_auto(57, ip)

