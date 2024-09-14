#!/usr/bin/env python
#-*- coding: utf-8 -*-

from ovirtsdk.api import API
from ovirtsdk.xml import params

try: #Api credentials is required for virtual machine
    api = API(url="https://HOST", 
              username="Radhika", 
              password="a@123", 
              ca_file="ca.crt")

    vm_name = "dummy1"
    vm_memory = 512 * 1024 * 1024 #calculating the memory in bytes
    vm_cluster = api.clusters.get(name="Default")
    vm_template = api.templates.get(name="Blank")

    #assigning the parameters to operating system
    vm_os = params.OperatingSystem(boot=[params.Boot(dev="hd")])

    vm_params = params.VM(name=vm_name,
                          memory=vm_memory,
                          cluster=vm_cluster,
                          template=vm_template,
                          os=vm_os)

    try: 
        api.vms.add(vm=vm_params) 
        print("Virtual machine '%s' added." % vm_name) #output if it is successful. 
    except Exception as ex: 
        print("Adding virtual machine '%s' failed: %s" % (vm_name, ex)) 
        api.disconnect()

except Exception as ex: 
    print("Unexpected error: %s" % ex)