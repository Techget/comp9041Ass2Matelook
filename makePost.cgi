#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use File::Path qw(make_path);

use DataManipulation;


#warningsToBrowser(1);

$postLetters = param("myPost") or die "no post";

$zid = cookie("zid");

##if the directory does not exist, create it
if(! -d "$users_dir/$zid/posts"){
	make_path("$users_dir/$zid/posts");
}

$post_num=0;
for my $postDir (glob "$users_dir/$zid/posts/*"){
	$post_num++;
}

##mkdir "$users_dir/$zid/posts/$post_num" or die "can't create new directory for new post";
##make it while since we may delete some posts
while(-d "$users_dir/$zid/posts/$post_num"){
	$post_num++;
}
make_path("$users_dir/$zid/posts/$post_num");

###put the message with other information into post.txt
$filename="$users_dir/$zid/posts/$post_num/post.txt";
open F,'>',$filename;

print F "from=$zid\n";
print F "message=$postLetters\n";
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
print F "time="."$year\-$mon\-$mday"."T"."$hour:$min:$sec\+0000";

close F;

###send notification when zid is mentioned
if($postLetters=~/z[0-9]{7}/){
	my @matesZid = ($postLetters =~ /z[0-9]{7}/g);
	foreach my $mateZid (@matesZid){
		sendNotificationWhenZidMentioned($mateZid,"$users_dir/$zid/posts/$post_num/post.txt");
	}
}

print redirect("matelook.cgi?showUserPage=1");

