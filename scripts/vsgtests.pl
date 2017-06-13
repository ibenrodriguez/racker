# begin - Iben Rodriguez 5 June 2017
$now_string = localtime;  # e.g., " Mon Oct 21 15:25:14 2013."
print "Begin - $now_string.\n";
$row = 1;
$sitecount = 4;
$hypervisorpersite = 2;
$vmperhypervisor = 2;
$vnicpervm = 2;
$tenantcount = 2;
$vmcount = $sitecount * $hypervisorpersite * $vmperhypervisor * $tenantcount;

print "row,hypervisor,tenant,vm,vnic\n";
for ($vm = 0; $vm <= $vmcount; $vm++) {
  for ($site = 1; $site <= $sitecount; $site++) {
  for (my $hypervisor = 1; $hypervisor <= $hypervisorpersite; $hypervisor++) {
       for ($tenant = 1; $tenant <= $tenantcount; $tenant++) {
         $vm++;
         for ($vnic = 1; $vnic <= $vnicpervm; $vnic++) {
           print "row=",$row," site=",$site," hypervisor=",$hypervisor," T=",$tenant," VM=",$vm," VNIC=",$vnic,"\n";$row++;
         }
         $vm++;
         for ($vnic = 1; $vnic <= 2; $vnic++) {
           print "row=",$row," site=",$site," hypervisor=",$hypervisor," T=",$tenant," VM=",$vm," VNIC=",$vnic,"\n";$row++;
         }
       }
     }
   }
}
$now_string = localtime;
print "Done - $now_string.\n";
# end
