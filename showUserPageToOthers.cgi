#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

use DataManipulation;


######this cgi file show user page to other users/his mates############

$user_zid = param("username") or die "do not have the zid cannot display user page";

#print header(-charset => "utf-8"),start_html(-title => "$user_zid user page");
if(-e "$users_dir/$user_zid/background.jpg"){
	print header(-charset => "utf-8"),start_html(-title => "$user_zid user page",-background=>"$users_dir/$user_zid/background.jpg");
}else{
	print header(-charset => "utf-8"),start_html(-title => "$user_zid user page");
}

print h2(returnUserNameWithZid($user_zid)." user page");
$tnjpgfile = returnUserImgWithZid($user_zid);
if($tnjpgfile){
	print "<span><img src=\"$tnjpgfile\" alt=\"$user_zid image\" width=\"200\" height=\"200\"></span>","\n"; 
}
#print "show to others";
print logoutHtml();
### a strange technique, the submit button's name is showUserPage, which in matelook.cgi will triger to show the user's profile
print "<form action=\"matelook.cgi?showUserPage=1\">",
    	"<input type='submit' action = \"matelook.cgi?showUserPage=1\" value=\"Go Back To My Page\" name=\"showUserPage\">",
      "</form>";

print "<br/>";

##check whether they're friends , and show add friends option if they are not
$current_user_cookie = cookie("zid");
if(! checkUsrsMateRelationship($user_zid,$current_user_cookie)){
	print "<a href=\"matelook.cgi?sendMateRequest=1&from=$current_user_cookie&to=$user_zid\">send mate request</a><br/>";
}


print searchForNameAndPostHtml();



##display user information according to notificationAndPrivacy.cgi if they not mate

if(! -e "$users_dir/$user_zid/notificationAndPrivacySetting.txt"){
	createDefaultNPStxt($user_zid);
}
open F,"<","$users_dir/$user_zid/notificationAndPrivacySetting.txt";
my @readLines=<F>;
close F;
#remove the notification setting
shift @readLines;
shift @readLines;
%displayToPublic=();
foreach my $line (@readLines){
	#print "$line 123\n";
	if($line=~/1$/){
		$line =~ s/=1//;
		#print "line:$line";
		$displayToPublic{$line}=1;
	}
}

if(checkUsrsMateRelationship($user_zid,cookie("zid"))){
	open F,"<$users_dir/$user_zid/user.txt";

	while(my $line = <F>){
		#print "<p>user infomation, what should i display?</p>";
		if($line =~ /password/){
			next;
		}else{
			print "<p>$line</p>","\n";
		}
	}

	close F;
}else{
	open F,"<$users_dir/$user_zid/user.txt";
	#print "come in here";
	#print "display to public:@displayToPublic";
	while(my $line = <F>){
		my $tempLine = $line;
		#print "tempLine1:$tempLine\n delimiter";
		$tempLine =~ s/(.*?)\=.*/$1/;
		#print "tempLine:$tempLine";
		if($displayToPublic{$tempLine}){
			#print "come in here2";
			print p("$line");
		}
	}

	close F;
}




open F,"<$users_dir/$user_zid/user.txt";

##display mate list
print "<p> MATES: </p>";
while(my $line = <F>){
	if($line =~ /^\s*mates/){
		my @matesZid = ($line =~ /z[0-9]{7}/g);
		#print @matesZid;
		foreach my $mateZid (@matesZid){
			#print "$mateZid";
			my $correspondingName = returnUserNameWithZid($mateZid);
			print "<a href=\"matelook.cgi?showUserPage=1&userZid=$mateZid\">$correspondingName</a>";
			my $tnjpgfile = returnUserImgWithZid($mateZid);
			if($tnjpgfile){
				print "<a href=\"matelook.cgi?showUserPage=1&userZid=$mateZid\"><img src=\"$tnjpgfile\" alt=\"go to $mateZid \" width=\"50\" height=\"30\"></a>"; 
			}
			print "<br/>";
		}
	}
}

close F;


##display posts


print end_html;



