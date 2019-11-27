from django.db import models


class Vm_data(models.Model):
    vm_name = models.CharField(max_length=100, blank=False)
    vm_summary = models.CharField(max_length=10000, blank=True)
    vm_owner = models.CharField(max_length=100, blank=False)
    vm_cpu_cores = models.IntegerField(default=1, blank=False)
    vm_mem_G = models.IntegerField(default=1, blank=False)
    vm_nics = models.IntegerField(default=1, blank=False)
    vm_nics_speed_M = models.IntegerField(default=1, blank=True)
    vm_disk_space_G = models.IntegerField(default=1, blank=True)
    vm_ip = models.GenericIPAddressField(default='1.1.1.1')
    vm_global_ip = models.GenericIPAddressField(default='1.1.1.1')
    vm_status = models.CharField(max_length=100, blank=True)
    vm_webconsole_url = models.URLField(blank=True)

