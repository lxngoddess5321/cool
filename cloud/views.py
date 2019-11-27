from multiprocessing.pool import ThreadPool
from random import randint

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from cloud.forms import VmForm, UserForm
from cloud.models import Vm_data

from cool.modules.Cloud_AUTO.ALL_AUTO import cloud_all_auto
from cool.modules.Cloud_AUTO.Recovery_Factory_Default import recovery
from cool.modules.vSphere.vsphere_0_login_info import vcip
from cool.modules.vSphere.vsphere_0_vc_basic_actions import poweroff_vm_by_name, poweron_vm_by_name, delete_vm_by_name
from cool.modules.vSphere.vsphere_1_get_vm_list import get_vm_id
from cool.modules.vSphere.vsphere_2_get_portgroup_list import get_network_id


# 首页
from cool.modules.vSphere.vsphere_3_create_and_remove_portgroup import remove_pg
from cool.modules.vSphere.vsphere_9_get_token import get_token_url


def index(request):
    return render(request, 'index.html')


# 创建虚拟机
@login_required()
def vmforms(request):
    if request.method == 'POST':
        form = VmForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把新添加的虚拟机信息写入数据库
        if form.is_valid():
            # 获取登录用户名
            owner = request.session.get('username')
            print('登录的用户是：', owner)
            # 随机产生VLANID,不要与已有的vmid和netid冲突
            while True:
                vlanid = randint(10, 99)
                vmid_list = get_vm_id()
                netid_list = get_network_id()
                if vlanid in vmid_list:
                    continue
                if vlanid in netid_list:
                    continue
                break

            # 由于消耗时间过长,所以使用多线程技术实现自动化
            pool = ThreadPool(processes=5)
            pool.apply_async(cloud_all_auto, args=(int(request.POST.get('cpu_cores')), int(request.POST.get('mem_G')), vlanid))

            # 把产生的新虚拟机写入数据库
            s1 = Vm_data(vm_name='CentOS_' + str(vlanid),
                         vm_global_ip="202.100.1." + str(vlanid),
                         vm_owner=owner,
                         vm_ip="172.16." + str(vlanid) + ".100",
                         vm_webconsole_url="/webconsole/CentOS_" + str(vlanid),
                         vm_cpu_cores=request.POST.get('cpu_cores'),
                         vm_mem_G=request.POST.get('mem_G'),
                         vm_disk_space_G=request.POST.get('disk_space_G'),
                         vm_nics=request.POST.get('nics'),
                         vm_nics_speed_M=request.POST.get('nics_speed_M'), )
            s1.save()
            # 写入成功后,重定向返回展示所有虚拟机信息的页面
            return HttpResponseRedirect('/myvms/')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            # 如果检查到错误,会添加错误内容到form内,例如:<ul class="errorlist"><li>QQ号码已经存在</li></ul>
            return render(request, 'registervm.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 显示表单内容给客户
        form = VmForm()
        return render(request, 'registervm.html', {'form': form})


# 展示客户虚拟机的页面,访问此页面需要认证
@login_required()
def myvms(request):
    # 获取登录用户名
    owner = request.session.get('username')
    if owner == 'admin':  # 如果是管理员可以访问所有客户的虚拟机
        # 查询整个数据库的信息 object.all()
        result = Vm_data.objects.all()
    else:  # 其他客户,只能访问自己创建和拥有的虚拟机
        result = Vm_data.objects.filter(vm_owner=owner)
    # 最终得到虚拟机清单vms_list,清单内部是每一个虚拟机信息的字典
    vms_list = []

    for x in result:

        # 产生虚拟机信息的字典
        vms_dict = {
            'name': x.vm_name,
            'cpu_cores': x.vm_cpu_cores,
            'mem_G': x.vm_mem_G,
            'disk_space_G': x.vm_disk_space_G,
            'nics': x.vm_nics,
            'nics_speed_M': x.vm_nics_speed_M,
            'owner': x.vm_owner,
            'summary': x.vm_summary,
            'global_ip': x.vm_global_ip,
            'ip': x.vm_ip,
            'status': x.vm_status,
            'webconsole_url': x.vm_webconsole_url
        }

        vms_list.append(vms_dict)
    # 返回客户虚拟机页面myvms.html
    return render(request, 'myvms.html', {'vms_list': vms_list})


# 显示客户登录页面
def cloud_login(request):
    if request.method == 'POST':
        # 获取客户提交的Form内容
        form = UserForm(request.POST)
        # 提取用户名和密码
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 校验用户的证书
        user = authenticate(username=username, password=password)
        # 如果user不是空,并且判断用户名密码有效
        if user is not None and user.is_active:
            # 用户登录
            login(request, user)
            # 创建会话变量username,并写入客户的用户名,便于后续页面提取
            request.session['username'] = username
            # 登录成功后显示主页,或者重定向的下一个页面
            next_url = request.GET.get('next', '/')
            return HttpResponseRedirect(next_url)

        else:  # 如果登录失败,给客户报错
            return render(request, 'registration/login.html', {'form': form, 'error': '用户名或密码错误'})
    else:  # 如果客户使用GET访问,并且客户已经认证,重定向他到主页
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        else:  # 如果客户使用GET访问, 给他展示登录页面
            form = UserForm()
            return render(request, 'registration/login.html', {'form': form})


# 登出操作,登出成功后,显示登录页面
def cloud_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')


# 访问特定虚拟机的WEBCONSOLE
def webconsole(request, name):
    try:  # 如果虚拟机已经准备好,嵌入webconsole的url链接到vsphere_web_console.html页面
        token_result = get_token_url(name)
        return render(request, 'vsphere_web_console.html', {'text': token_result})
    except:  # 如果虚拟机没有准备好,显示等待几分钟的页面wait_1_min.html
        return render(request, "wait_1_min.html")


# 关闭特定虚拟机电源,访问此页面需要认证
@login_required()
def poweroff(request, vmname):
    # 关闭特定虚拟机电源
    poweroff_vm_by_name(vcip, vmname)
    # 执行成功后,重定向到我的虚拟机页面
    return HttpResponseRedirect('/myvms/')


# 打开特定虚拟机电源,访问此页面需要认证
@login_required()
def poweron(request, vmname):
    # 打开特定虚拟机电源
    poweron_vm_by_name(vcip, vmname)
    # 执行成功后,重定向到我的虚拟机页面
    return HttpResponseRedirect('/myvms/')


# 删除虚拟机,访问此页面需要认证
@login_required()
def delete_vm(request, vmname):
    try:
        # 删除虚拟机(关机再删除)
        delete_vm_by_name(vcip, vmname)
        # 删除端口组
        vlan_name = vmname.replace('CentOS_', 'VLAN')
        remove_pg(vlan_name)
        # 清空Vm_data数据库
        Vm_data.objects.get(vm_name=vmname).delete()
    except Exception:
        # 清空Vm_data数据库
        Vm_data.objects.get(vm_name=vmname).delete()
    return HttpResponseRedirect('/myvms/')


# 恢复试验台页面,访问此页面需要认证
@login_required()
def recovery_cloud(request):
    # 如果客户使用POST访问
    if request.method == 'POST':
        # 删除所有虚拟机和端口组
        recovery(vcip)
        # 删除Vm_data数据库内的所有虚拟机
        Vm_data.objects.all().delete()
        return render(request, 'recovery.html')
    else:  # 如果使用GET访问,给客户展示recovery.html
        return render(request, 'recovery.html')

