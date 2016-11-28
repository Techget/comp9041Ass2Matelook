#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

use DataManipulation;

##user zid, which is stored in cookie
$zid_cookie_value = cookie("zid");


##should not allow user to change zid,full_name,email,password here
##update values if it's input
##use ne instead of !=
if(defined param('birthday') && param("birthday") ne ''){
	my $userTXTPath = "$users_dir/$zid_cookie_value/user.txt";
	open F,'<',$userTXTPath;
	my @lines=<F>;
	close F;
	open F,'>',$userTXTPath;
	#write this into file, no matter if it is exist in the orignal file
	print F "birthday=".param('birthday')."\n";
	foreach my $line (@lines){
		if($line =~ /^\s*birthday/){
			next;
		}else{
			print F $line;
		}
	}
	close F;
}
if(defined param('home_suburb') && param('home_suburb') ne ''){
	my $userTXTPath = "$users_dir/$zid_cookie_value/user.txt";
	open F,'<',$userTXTPath;
	my @lines=<F>;
	close F;
	
	open F,'>',$userTXTPath or die "can't open $userTXTPath";
	print F "home_suburb=".param('home_suburb')."\n";
	foreach my $line (@lines){
		if($line =~ /^\s*home_suburb/){
			next;
		}else{
			print F $line;
		}
	}
	close F;
}
if(defined param('courses') && param("courses") ne ''){
	my $userTXTPath = "$users_dir/$zid_cookie_value/user.txt";
	open F,'<',$userTXTPath;
	my @lines=<F>;
	close F;
	open F,'>',$userTXTPath;
	print F "courses=[".param('courses')."]"."\n";
	foreach my $line (@lines){
		if($line =~ /^\s*courses/){
			next;
		}else{
			print F $line;
		}
	}
	close F;
}
if(defined param('profile') && param("profile") ne ''){
	my $userTXTPath = "$users_dir/$zid_cookie_value/user.txt";
	open F,'<',$userTXTPath;
	my @lines=<F>;
	close F;
	
	open F,'>',$userTXTPath;
	print F "profile=".param('profile')."\n";
	foreach my $line (@lines){
		if($line =~ /^\s*profile/){
			next;
		}else{
			print F $line;
		}
	}
	close F;
}

if(defined param('program') && param("program") ne ''){
	my $userTXTPath = "$users_dir/$zid_cookie_value/user.txt";
	open F,'<',$userTXTPath;
	my @lines=<F>;
	close F;
	
	open F,'>',$userTXTPath;
	print F "program=".param('program')."\n";
	foreach my $line (@lines){
		if($line =~ /^\s*program/){
			next;
		}else{
			print F $line;
		}
	}
	close F;
}

##update image
##grab this snippet from http://www.grm.cuhk.edu.hk/~htlee/perlcourse/fileupload/fileupload2.html
$upload_filehandle = upload("image");
if($upload_filehandle){
	open UPLOADFILE, ">$users_dir/$zid_cookie_value/profile.jpg";
	binmode UPLOADFILE;
	while ( <$upload_filehandle> ) { print UPLOADFILE; }
	close UPLOADFILE;
}
##update BACKGROUND image
##grab this snippet from http://www.grm.cuhk.edu.hk/~htlee/perlcourse/fileupload/fileupload2.html
$upload_filehandle = upload("backGroundImage");
if($upload_filehandle){
	open UPLOADFILE, ">$users_dir/$zid_cookie_value/background.jpg";
	binmode UPLOADFILE;
	while ( <$upload_filehandle> ) { print UPLOADFILE; }
	close UPLOADFILE;
}

##remove profile images 
if(defined param('dpi')){
	if(-e "$users_dir/$zid_cookie_value/profile.jpg"){
		unlink "$users_dir/$zid_cookie_value/profile.jpg";
	}
}
##remove background images
if(defined param('dbi')){
	#print "dbi\n";'
	if(-e "$users_dir/$zid_cookie_value/background.jpg"){
		unlink "$users_dir/$zid_cookie_value/background.jpg";
	}
}

##print out user current information and give out the fill-in form, user could change his/her info by filling the form
print header(-charset => "utf-8"), start_html('edit user profile');

print h2("edit your profile");

### go back to user home page
### a strange technique, the submit button's name is showUserPage, which in matelook.cgi will triger to show the user's profile
print "<form action=\"matelook.cgi?showUserPage=1\">",
    	"<input type='submit' action = \"matelook.cgi?showUserPage=1\" value=\"Go Back To My Page\" name=\"showUserPage\">",
      "</form>";

print "<br/>";

###display user infomation
print "<b>Current User Profile:</b>";
open F,"<$users_dir/$zid_cookie_value/user.txt";
while(my $line = <F>){
	if($line =~ /^\s*mates/){
		next;
	}
	print "<p>$line</p>","\n";
}
close F;
$tnjpgfile = returnUserImgWithZid($zid_cookie_value );
if($tnjpgfile){
	print "<span><img src=\"$tnjpgfile\" alt=\"$zid_cookie_value image\" width=\"200\" height=\"200\"></span>","\n"; 
}


print h2("edit user profile");
print "<div style=\"background:#F9EECF;border:10px splash black;text-align:left;width:100%\">";
### need to specify the action, or else it would be /~z5089812/ass2/editUserProfile.cgi which may lost in some circumstance
print p("if you do not want to change a field, do not input anything in that field");
print start_form(-action=>"editUserProfile.cgi",-enctype=>'multipart/form-data');
print "birthday:",textfield(-name=>'birthday'),"\n";
print "<br/>";
print "home_suburb:",textfield(-name=>'home_suburb'),"\n";
print "<br/>";
print "courses",textfield(-name=>'courses'),"(please follow the format:year sem coursecode, and delimit with comma(,))","\n";
print "<br/>";
print "Introduce self/Profile text",textarea(-name=>'profile'),"\n";
print "<br/>";
print "program:",textfield(-name=>'program'),"\n";
print "<br/>";
print "Enter a image to upload: <input type=\"file\" name=\"image\">";
print "<br/>";
##only editUserProfile.cgi has this function, createUserAccount do not include upload background image
print "upload a background image : <input type=\"file\" name=\"backGroundImage\">";
print "<br/>";
##check box , to delete the profile image and background image
print "delete profile image?",checkbox(-name => 'dpi',-checked =>'0',-label   => 'delete profile image'),"\n";
print "<br/>";
print "delete background image?",checkbox(-name => 'dbi',-checked =>'0',-label   => 'delete background image'),"\n";
print "<br/>";

print submit;
print end_form;
print "</div>";

print end_html;







