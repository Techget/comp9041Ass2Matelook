#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use File::Path qw(make_path);
use File::Copy qw(move); ##it helps to move a directory

use DataManipulation;

sub htmlUserAlreadyExist();


###the filled in information will be send back to this cgi file, and this cgi file will implement information verification####
###email validation, suspend account create. After the email is validated. User will be redirected to welcome login page.###
###and user account will be moved from suspend to the dataset if he/her click the verification link sent to his/her email###



##need at least these four infos to build a user account
$new_zid=param('ZID')||'';
$email = param('email')||'';
$password = param('password')||'';
$full_name=param('full_name')||'';

if(defined $new_zid && $new_zid =~ /z[0-9]{7}/ && defined $email && defined $password && defined $full_name){
	######check zid, is existed? is valid?
	foreach my $existing_zid (glob "$users_dir/*"){
		$existing_zid =~ s/.*?(z[0-9]{7}).*/$1/;
		if($new_zid eq $existing_zid){
			htmlUserAlreadyExist();
			#last;
			exit;
		}
	}
	#check if it's exist in suspendAccount directory
	if(-d "suspendAccount/$new_zid"){
		foreach my $existing_zid (glob "$suspend_dir/*"){
			$existing_zid =~ s/.*?(z[0-9]{7}).*/$1/;
			if($new_zid eq $existing_zid){
				htmlUserAlreadyExist();
				#last;
				exit;
			}
		}
	}

	#####send email, to check the email address
	###grab it from https://www.tutorialspoint.com/perl/perl_sending_email.htm
	my $to = $email; 
	my $from = 'z5089812@ad.unsw.edu.au';
	my $subject = 'Validate Email Address';
	#????? do not use an absolut url, how can you verify the email address
	#http://www.cse.unsw.edu.au/~z5089812/ass2
	my $url=$ENV{HTTP_REFERER};
	$url =~ s/\/createUserAccount.cgi//;
	#my $scriptName=$ENV{SCRIPT_NAME}; $ENV{SERVER_NAME} can do the same thing
	my $message = "$url/matelook.cgi?EmailVerify=1&&new_user_account_zid=$new_zid";
	 
	open(MAIL, "|/usr/sbin/sendmail -t");
	 
	# Email Header
	print MAIL "To: $to\n";
	print MAIL "From: $from\n";
	print MAIL "Subject: $subject\n\n";
	print MAIL "Content-type: text/html\n\n";
	# Email Body
	print MAIL "\n".$message;

	close(MAIL);

	###create the user directory and user.txt, put it into suspend directory, once it is verified, in the matelook.cgi will
	###move it to dataset directory
	if(! -d "$suspend_dir"){
		make_path("$suspend_dir");
	}
	make_path("$suspend_dir/$new_zid");
	my $userTXTPath = "$suspend_dir/$new_zid/user.txt";
	open F,'>',$userTXTPath;

	print F "zid=$new_zid\n";
	print F "password=$password\n";
	print F "email=$email\n";
	print F "full_name=$full_name\n";
	if(defined param('birthday')){
		print F "birthday=".param('birthday')."\n";
	}
	if(defined param('home_suburb')){
		print F "home_suburb=".param('home_suburb')."\n";
	}
	if(defined param('courses')){
		print F "courses=[".param('courses')."]"."\n";
	}
	if(defined param('profile')){
		print F "profile=".param('profile')."\n";
	}
	if(defined param('program')){
		print F "program=".param('program')."\n";
	}
	
	##initially put in the mates list, set it to null
	print F "mates=[]"."\n";
	close F;
	
	##grab this snippet from http://www.grm.cuhk.edu.hk/~htlee/perlcourse/fileupload/fileupload2.html
	$upload_filehandle = upload("image");
	if($upload_filehandle){
		open UPLOADFILE, ">$suspend_dir/$new_zid/profile.jpg";
		binmode UPLOADFILE;
		while ( <$upload_filehandle> ) { print UPLOADFILE; }
		close UPLOADFILE;
	}

	print redirect("welcomeLoginPage.cgi");

}else{
	#html indicate user to input infomation
	print header(-charset => "utf-8"), start_html('create user account');

	print h2("create user account");
	print "<div style=\"background:#F9EECF;border:10px splash black;text-align:left\">";
	print start_form(-enctype=>'multipart/form-data');
	print "*ZID:",textfield(-name=>'ZID'),"\n";
	print "<br/>";
	print "*full_name:",textfield(-name=>'full_name'),"\n";
	print "<br/>";
	print "*password:",textfield(-name=>'password',-size=>'20'),"(password length is restricted to 20 character)","\n";
	print "<br/>";
	print "*email:",textfield(-name=>'email'),"\n";
	print "<br/>";
	print "birthday:",textfield(-name=>'birthday'),"\n";
	print "<br/>";
	print "home_suburb:",textfield(-name=>'home_suburb'),"\n";
	print "<br/>";
	print "program:",textfield(-name=>'program'),"\n";
	print "<br/>";
	print "courses",textfield(-name=>'courses'),"(please follow the format:year sem coursecode, and delimit with comma(,))","\n";
	print "<br/>";
	print "Introduce self/Profile text",textarea(-name=>'profile'),"\n";
	print "<br/>";
	print "Enter a image to upload: <input type=\"file\" name=\"image\">";
	print "<br/>";
	print submit;
	print end_form;
	print "<p>items start with *, should be filled out</p>";
	print "</div>";

	print end_html;
}


###merely code reuse
sub htmlUserAlreadyExist{
	print header(-charset => "utf-8"), start_html('create user account');

	print h2("create user account");
	print "<h3 style=\"color:red\">$new_zid ALREADY EXISTS</h3>";
	print "<div style=\"background:#F9EECF;border:10px splash black;text-align:left;width:100%\">";
	print start_form(-action=>"createUserAccount.cgi",-enctype=>'multipart/form-data');
	print "*ZID:",textfield(-name=>'ZID'),"\n";
	print "<br/>";
	print "*full_name:",textfield(-name=>'full_name'),"\n";
	print "<br/>";
	print "*password:",textfield(-name=>'password'),"(password length is restricted to 20 character)","\n";
	print "<br/>";
	print "*email:",textfield(-name=>'email'),"\n";
	print "<br/>";
	print "birthday:",textfield(-name=>'birthday'),"\n";
	print "<br/>";
	print "home_suburb:",textfield(-name=>'home_suburb'),"\n";
	print "<br/>";
	print "program:",textfield(-name=>'program'),"\n";
	print "<br/>";
	print "courses",textfield(-name=>'courses'),"(please follow the format:year sem coursecode, and delimit with comma(,))","\n";
	print "<br/>";
	print "Introduce self/Profile text",textarea(-name=>'profile'),"\n";
	print "<br/>";
	print "Enter a image to upload: <input type=\"file\" name=\"image\">";
	print "<br/>";
	print submit;
	print end_form;
	print "<p>items start with *, should be filled out</p>";
	print "</div>";

	print end_html;

}
