from pysphere import *
from pysphere.resources import VimService_services as VI
# from pysphere.vi_task import *
# from pysphere.vi_server import *

#Connect to the server 
s = VIServer()
s.connect("vi-ip-address", "vi-password", "vi-password")
"""
resource_pool = s.get_resource_pools()
print resource_pool
"""


vmlist = s.get_registered_vms(None, None, '/Resources/apples', None, None)
print "\n".join(vmlist)
for remove_vm in vmlist: 
	if "swim" in remove_vm:
		print remove_vm
		#Get VM
		vm = s.get_vm_by_path(remove_vm) 
		power = vm.get_status()
		print power	
		#Turn off VM
		if vm.get_status != 'POWERED OFF': 
			vm.power_off()
		#Invoke Destroy_Task 
		request = VI.Destroy_TaskRequestMsg() 
		_this = request.new__this(vm._mor) 
		_this.set_attribute_type(vm._mor.get_attribute_type()) 
		request.set_element__this(_this) 
		ret = s._proxy.Destroy_Task(request)._returnval 

		#Wait for the task to finish 
		task = VITask(ret, s) 

		status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR]) 
		if status == task.STATE_SUCCESS: 
		    print "VM successfully deleted from disk" 
		elif status == task.STATE_ERROR: 
		    print "Error removing vm:", task.get_error_message() 
	else:
		print remove_vm
	
#Disconnect from the server 
s.disconnect() 
