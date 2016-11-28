#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

use DataManipulation;


$user_zid = param("user_zid") || '';
$user_email = param("user_email") || '';

$send_password_flag=0;
$user_password='';


if(defined $user_zid && $user_zid ne '' && defined $user_email && $user_email ne ''){
	open F,'<',"$users_dir/$user_zid/user.txt" or print header(-charset => "utf-8"),start_html(-title => "$user_zid asking send password to his/her email"),
	"$user_zid not exist",
	start_form(-action=>"sendUserPassword.cgi"),
	"user_zid:",textfield(-name=>"user_zid"),
	"<br/>",
	"you register email",textfield(-name=>"user_email"),
	submit,
	end_form,
	end_html;
	while(my $line = <F>){
		if($line =~ /email/i){
			#$line =~ s/email\s*=\s*//i;
			chomp $line;
			if($line =~ /\Q$user_email\E/){
				$send_password_flag=1;	
			}
		}	
		if($line =~ /password/){
			$user_password=$line;
			#$user_password =~ s/\s*password\s*=\s*//;		
		}
	}
	close F;
	
	if($send_password_flag == 1 && $user_password ne ''){
		###grab it from https://www.tutorialspoint.com/perl/perl_sending_email.htm
		my $to = $user_email; 
		my $from = 'z5089812@ad.unsw.edu.au';
		my $subject = 'Password recovery';
		#????? do not use an absolut url, how can you verify the email address
		my $message = "user_zid:$user_zid, user_password:$user_password\n";
		 
		open(MAIL, "|/usr/sbin/sendmail -t");
		 
		# Email Header
		print MAIL "To: $to\n";
		print MAIL "From: $from\n";
		print MAIL "Subject: $subject\n\n";
		print MAIL "Content-type: text/html\n";
		# Email Body
		print MAIL $message;

		close(MAIL);
		
		#sendEmail(getEmailByZid($user_zid),'z5089812@ad.unsw.edu.au','Password recovery',"user_zid:$user_zid, user_password:$user_password\n");
		
		print redirect("welcomeLoginPage.cgi");
	}else{
		print header(-charset => "utf-8"),start_html(-title => "$user_zid asking send password to his/her email");
		print "<p style=color:\"red\">email do not match, you should use the email when you registered</p>";
		#print "$user_password 123";
		print start_form(-action=>"sendUserPassword.cgi");
		print "user_zid:",textfield(-name=>"user_zid");
		print "<br/>";
		print "you register email:",textfield(-name=>"user_email");
		print "<br/>";
		print submit;
		print end_form;
		print end_html;
	
	}
	
	
}else{
	print header(-charset => "utf-8"),start_html(-title => "$user_zid asking send password to his/her email");
	print start_form(-action=>"sendUserPassword.cgi");
	print "user_zid:",textfield(-name=>"user_zid"),"\n";
	print "<br/>";
	print "you register email:",textfield(-name=>"user_email");
	print "<br/>";
	print submit;
	print end_form;
	print end_html;
}

