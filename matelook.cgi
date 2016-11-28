#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2016
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/matelook/


###############################################################
##matelook.cgi works like a redirecting hub,
##other cgi scripts may send param to here
##and I process them and redirect to propre webpages
############################################################## 

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use File::Copy qw(move); ##it helps to move a directory

use DataManipulation;

# define some global variables
$debug = 1;
#$users_dir = "dataset-medium";

#user identification , the user id is saved in cookie, I do not specify its expire date
#so, after the browser is closed, the cookied is removed

sub main() {	
	# Now tell CGI::Carp to embed any warning in HTML
	#warningsToBrowser(1);

	$zid_cookie_value = cookie("zid");
	
	###create account should be put at first, it's a action do not need to login
	if(defined param("createUserAccount")){
		print redirect("createUserAccount.cgi");
	}
	
	if(defined param("EmailVerify") && defined param('new_user_account_zid')){
		my $new_user_account_zid=param('new_user_account_zid');
		##investigate the move function
		move("$suspend_dir/$new_user_account_zid","$users_dir/$new_user_account_zid");
	}
	
	###user forget password, send user their password.
	if(defined param("SendUserPassword")){
		print redirect("sendUserPassword.cgi");
	}
	
	###recover suspended account
	if(defined param("recoverSuspendAccount")){
		print redirect("recoverSuspendedAccount.cgi");
	}
	
	###change user password
	if(defined param("changeUserPassword")){
		print redirect("changeUserPassword.cgi");
	}
	
	###suspend or delete user account
	if(defined param("suspendOrDelete")){
		print redirect("suspendOrDelete.cgi");
	}
	
	###unmate two user
	if(defined param("unmate") && defined param("user1") && defined param("user2")){
		unmateTwoUser(param("user1"),param("user2"));
		print redirect("showUserPage.cgi?username=$zid_cookie_value"); 
	}
	
	###send mate request sendMateRequest
	if(defined param("sendMateRequest") && defined param("from") &&defined param("to")){
		#the order of parameter does matter.
		sendMateRequest(param("to"),param("from"),$ENV{HTTP_REFERER});
		print redirect("showUserPageToOthers.cgi?username=".param("to")); 
	}
	###confirmation of accept or decline to the mate request, and donot redirect to anywhere
	if(defined param("acceptMateRequest") &&  defined param("from") &&defined param("to")){
		if(! checkUsrsMateRelationship(param("from"),param("to"))){
			#avoid make them friend multiple times
			makeMateTwoUser(param("from"),param("to"));
		}
		
	}elsif(defined param("declineMateRequest") &&  defined param("from") &&defined param("to")){
		#exit 0;
		#do not need to any action currently
	}

	#login welcome page.
	#how to call relative url /welcomeLoginPage does not work
	print redirect("welcomeLoginPage.cgi") if ! defined $zid_cookie_value;

	#print param("logout") if defined param("logout");
	if (defined param("logout")){
		##here may have some potential bug, send cookie value '' to welcomeLoginPage instead of matelook.cgi
		my $userZidCookie = cookie(-name=>'zid',-value=>'');	
		#print redirect(-url=>'matelook.cgi',-cookie=>$userZidCookie); redirct to itself may solve the potential problem
		print redirect(-url=>'welcomeLoginPage.cgi',-cookie=>$userZidCookie);
	}
	#print redirect("welcomeLoginPage.cgi") if defined param("logout");

	#param(showUserPage) is a flag bit, indicate to show user page
	if (defined param("showUserPage") && defined param("userZid")){
		#this clause used after login, you can have a look on your friends web page		
		my $tempUserZid = param("userZid");
		print redirect("showUserPageToOthers.cgi?username=$tempUserZid"); 
	}elsif(defined param("showUserPage")){
		#this clause designed for login user info display
		print redirect("showUserPage.cgi?username=$zid_cookie_value"); 
	}
	
	#edit user profile signal redirect
	if(defined param('editUserProfile')){
		print redirect("editUserProfile.cgi");
	}
	
	if(defined param("notificationAndPrivacySetting")){
		print redirect("notificationAndPrivacySetting.cgi");
	}



	#test print,shouldn't print it, if it's printed, could be something wrong with cookie, shutdown the browser open it again
	print page_header();
	print "$zid_cookie_value";

	print page_trailer();
}


#after login,every webpage should have a logout 	
#submit(-name=>'LogOut',-value=>'Log Out');

#
# HTML placed at the top of every page
#
sub page_header {
    #return header(-charset => "utf-8")
    return header(-charset => "utf-8"),
        start_html(-title => 'matelook', -style => "matelook.css"),
        div({-class => "matelook_heading"}, "matelook");
}


#
# HTML placed at the bottom of every page
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}



main();

