#!usr/bin/perl -w

# Kevin Chiogioji
# Remy Baumgarten

use strict;

my @data, my @nodes, my @nodepartinfo;
my %catalog, my %node, my %partinfo, my %partition;
my $outFileName = "temp.cfg";
my $foundFirst = 0;
my $i, my $k;


# Open file for reading
open(FILENAME, $ARGV[0]) or die('clustercfg.txt does not exist');

# Read contents of file into data array 
@data = <FILENAME>;

# Close file after reading
close(FILENAME);

# Remove any new lines from end of data array
for ($i=$#data; $i>0; $i--) {
  $data[$i] eq "\n" ? pop(@data) : last;
}

# Create hash for catalog section
foreach (@data) {
  if($_ =~ m/catalog\.(.+)=(.+$)/) { $catalog{$1} = $2; }
}

# Create hashes for nodes and push each node to array
foreach (@data) {
	if($_ =~ m/^node\d+\.(.+)=(.+$)/) { 
	  ($node{$1}, $foundFirst) = ($2, 1); 
	  if ($_ eq $data[$#data]) { 
	    push (@nodes, {%node}); 
	  }
	}
	elsif($_ =~ /\n/ && $foundFirst) { 
	  push (@nodes, {%node}); 
	}
}

# Create hashes for partiion information
foreach (@data) {
  if($_ =~ m/(tablename)=(.+$)/) {
    $partinfo{$1} = $2;
  }
  elsif($_ =~ m/partition\.(method)=(.+$)/) {
    $partinfo{$1} = $2;
  }
  elsif($_ =~ m/partition\.(column)=(.+$)/) {
    $partinfo{$1} = $2;
  }
  elsif($_ =~ m/partition\.(param1)=(.+$)/) {
    $partinfo{$1} = $2;
  }
}

# Reinitialize foundFirst variable
$foundFirst = 0;

# Create hashes for node partition information
foreach (@data) {
  if($_ =~ m/partition\.(node\d+\..+)=(\d+$)/) {
    ($partition{$1}, $foundFirst) = ($2, 1);
    if ($_ eq $data[$#data]) { 
	    push (@nodepartinfo, {%partition}); 
	  }
  }
  elsif($_ =~ m/\n/ && $foundFirst) {
    push (@nodepartinfo, {%partition});
  }
}

 # Open file for writing
open(OUTPUT, ">$outFileName");

# Write out catalog section if it exists
if (%catalog) {
  print OUTPUT "[catalog]\n";

  print OUTPUT "driver=".$catalog{'driver'}."\n";
  if ($catalog{'hostname'} =~ m/^.+:.+:\/\/(.+):(.+)\/(.+$)/){
    print OUTPUT "ip=".$1."\n";
    print OUTPUT "port=".$2."\n";
	  print OUTPUT "hostname=".$3."\n";
  }
  else {
    print OUTPUT "hostname=".$catalog{'hostname'}."\n";
  }
  print OUTPUT "username=".$catalog{'username'}."\n";
	print OUTPUT "passwd=".$catalog{'passwd'}."\n";
}

#while(my ($key, $value) = each (%catalog)) {print OUTPUT "$key=$value\n";}

#print OUTPUT "table=dtables(tname char(32), nodedriver char(64), nodeurl char(128), nodeuser char(16), nodepasswd char(16), partmtd int, partparam1 char(32), partparam2 char(32))\n";

# Remove any new lines from end of nodes array
for ($i=$#nodes; $i>0; $i--) {
  $nodes[$i] eq "\n" ? pop(@nodes) : last;
}

# Write out node section if it exists
if(@nodes) {
  for(my $i=0; $i<@nodes; $i++){
	  print OUTPUT "\n[node" . ($i+1) . "]\n";
	  print OUTPUT "driver=".$nodes[$i]{'driver'}."\n";
	  if ($nodes[$i]{'hostname'} =~ m/^.+:.+:\/\/(.+):(.+)\/(.+$)/){
	    print OUTPUT "ip=".$1."\n";
	    print OUTPUT "port=".$2."\n";
	    print OUTPUT "hostname=".$3."\n";
	  }
	  else {
	    print OUTPUT "hostname=".$nodes[$i]{'hostname'}."\n";
	  }
	  print OUTPUT "username=".$nodes[$i]{'username'}."\n";
	  print OUTPUT "passwd=".$nodes[$i]{'passwd'}."\n";
  }
}

# Write out partition information section if it exists
if(%partinfo) {
  # Write out catalog section
  print OUTPUT "\n[partition]";
  foreach $k (sort keys %partinfo) {
    print OUTPUT "\n$k = $partinfo{$k}";
  }
  print OUTPUT "\n";
}

# Write out node partion information section if it exists
if(@nodepartinfo) {
  for(my $i=0; $i<@nodepartinfo; $i++){
    my $param1 = "node".($i+1).".param".(1);
    my $param2 = "node".($i+1).".param".(2);
	  print OUTPUT "\n[node" . ($i+1) . "]\n";
	  print OUTPUT $param1."=".$nodepartinfo[$i]{$param1}."\n";
	  print OUTPUT $param2."=".$nodepartinfo[$i]{$param2}."\n";
  }
}

# Close file after writing
close(OUTPUT);
