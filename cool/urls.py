"""cool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from cloud import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('registervm/', views.vmforms),     # 创建虚拟机
    path('accounts/login/', views.cloud_login),  # 登录
    path('accounts/logout/', views.cloud_logout),  # 登出
    path('myvms/', views.myvms),        # 显示我的虚拟机
    path('webconsole/<str:name>/', views.webconsole),  # 访问webconsole
    path('poweron/<str:vmname>', views.poweron),  # 打开特定虚拟机电源
    path('poweroff/<str:vmname>', views.poweroff),  # 关闭特定虚拟机电源
    path('delete/<str:vmname>', views.delete_vm),  # 删除特定虚拟机
    path('recovery/', views.recovery_cloud),  # 重置实验环境
]
