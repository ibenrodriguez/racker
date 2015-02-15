# begin - Iben Rodriguez
$now_string = localtime;  # e.g., " Mon Oct 21 15:25:14 2013."
print "Begin - $now_string.\n";
$row = 1;
$ge1 = 1;
$ge2 = 1;
$ge3 = 1;
$te1 = 1;
$te2 = 1;
print "row,switch,sw-port,chassis,node,node-port\n";
for ($chassis = 1; $chassis <= 11; $chassis++) {
     for ($node = 1; $node <= 4; $node++) {
         print "$row,ge1,$ge1,$chassis,$node,IPMI\n";$row++;$ge1++;
         print "$row,ge2,$ge2,$chassis,$node,ge1\n";$row++;$ge2++;
         print "$row,ge3,$ge3,$chassis,$node,ge2\n";$row++;$ge3++;
         print "$row,te1,$te1,$chassis,$node,te1\n";$row++;$te1++;
         print "$row,te2,$te2,$chassis,$node,te2\n";$row++;$te2++;
     }
 }
$now_string = localtime;
print "Done - $now_string.\n";
# end
		ge2 += 1;
		print row,",", ge3,",", ge3,",", chassis,",", node, ",ge2"
		row += 1;
		ge3 += 1;
		print row,",", te1,",", te1,",", chassis,",", node, ",te1"
		row += 1;
		te1 += 1;
		print row,",", te2,",", te2,",", chassis, ",", node, ",te2"
		row += 1;
		te2 += 1;
	chassis += 1
now_string = time.time()
print "Done - ", localtime
# end