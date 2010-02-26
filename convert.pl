#!usr/bin/perl -w

use strict;

my @data, my @nodes;
my %catalog, my %node;
my $outFileName = "temp.cfg";
my $foundFirst = 0;
my $Last=0;

# Open file for reading

open(FILENAME, "clustercfg") or die('clustercfg.txt does not exist');

# Read contents of file into data array 
@data = <FILENAME>;

# Close file after reading
close(FILENAME);

# Remove any new lines from end of data array
for (my $i=$#data; $i>0; $i--) {
  $data[$i] eq "\n" ? pop(@data) : last;
}

# Create hash for catalog section
foreach (@data) {
  if($_ =~ m/catalog\.(.+)=(.+$)/) { $catalog{$1} = $2; }
}

# Create hashes for nodes and push each node to array
foreach (@data) {
	if($_ =~ m/node\d+\.(.+)=(.+$)/) { ($node{$1}, $foundFirst) = ($2, 1); }
	elsif($_ =~ /\n/ && $foundFirst) { push (@nodes, {%node}); }
	if ($_ eq $data[$#data]) { push (@nodes, {%node}); }
}

 # Open file for writing
open(OUTPUT, ">$outFileName");

# Write out catalog section
print OUTPUT "[catalog]\n";

while(my ($key, $value) = each (%catalog)) {print OUTPUT "$key=$value\n";}

print OUTPUT "table=dtables(tname char(32), nodedriver char(64), nodeurl char(128), nodeuser char(16), nodepasswd char(16), partmtd int, partparam1 char(32), partparam2 char(32))";

# Write out node section
for(my $i=0; $i<@nodes; $i++){
	print OUTPUT "\n\n[node" . ($i+1) . "]\n";
	print OUTPUT "driver=".$nodes[$i]{'driver'}."\n";
	print OUTPUT "hostname=".$nodes[$i]{'hostname'}."\n";
	print OUTPUT "username=".$nodes[$i]{'username'}."\n";
	print OUTPUT "passwd=".$nodes[$i]{'passwd'};
}

# Close file after writing
close(OUTPUT);
