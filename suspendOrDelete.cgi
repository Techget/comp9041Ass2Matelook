#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

use DataManipulation;

use File::Path;
use File::Copy;

$zid_cookie=cookie("zid");


if(defined param("group") && param("group") eq "suspend"){
	##remove mate relation ship from their friend, single direction, the user preserve the mate relationship information
	open F,"<$users_dir/$zid_cookie/user.txt";

	while(my $line = <F>){
		if($line =~ /^\s*mates/){
			my @matesZid = ($line =~ /z[0-9]{7}/g);
			#print @matesZid;
			foreach my $mateZid (@matesZid){
				open F2,'<',"$users_dir/$mateZid/user.txt";
				my @readFromFile = <F2>;
				close F2;
				
				open F2,'>',"$users_dir/$mateZid/user.txt";
				foreach my $tempLine (@readFromFile){
					if($tempLine =~ /^\s*mates/){
						$tempLine =~ s/(,\Q$zid_cookie\E)|(\Q$zid_cookie\E)//;
						print F2 $tempLine;
					}else{
						print F2 $tempLine;
					}
				}
				close F2;
			}
		}
	}

	close F;
	
	move("$users_dir/$zid_cookie","$suspend_dir/$zid_cookie");
	print redirect("welcomeLoginPage.cgi");
}elsif(defined param("group") && param("group") eq "delete"){
	open F,"<$users_dir/$zid_cookie/user.txt";

	while(my $line = <F>){
		if($line =~ /^\s*mates/){
			my @matesZid = ($line =~ /z[0-9]{7}/g);
			#print @matesZid;
			foreach my $mateZid (@matesZid){
				open F2,'<',"$users_dir/$mateZid/user.txt";
				my @readFromFile = <F2>;
				close F2;
				
				open F2,'>',"$users_dir/$mateZid/user.txt";
				foreach my $tempLine (@readFromFile){
					if($tempLine =~ /^\s*mates/){
						$tempLine =~ s/(,\Q$zid_cookie\E)|(\Q$zid_cookie\E)//;
						print F2 $tempLine;
					}else{
						print F2 $tempLine;
					}
				}
				close F2;
			}
		}
	}

	close F;

	rmtree("$users_dir/$zid_cookie");
	print redirect("welcomeLoginPage.cgi");
}

print header(-charset => "utf-8"), start_html('suspend or delete');

print start_form(-action=>"suspendOrDelete.cgi");
#print "I pressed suspend the result is:".param("group")."\n"."<br/>";
print "suspend<br>
  <input type=\"radio\" name=\"group\" value=\"suspend\"><br>
  Delete:<br>
  <input type=\"radio\" name=\"group\" value=\"delete\"><br/>";
print submit;
print end_form;

print end_html;



