#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

use DataManipulation;



#login page, include login function
#



$username = param('username') || '';
$password = param('password') || '';

if ($username && $password) {

	#print "/DataManipulation::$users_dir/$username/user.txt\n";
	#print "DataManipulation::$users_dir";

	#print "$users_dir";

	#$users_dir comes from DataManipulation
	#if user do not exist , return to login page
	if(open F,"<$users_dir/$username/user.txt"){
		while(my $line = <F>){
			if($line =~ /password/){
				chomp $line;
				my $pwd = $line;
				$pwd =~ s/\s*password\s*\=\s*//;
				if($pwd eq $password){
					##authentication success	
					$userZidCookie = cookie(-name=>'zid',-value=>$username);	
					print redirect(-url=>'matelook.cgi?showUserPage=1',-cookie=>$userZidCookie);	
					#print header(-cookie=>$userZidCookie), start_html('Login');
					#warningsToBrowser(1);
					#After you set your cookie, print out the following meta tag in the header of the file. It'll use the browser's refresh to direct you to a new page.
					#print qq{<meta http-equiv="refresh" content="0;URL=url.html">};
					
				}else{
					print header(-charset => "utf-8"), start_html('Login');
					warningsToBrowser(1);
					##wrong password input again
					#print "$pwd\n" if defined $pwd;
					#print "$password";
					print h2("Welcome to MATELOOK");
					#print logoutHtml();
					print "<br/>";
					print searchForNameAndPostHtml();

					print "<p>wrong password</p>";
					print start_form;
					print "Username:\n", textfield('username');
					print "Password:\n", textfield('password'); 
					print submit(value => Login);
					print end_form;
				}
			}
		}
	
	}else{
		print header(-charset => "utf-8"), start_html('Login');
		warningsToBrowser(1);
		print h2("Welcome to MATELOOK");
		#print logoutHtml();
		print "<br/>";
		print searchForNameAndPostHtml();

		print "$username do not exist";
		print	start_form;
		print	"Username:\n" ,textfield('username');
		print	"Password:\n" ,textfield('password'); 
		print	submit(value => Login);
		print	end_form;
	}

} elsif($username){
	print header(-charset => "utf-8"), start_html('Login');
	warningsToBrowser(1);

	print h2("Welcome to MATELOOK");
	#print logoutHtml();
	print "<br/>";
	print searchForNameAndPostHtml();

	#$_=$username;
	print start_form, "\n";
	#<INPUT TYPE="hidden" NAME  = "id" VALUE = "e07a08c4612b0172a162386ca76d2b65">
	print hidden(-name=>'username',-value=>$username); 
	#print "Username:\n", textfield('username'), "\n";
	print "Password:\n", textfield('password'), "\n";
	print submit(value => Login), "\n";
	print end_form, "\n";
} elsif($password){
	print header(-charset => "utf-8"), start_html('Login');
	warningsToBrowser(1);
	print h2("Welcome to MATELOOK");
	#print logoutHtml();
	print "<br/>";
	print searchForNameAndPostHtml();

	$_=$password;
	print start_form, "\n";
	print "Username:\n", textfield('username'), "\n";
	print hidden(-name=>'password',-value=>$password);
	#print "Password:\n", textfield('password'), "\n";
	print submit(value => Login), "\n";
	print end_form, "\n";	
} else {
	print header(-charset => "utf-8"), start_html('Login');
	warningsToBrowser(1);
	print h2("Welcome to MATELOOK");
	#print logoutHtml();
	print "<br/>";
	print searchForNameAndPostHtml();

	print start_form, "\n";
	print "Username:\n", textfield('username'), "\n";
	print "Password:\n", textfield('password'), "\n";
	print submit(value => Login), "\n";
	print end_form, "\n";
}

##create new account
print "do not have an account?","\n";
print "<a href=\"matelook.cgi?createUserAccount=1\">create a new account!</a>","\n";

##in case , user may forget his/her password
print "forget your password?","\n";
print "<a href=\"matelook.cgi?SendUserPassword=1\">Send Your password to your email.</a>","\n";

##recover suspended account
##argue this as an advanced feature
print "click to recover suspended account","\n";
print "<a href=\"matelook.cgi?recoverSuspendAccount=1\">Recover your suspended account.</a>","\n";

print end_html;
#}


#login_page();
