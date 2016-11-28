#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

use DataManipulation;


$new_password = param("new_password") || '';
$confirm_new_password = param("confirm_new_password") || '';
$user_zid_cookie = cookie("zid");

if(defined $new_password && $new_password ne '' && defined $confirm_new_password && $confirm_new_password ne '' && $new_password eq $confirm_new_password && defined $user_zid_cookie){
	open F,'<',"$users_dir/$user_zid_cookie/user.txt";
	my @lines = <F>;
	close F;
	
	open F,'>',"$users_dir/$user_zid_cookie/user.txt";	
	print F "password=".$new_password."\n";
	foreach my $line (@lines){
		if($line =~ /^\s*password\s*=/){
			next;
		}else{
			print F $line;
		}
	}
	close F;
	print redirect("matelook.cgi?showUserPage=1");
}else{

	print header(-charset => "utf-8"),start_html(-title => "$user_zid_cookie change to new password");
	#print "$new_password,  $confirm_new_password";
	print start_form(-action=>"changeUserPassword.cgi");
	print "new password:",textfield(-name=>"new_password"),"\n";
	print "<br/>";
	print "confirm password:",textfield(-name=>"confirm_new_password");
	print "<br/>";
	print submit;
	print end_form;
	print end_html;	
}


