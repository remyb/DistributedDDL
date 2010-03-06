package grading;


use strict;
use Data::Dumper;
use warnings;

require Exporter;
#use AutoLoader qw(AUTOLOAD);

our @ISA = qw(Exporter);

# Items to export into callers namespace by default. Note: do not export
# names by default without a very good reason. Use EXPORT_OK instead.
# Do not simply export all your public functions/methods/constants.

# This allows declaration use Foo::Bar ':all';
# If you do not need this, moving things directly into @EXPORT or @EXPORT_OK
# will save memory.
our %EXPORT_TAGS = ( 'all' => [ qw(

) ] );

our @EXPORT_OK = ( @{ $EXPORT_TAGS{'all'} } );

our @EXPORT = qw(
runTests
compileCode
checkRequiredFiles
rmFiles
);


#------------------------------------------------
# assumes that the cur dir is the working 
# directory
#------------------------------------------------
sub runTests {
#------------------------------------------------
   my ($stu, $testdir, $passwd, $runcmd, $tests) = @_;

   my @results = ();

   if( ! -e $runcmd )
   {
      print "$runcmd doesn't exist! skipping ...\n";
      return @results;
   }

   foreach my $t (@$tests)
   {
      my $cfgfile="test$t.cfg";
      my $sqlfile="test$t.sql";
      my $logfile="test$t.log";
      my $grepfile="test$t.grep";
      my $presql="test$t.pre.db2";
      my $postsql="test$t.post.db2";
      my $expfile="test$t.post.db2.exp";

      print "test $t : Running ...\n";

      rmFiles("test$t*");

      foreach my $f ($cfgfile, $sqlfile, $presql, $postsql, $expfile, $grepfile)
      {
         if( -e "$testdir/$f" )
         {
            `sed "s/XXTNXX/$stu/g;s/XXPWXX/$passwd/g" $testdir/$f > ./$f`;
         }
      }

      print "\tdb2 -tvf $presql > $presql.log\n";
      `db2 -tvf $presql > $presql.log`;

      print "\t$runcmd $cfgfile $sqlfile >& $logfile\n";
      `$runcmd $cfgfile $sqlfile >& $logfile`;
      if ( `grep rror $logfile` || `grep xception $logfile` )
      {
         print "test $t : runtime errors found ! see $logfile\n";
      }
      else
      {
      }

      print "\tdb2 -tvf $postsql > $postsql.log\n";
      `db2 -tvf $postsql > $postsql.log`;

      if ( -e $expfile )
      {
         print "\tdiff -B $postsql.log $expfile > $postsql.diff\n";
         `diff -B $postsql.log $expfile > $postsql.diff`;
         my $diff = `wc -l < $postsql.diff`;
         #print "diff=$diff\n";
         if ( $diff > 0 )
         {
            print "test $t : FAILED!\n\tSee $postsql.log\n";
         }
         else
         {
            print "test $t : PASSED!\n";
         }
      }
      elsif ( -e $grepfile )
      {
         # correctness is based on output in the program output
         print "\tChecking if $logfile contains patterns from $grepfile ...\n";
         if( grepPatterns($grepfile, $logfile) ==0)
         {
            print "test $t : PASSED!\n";
         }
         else 
         {
            print "test $t : FAILED!\n\t $logfile didn't contain at least one pattern from $grepfile\n";
         }

      }
      #`rm $cfgfile $sqlfile`;
   }
   return @results;
}

#------------------------------------------------
# assumes files are in current directory
# the file must contain ALL patterns in the 
# grepfile in order for success (return 0).
# grep file contains 1 pattern per line. Order of
# patterns is not important
#------------------------------------------------
sub grepPatterns
{
   my ($grepfile, $infile)=@_;

   # read in patterns to grep
   my @greplist = ();
   open ( GRE, "<$grepfile");
   while(<GRE>)
   { 
      chomp;
      push @greplist, $_; 
   }
   close ( GRE );

   my $failed=0;
   foreach my $grepstr (@greplist)
   {
      #print "checking $grepstr\n";
      my $grepout = `grep $grepstr $infile`;
      if( length($grepout)<1 )
      {
         $failed++;
         last;
      }
   }
   return $failed;
}


#------------------------------------------------
# assumes that the cur dir is the working 
# directory
#------------------------------------------------
sub compileCode{
#------------------------------------------------

   my ($cmd) = @_;

   print "$cmd >& $cmd.log\n";
   `$cmd >& $cmd.log`;
   if ( `grep error $cmd.log` )
   {
      print "Compile Errors found\n";
      return 1;
   } 
   print "Compile Success.\n";
   return 0;
}

#------------------------------------------------
# assumes that the cur dir is the working 
# directory
#------------------------------------------------
sub rmFiles {
#------------------------------------------------
   my ($expr) = @_;

   my @files=glob($expr);

   #print "Removing $expr files\n";
   if (scalar(@files)>0)
   {
      `rm $expr`;
   }
}

#------------------------------------------------
sub checkRequiredFiles {
#------------------------------------------------

   my ($studir, $filelist) = @_;

   my @srcfiles = glob("$studir/*.java");
   if ( scalar(@srcfiles)==0)
   {
      print "Cannot find java source files in current dir ... skipping dtable check\n";
   } else
   {
      if ( `grep "dtable " $studir/*.java` )
      {
         print "Error: catalog uses dtable instead of dtables\n";
      }
   }
   if (! -e "$studir/team.txt" )
   {
      print "-------------------------\n";
      print "WARNING: team.txt missing!\n\tteam.txt should contain the UH email ID of your team member. One email ID on each line.\n";
      print "-------------------------\n";
   } else {
      print "-------------------------\n";
      print "team.txt shows that the UH email IDs (without \@hawaii.edu) of your team members are:\n";
      print `cat team.txt`;
      print "\n-------------------------\n";

   }
 
  
   foreach my $reqf (@$filelist)
   { 
      if (! -e "$studir/$reqf" )
      {
         print "ERROR: $reqf missing!\n";
      }
      elsif ( $reqf =~ /compile/ || $reqf =~ /run/ )
      {
         `chmod u+x $studir/$reqf`;
         if (! `grep \"$studir\" $studir/$reqf` )
         {
            print "ERROR: paths in $reqf does not refer to current directory\n";
         }
         if ( $reqf =~ /run/ )
         {
            if ( ! `grep \"\$2\" $studir/$reqf` )  
            {
               print "ERROR: $reqf does not use the correct input arguments\n";
            }
         }
      } 
   }
}

#------------------------------------------------
#------------------------------------------------
1;
