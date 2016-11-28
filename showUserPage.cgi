#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

use List::MoreUtils qw(uniq);

use DataManipulation;

################# this is user's home page ################################################

$user_zid = param("username") or die "do not have the zid cannot display user page";

if(-e "$users_dir/$user_zid/background.jpg"){
	print header(-charset => "utf-8"),start_html(-title => "$user_zid user page",-background=>"$users_dir/$user_zid/background.jpg");
}else{
	print header(-charset => "utf-8"),start_html(-title => "$user_zid user page");
}

##welcome information and user profile image
print "<span>".h2(returnUserNameWithZid($user_zid)." user page")."</span>";
$tnjpgfile = returnUserImgWithZid($user_zid);
if($tnjpgfile){
	print "<span><img src=\"$tnjpgfile\" alt=\"$user_zid image\" width=\"200\" height=\"200\"></span>","\n"; 
}

##logout button
print logoutHtml();
print "<br/>";

##edit user information 
print "<a href=\"matelook.cgi?editUserProfile=1\">edit user profile</a>","\n";
print "<br/>";

##change user password
print "<a href=\"matelook.cgi?changeUserPassword=1\">change your password</a>","\n";
print "<br/>";

##suspend/delete user account
print "<a href=\"matelook.cgi?suspendOrDelete=1\">suspend or delete your account</a>","\n";
print "<br/>";

##edit notification and privacy info
print "<a href=\"matelook.cgi?notificationAndPrivacySetting=1\">edit user nofication and privacy setting</a>","\n";
print "<br/>";

##the search html part
print "<br/>";
print searchForNameAndPostHtml();
print "<br/>";


##display make post 
print "<p><strong>Make A Post:</strong></p>","\n";
print start_form(-method=>'POST',-action=>"makePost.cgi"),"\n";
print textarea(-name=>'myPost',-default=>'Come on, say something',-rows=>5,-columns=>100),"\n";
print submit(-name=>'submit',-value=>'submit'),"\n";
print end_form;

##display user infomation
print "<p> <strong>Your Information: </strong> </p>";
open F,"<$users_dir/$user_zid/user.txt";

while(my $line = <F>){
	if($line =~ /password/){
		next;
	}else{
		print "<p>$line</p>","\n";
	}
}

close F;

open F,"<$users_dir/$user_zid/user.txt";

##display mate list
my @matesZid;
print p("<strong> MATES: </strong>");
while(my $line = <F>){
	if($line =~ /^\s*mates/){
		@matesZid = ($line =~ /z[0-9]{7}/g);
		#print @matesZid;
		foreach my $mateZid (@matesZid){
			#print "$mateZid";
			my $correspondingName = returnUserNameWithZid($mateZid);
			print "<a href=\"matelook.cgi?showUserPage=1&userZid=$mateZid\">$correspondingName</a>";
			my $tnjpgfile = returnUserImgWithZid($mateZid);
			if($tnjpgfile){
				print "<a href=\"matelook.cgi?showUserPage=1&userZid=$mateZid\"><img src=\"$tnjpgfile\" alt=\"go to $mateZid \" width=\"50\" height=\"30\"></a>","\n"; 
			}
			print "<a href=\"matelook.cgi?unmate=1&user1=$mateZid&user2=$user_zid\">Unmate</a>\n";
			print "<br/>";
		}
	}
}

close F;

##mate suggestion
##suggest at most 5 mates to user 
print "<br/>";
print p("<strong> Mate Suggestion: </strong>");
#mateSuggestion() return an array reference
$suggestedMates=mateSuggestion($user_zid);
$countMateSuggestion=0;
foreach my $suggestedMate (@$suggestedMates){
	my $correspondingName = returnUserNameWithZid($suggestedMate);
	print "<a href=\"matelook.cgi?showUserPage=1&userZid=$suggestedMate\">$correspondingName</a>";
	my $tnjpgfile = returnUserImgWithZid($suggestedMate);
	if($tnjpgfile){
		print "<a href=\"matelook.cgi?showUserPage=1&userZid=$suggestedMate\"><img src=\"$tnjpgfile\" alt=\"go to $suggestedMate \" width=\"50\" height=\"30\"></a>","\n"; 
	}
	
	if($countMateSuggestion>=4){
		last;
	}else{
		$countMateSuggestion++;
	}
}


## pagination, declare some variables used in pagination
## the idea behind this mechenism is , everytime only the $post_count in the range of display_start_num~display_stop_num, add to $outputPosts
## set a page display 8 posts
$display_post_num=8;

if(defined param("pageNum")){
	$display_stop_num = scalar(param("pageNum"))*8 || 8;
}else{
	$display_stop_num = 8;
}
$display_start_num = $display_stop_num-$display_post_num;

$post_counter=0;

##display his posts
print "<br/>";
print "<p> <strong>POSTS:your posts,and posts from your mate</strong></p>"."\n";
print "<br/>";
$outputPosts="";
if(-d  "$users_dir/$user_zid/posts"){
	for my $postDir (glob "$users_dir/$user_zid/posts/*"){
		if($post_counter >= $display_start_num && $post_counter<$display_stop_num){
			$outputPosts .= "<div style=\"background:#F9EECF;border:10px splash black;text-align:left;margin:10px\">".displayPostWithDir($postDir,$user_zid)."</div>"."\n";
		}
		$post_counter++;
	}
}

#display mates' post
foreach my $mateZid (@matesZid){
	if(-d "$users_dir/$mateZid/posts"){
		for my $postDir (glob "$users_dir/$mateZid/posts/*"){
			##still use $user_zid in displayPostWithDir, since it indicates the posts current user can delete
			if($post_counter >= $display_start_num && $post_counter<$display_stop_num){
				$outputPosts .= "<div style=\"background:#F9EECF;border:10px splash black;text-align:left;margin:10px\">".displayPostWithDir($postDir,$user_zid)."</div>"."\n";
			}
			$post_counter++;
		}
	}

}

##eliminate the case, /z5089812/ as a directory in html, as support info transmit to server
@zidsInOutputPosts = ($outputPosts =~ /[^\/]z[0-9]{7}/g);
@uniqZidsInOutputPosts = uniq @zidsInOutputPosts;

foreach my $tempZid (@uniqZidsInOutputPosts){
	#print "tempZid:herehere:$tempZid\n";
	my $tempZidWithPreceeding= $tempZid;
	$tempZid =~ s/.(z[0-9]{7})/$1/;
	#print "tempZid:herehere:$tempZid\n";
	my $correspondingName = returnUserNameWithZid($tempZid);
	#need to care about the special character, so escape all of them
	my $substituteString = "<a href=\"matelook.cgi\?showUserPage=1\&userZid=$tempZid\">$correspondingName<\/a>";
	#my $pattern = "'$tempZid'";
	#print "$tempZid,$substituteString";
	$outputPosts =~ s/\Q$tempZidWithPreceeding\E/$substituteString/eg;
}

#display hyper link properly
if($outputPosts =~ /(https)|(http):\/\//){
	$outputPosts =~ s/(.*?)(http[^ ,]*)(.*)/$1 \<a href=\"$2\"\>$2\<\/a\> $3/g;
}

print $outputPosts,"\n";


##print out page number
#print $post_counter/$display_post_num;

$outputPageNums="Pages:";
for(my $i=1; $i<=($post_counter/$display_post_num + 1);$i++){
	$outputPageNums .= "<a href=\"showUserPage.cgi?username=$user_zid&pageNum=$i\" style=\"border:10px; border:solid;\">$i</a>  ";
}
print $outputPageNums;

print end_html;



