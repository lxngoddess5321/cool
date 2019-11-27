#! /usr/bin/python3

# 导入psycopg2包
import psycopg2
import sys
sys.path.append('/home/cloud')
print(sys.path)

from cool.modules.vSphere.vsphere_0_login_info import vcip
from cool.modules.vSphere.vsphere_0_vc_basic_actions import get_vms


# 周期性(使用crontab调度,每10秒执行一次)更新数据库中虚拟机的电源状态
# crontab -e

#   Example of job definition:
#   .---------------- minute (0 - 59)
#   |  .------------- hour (0 - 23)
#   |  |  .---------- day of month (1 - 31)
#   |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
#   |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
#   |  |  |  |  |
#   *  *  *  *  * user-name  command to be executed
#   *  *  *  *  * root /usr/bin/python3 /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/Monitor_DB_VM.py >> /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/crontab.log
#   *  *  *  *  * root sleep 10; /usr/bin/python3 /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/Monitor_DB_VM.py >> /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/crontab.log
#   *  *  *  *  * root sleep 20; /usr/bin/python3 /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/Monitor_DB_VM.py >> /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/crontab.log
#   *  *  *  *  * root sleep 30; /usr/bin/python3 /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/Monitor_DB_VM.py >> /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/crontab.log
#   *  *  *  *  * root sleep 40; /usr/bin/python3 /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/Monitor_DB_VM.py >> /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/crontab.log
#   *  *  *  *  * root sleep 50; /usr/bin/python3 /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/Monitor_DB_VM.py >> /home/ljtc/config_file/cloud_snow/cool/modules/Cloud_AUTO/crontab.log


# 连接到一个给定的数据库
conn = psycopg2.connect(database="clouddb", user="clouduser",
                        password="YUting@123", host="192.168.10.122", port="5432")
# 建立游标，用来执行数据库操作
cursor = conn.cursor()

# 执行SQL命令
cursor.execute("select vm_name from cloud_vm_data")

# 获取SELECT返回的元组
results = cursor.fetchall()
print(results)

# 获取虚拟机当前的电源状态
vm_now_state = {x['name']: x['power_state'] for x in get_vms(vcip)}
print(vm_now_state)

# 以字典的格式获取所有虚拟机的状态
write_db_state = {vm[0]: vm_now_state.get(vm[0], 'UNKOWN') for vm in results}
with open('crontab.log', 'a') as f:
    f.write(str(write_db_state))
print(write_db_state)

# 以key, value形式遍历字典，返回一个列表。
# 把虚拟机当前的电源状态写入到数据库
for vm, state in write_db_state.items():
    if state == 'POWERED_ON':
        cursor.execute("update cloud_vm_data set vm_status = '电源已打开' WHERE vm_name = '%s'" % vm)
    if state == 'POWERED_OFF':
        cursor.execute("update cloud_vm_data set vm_status = '电源已关闭' WHERE vm_name = '%s'" % vm)
conn.commit()

# 关闭游标
cursor.close()

# 关闭数据库连接
conn.close()