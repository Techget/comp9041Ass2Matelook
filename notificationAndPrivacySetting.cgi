#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

use DataManipulation;

$zid_cookie_value = cookie("zid");

##if submit, rewrite the file is quicker
if(defined param("submitted")){
	open F,'>',"$users_dir/$zid_cookie_value/notificationAndPrivacySetting.txt";
	
	if(defined param("nwzim") && param("nwzim") ne ''){
		print F "notified when zid is mentioned=1\n";
	}else{
		print F "notified when zid is mentioned=0\n";
	}
	if(defined param("nwgamr")){
		print F "notified when get a mate request=1\n";
	}else{
		print F "notified when get a mate request=0\n";
	}
	if(defined param("profile")){
		print F "profile=1\n";
	}else{
		print F "profile=0\n";
	}
	if(defined param("home_suburb")){
		print F "home_suburb=1\n";
	}else{
		print F "home_suburb=0\n";
	}
	if(defined param("courses")){
		print F "courses=1\n";
	}else{
		print F "courses=0\n";
	}
	if(defined param("program")){
		print F "program=1\n";
	}else{
		print F "program=0\n";
	}
	if(defined param("birthday")){
		print F "birthday=1\n";
	}else{
		print F "birthday=0\n";
	}
	if(defined param("email")){
		print F "email=1\n";
	}else{
		print F "email=0\n";
	}
	close F;
}


print header(-charset => "utf-8"), start_html('edit user profile');

### go back to user home page
### a strange technique, the submit button's name is showUserPage, which in matelook.cgi will triger to show the user's profile
print "<form action=\"matelook.cgi?showUserPage=1\">",
    	"<input type='submit' action = \"matelook.cgi?showUserPage=1\" value=\"Go Back To My Page\" name=\"showUserPage\">",
      "</form>";

print "<br/>";


###display user notification and privacy setting
print "<b>Current User Notification and Privacy Setting:</b>"."<br/>";

if(-e "$users_dir/$zid_cookie_value/notificationAndPrivacySetting.txt"){
	#if exist display the information 
	open F,"<$users_dir/$zid_cookie_value/notificationAndPrivacySetting.txt";
	while(my $line = <F>){
		print $line,"\n";
		print "<br/>";
	}
	close F;
}else{
	#create a new default notificationAndPrivacySetting.txt, set all the stuff to 1
	createDefaultNPStxt($zid_cookie_value);
	open F,"<$users_dir/$zid_cookie_value/notificationAndPrivacySetting.txt";
	while(my $line = <F>){
		print $line,"\n";
		print "<br/>";
	}
	close F;
}


print "<strong>change settings to your notification and privay setting</strong>";

print start_form(-action => "notificationAndPrivacySetting.cgi");
open F,"<$users_dir/$zid_cookie_value/notificationAndPrivacySetting.txt";
print hidden("submitted","1");
##keep previous setting
while(my $line = <F>){
	if($line =~ /notified when zid is mentioned\=(\d)/){
		print "notified when zid is mentioned?",checkbox(-name => 'nwzim',-checked =>$1,-label => 'notified when zid is mentioned'),"\n";
		print "<br/>";
	}elsif($line =~ /notified when get a mate request=(\d)/){
		print "notified when get a mate request?",checkbox(-name => 'nwgamr',-checked =>$1,-label => 'notified when get a mate request'),"\n";
		print "<br/>";
	}elsif($line =~ /profile=(\d)/){
		print "profile showed to public?",checkbox(-name => 'profile',-checked =>$1,-label => 'profile showed to public'),"\n";
		print "<br/>";
	}elsif($line =~ /home_suburb=(\d)/){
		print "home_suburb showed to public?",checkbox(-name => 'home_suburb',-checked =>$1,-label => 'home_suburb showed to public'),"\n";
		print "<br/>";
	}elsif($line =~ /courses=(\d)/){
		print "courses showed to public?",checkbox(-name => 'courses',-checked =>$1,-label => 'courses showed to public'),"\n";
		print "<br/>";
	}elsif($line =~ /program=(\d)/){
		print "program showed to public?",checkbox(-name => 'program',-checked =>$1,-label => 'program showed to public'),"\n";
		print "<br/>";
	}elsif($line =~ /birthday=(\d)/){
		print "birthday showed to public?",checkbox(-name => 'birthday',-checked =>$1,-label => 'birthday showed to public'),"\n";
		print "<br/>";
	}elsif($line =~ /email=(\d)/){
		print "email showed to public?",checkbox(-name => 'email',-checked =>$1,-label => 'email showed to public'),"\n";
		print "<br/>";
	}
}
close F;
print submit;
print end_form;

print end_html;









