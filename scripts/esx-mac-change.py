
from pysphere import * 
from pysphere.resources import VimService_services as VI 
from pysphere.vi_task import VITask 

new_mac = "mac-address-change-this"
vm_path = "[datastore] vm-name/vm-name.vmx"

#Connect to the server 
s = VIServer() 
s.connect("vcenter-ip-address", "username", "password")

vmlist = s.get_registered_vms()

#print "\n".join(vmlist)

#Get VM 
vm = s.get_vm_by_path(vm_path) 

#Find Virtual Nic device 
net_device = None 
for dev in vm.properties.config.hardware.device: 
    if dev._type in ["VirtualE1000", "VirtualE1000e", 
                     "VirtualPCNet32", "VirtualVmxnet3"]: 
        print dev._type
        net_device = dev._obj
        net_device.set_element_addressType("Manual")
        net_device.set_element_macAddress(new_mac)


exit()
if not net_device: 
    s.disconnect() 
    raise Exception("EXCEPTION: No Virtual Nic Found") 

#Set Nic macAddress to Manual and set address 
net_device.set_element_addressType("Manual") 
net_device.set_element_macAddress(new_mac) 

#Invoke ReconfigVM_Task 
request = VI.ReconfigVM_TaskRequestMsg() 
_this = request.new__this(vm._mor) 
_this.set_attribute_type(vm._mor.get_attribute_type()) 
request.set_element__this(_this) 
spec = request.new_spec() 
dev_change = spec.new_deviceChange() 
dev_change.set_element_device(net_device) 
dev_change.set_element_operation("edit") 
spec.set_element_deviceChange([dev_change]) 
request.set_element_spec(spec) 
ret = s._proxy.ReconfigVM_Task(request)._returnval 

#Wait for the task to finish 
task = VITask(ret, s) 

status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR]) 
if status == task.STATE_SUCCESS: 
    print "VM successfully reconfigured" 
elif status == task.STATE_ERROR: 
    print "Error reconfiguring vm:", task.get_error_message() 

#Disconnect from the server 
s.disconnect() 
