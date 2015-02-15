#! /usr/bin/env python
import os, sys, optparse, netaddr
# ipaddress

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
	mac = ('00:00:%02x:%02x:%02x:%02x' %(ip_list[0],ip_list[1],ip_list[2],ip_list[3]))    #Construct the hostname
	return mac

def hostname_generator( ip_address ):
        """generates hostnames based on IP address. assumes no more that 255 hosts in a swim lane"""
        ip_address_int = int(ip_address) #turn IP address, which is currently a class into an integer
        ip_list = [ ip_address_int / 16777216, (ip_address_int % 16777216) / 65536, ((ip_address_int % 16777216) % 65536) / 256, (((ip_address_int % 16777216) % 65536) % 256)]
        hostname = ('swim%03dhost%03d' %(ip_list[2],ip_list[3]))    #Construct the hostname
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

def write_virt_install( hostname, sequence, ManNet_mac, ProNet_mac, filename ):
        with open(filename, 'a') as out3:
                out3.write ('virt-install --connect qemu:///system -n %s -r 2048 --vcpus=1 --disk path=/vols/%s.img,size=5,device=disk,bus=virtio --vnc --vncport=9%03d --vnclisten=10.51.107.100 --noautoconsole --os-type linux --accelerate --network=bridge:br0,mac=%s,model=virtio --network=bridge:br1,mac=%s,model=virtio --hvm --pxe\n' %(hostname, hostname, sequence, ManNet_mac, ProNet_mac))

netManagement = ipaddress.ip_network(u'10.1.2.0/20')
netProduction = ipaddress.ip_network(u'192.168.2.0/20')

filename_M = "/etc/dhcp/dhcpd.conf.10.1.1.0"
filename_P = "/etc/dhcp/dhcpd.conf.192.168.2.0"
os.unlink(filename_M)
os.unlink(filename_P)

# check = file_exist_check( filename  )

for ManNet_ip, ProNet_ip in zip(netManagement.hosts(), netProduction.hosts()) :
		ManNet_mac = mac_address_generator(ManNet_ip)
		ProNet_mac = mac_address_generator(ProNet_ip)
		ManNet_host = hostname_generator(ManNet_ip)
		ProNet_host = hostname_generator(ProNet_ip)
		print ManNet_host
		write_dhcpd_conf ( ManNet_mac, ManNet_ip, ManNet_host[0] , 'test.mydomain.com', filename_M  )
		write_dhcpd_conf_pro ( ProNet_mac, ProNet_ip, ProNet_host[0], 'test.mydomain.com', filename_P  )
		write_virt_install ( ManNet_host[0], ManNet_host[1], ManNet_mac, ProNet_mac, "virt_install_filename" ) 
