# begin - Iben Rodriguez 5 June 2017
$now_string = localtime;  # e.g., " Mon Oct 21 15:25:14 2013."
print "Begin - $now_string.\n";
$row = 1;


print "row,hypervisor,tenant,vm,vnic\n";
for ($vm = 0; $vm <=12; $vm++) {
  for (my $hypervisor = 1; $hypervisor <= 3; $hypervisor++) {
       for ($tenant = 1; $tenant <= 2; $tenant++) {
         $vm++;
         for ($vnic = 1; $vnic <= 2; $vnic++) {
           print "row=",$row," hypervisor=",$hypervisor," T=",$tenant," VM=",$vm," VNIC=",$vnic,"\n";$row++;
         }
         $vm++;
         for ($vnic = 1; $vnic <= 2; $vnic++) {
           print "row=",$row," hypervisor=",$hypervisor," T=",$tenant," VM=",$vm," VNIC=",$vnic,"\n";$row++;
         }
       }
   }
 }
$now_string = localtime;
print "Done - $now_string.\n";
# end
