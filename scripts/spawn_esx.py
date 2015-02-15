#! /usr/bin/env python
# Iben Rodriguez - this is spawn_esx.py - used with the pyshpere module against an vcenter - also updates DHCPD.CONF
#
import ipaddress, os
import sys, re, getpass, argparse, subprocess
from time import sleep
from pysphere import MORTypes, VIServer, VITask, VIProperty, VIMor, VIException
from pysphere.vi_virtual_machine import VIVirtualMachine
from pysphere.resources import VimService_services as VI

def file_exist_check( filename ): #check if file exists. return 0 if yes else 1.
	try:
   		with open(filename):
			return 0
	except IOError:
   		return 1

def mac_address_generator( ip_address ):
	"""generates a mac address based on the ip address"""
	ip_address_int = int(ip_address)
	ip_list = [ ip_address_int / 16777216, (ip_address_int % 16777216) / 65536, ((ip_address_int % 16777216) % 65536) / 256, (((ip_address_int % 16777216) % 65536) % 256)]
	mac = ('00:00:%02x:%02x:%02x:%02x' %(ip_list[0],ip_list[1],ip_list[2],ip_list[3]))    #Construct the mac address from the ip address
	return mac

def hostname_generator( ip_address ):
        """generates hostnames based on IP address. assumes no more that 255 hosts in a swim lane"""
        ip_address_int = int(ip_address) #turn IP address, which is currently a class into an integer
        ip_list = [ ip_address_int / 16777216, (ip_address_int % 16777216) / 65536, ((ip_address_int % 16777216) % 65536) / 256, (((ip_address_int % 16777216) % 65536) % 256)]
        hostname = ('swim%03dhost%03d' %(ip_list[2],ip_list[3]))    #Construct the hostname from the ip address
	return [hostname, ip_list[3]]

def write_dhcpd_conf( mac, ip, hostname, domain, filename): 
	with open(filename, 'a') as out1:
		out1.write ('host %s.%s {\n' %(hostname, domain))
		out1.write ('hardware ethernet %s;\n' %(mac))
                out1.write ('fixed-address %s;\n' %(ip))
		out1.write ('option host-name "%s.%s";\n' %(hostname, domain))
                out1.write ('filename "pxelinux.0";\n')
		out1.write ('}\n')
		return 1

def write_dhcpd_conf_pro( mac, ip, hostname, domain, filename):
        with open(filename, 'a') as out2:
                out2.write ('host %s {\n' %(hostname))
		out2.write ('hardware ethernet %s;\n' %(mac))
                out2.write ('fixed-address %s;\n' %(ip))
                out2.write ('}\n')
                return 1

def find_vm(name):
        try:
                vm = con.get_vm_by_name(name)
                return vm
        except VIException:
                return None

def write_virt_install( hostname, sequence, ManNet_mac, ProNet_mac, filename ):
        with open(filename, 'a') as out3:
                out3.write ('virt-install --connect qemu:///system -n %s -r 2048 --vcpus=1 --disk path=/vols/%s.img,size=5,device=disk,bus=virtio --vnc --vncport=9%03d --vnclisten=10.51.107.100 --noautoconsole --os-type linux --accelerate --network=bridge:br0,mac=%s,model=virtio --network=bridge:br1,mac=%s,model=virtio --hvm --pxe\n' %(hostname, hostname, sequence, ManNet_mac, ProNet_mac))

def spawn_esx_vm( hostname, ManNet_mac, ProNet_mac ):
	# Here we fetch the vm by its name #
	template_vm = find_vm('tcv-template')
	print ('Trying to clone %s to VM %s' % (template_vm,hostname))
	print template_vm
	print ('================================================================================')
	# Does the VM already exist? #
	if find_vm(hostname):
                print 'ERROR: %s already exists' % hostname
	else:
		clone = template_vm.clone(hostname, True, None, None, None, None, False)
		print ('VM %s created' % (hostname))

	# And now we need to change its MAC address. We expect to find a E1000 device for management and a Vmxnet3 device for production #
	# First we do the management interface. an Intel E1000 device #
	for dev in clone.properties.config.hardware.device: 
        if dev._type in ["VirtualE1000"]:  # Change to VMXNET3
        		print dev._type
        		net_device = dev._obj
        		net_device.set_element_addressType("Manual")
       			net_device.set_element_macAddress(ManNet_mac)

	#Invoke ReconfigVM_Task 
	request = VI.ReconfigVM_TaskRequestMsg()
	_this = request.new__this(clone._mor)
	_this.set_attribute_type(clone._mor.get_attribute_type())
	request.set_element__this(_this)
	spec = request.new_spec()
	dev_change = spec.new_deviceChange()
	dev_change.set_element_device(net_device)
	dev_change.set_element_operation("edit")
	spec.set_element_deviceChange([dev_change])
	request.set_element_spec(spec)
	ret = con._proxy.ReconfigVM_Task(request)._returnval

	#Wait for the task to finish 
	task = VITask(ret, con)

	status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
	if status == task.STATE_SUCCESS:
	    print "VM successfully reconfigured"
	elif status == task.STATE_ERROR:
	    print "Error reconfiguring vm:", task.get_error_message()

        for dev in clone.properties.config.hardware.device:	
		if dev._type in ["VirtualVmxnet3"]:
			print dev._type
			net_device = dev._obj
			net_device.set_element_addressType("Manual")
			net_device.set_element_macAddress(ProNet_mac)
		
	#Invoke ReconfigVM_Task 
	request = VI.ReconfigVM_TaskRequestMsg() 
	_this = request.new__this(clone._mor) 
	_this.set_attribute_type(clone._mor.get_attribute_type()) 
	request.set_element__this(_this) 
	spec = request.new_spec() 
	dev_change = spec.new_deviceChange() 
	dev_change.set_element_device(net_device) 
	dev_change.set_element_operation("edit") 
	spec.set_element_deviceChange([dev_change]) 
	request.set_element_spec(spec) 
	ret = con._proxy.ReconfigVM_Task(request)._returnval 

	#Wait for the task to finish 
	task = VITask(ret, con) 

	status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR]) 
	if status == task.STATE_SUCCESS: 
	    print "VM successfully reconfigured" 
	elif status == task.STATE_ERROR: 
	    print "Error reconfiguring vm:", task.get_error_message() 		

netManagement = ipaddress.ip_network(u'mgmt-subnet/20')
netProduction = ipaddress.ip_network(u'mission1subnet/20')

filename_M = "/etc/dhcp/dhcpd.conf.10.51.104.0"
filename_P = "/etc/dhcp/dhcpd.conf.192.168.104.0"
os.unlink(filename_M)
os.unlink(filename_P)

### Connect to vCenter ###
con = VIServer()
con.connect('vi-ip-address','username','password')

# check = file_exist_check( filename  )

for ManNet_ip, ProNet_ip in zip(netManagement.hosts(), netProduction.hosts()) :
		ManNet_mac = mac_address_generator(ManNet_ip)
		ProNet_mac = mac_address_generator(ProNet_ip)
		ManNet_host = hostname_generator(ManNet_ip)
		ProNet_host = hostname_generator(ProNet_ip)
		print ManNet_host
		write_dhcpd_conf ( ManNet_mac, ManNet_ip, ManNet_host[0] , 'test.mydomain.com', filename_M  )
		write_dhcpd_conf_pro ( ProNet_mac, ProNet_ip, ProNet_host[0], 'test.mydomain.com', filename_P  )
		spawn_esx_vm ( ManNet_host[0], ManNet_mac, ProNet_mac ) 
