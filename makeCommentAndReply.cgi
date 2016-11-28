#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use File::Path qw(make_path);

use DataManipulation;


#warningsToBrowser(1);

$content = param("content") or die "no post";

$currentDir = param("currentDir") or die "no directory comes in";
#since zid will be changed, i have to recover it here
$currentDir =~ s/(.*?)<a.*?(z[0-9]{7}).*?a>(.*)/$1$2$3/;
$currentDir =~ s/\"//g;

#it indicates who is commenting or replying
$zidCurrentUser = cookie("zid");



if(defined param("makeComment")){
	#currentDir like "dataset-medium/zid/posts/0"
	if(! -d "$currentDir/comments"){
		make_path("$currentDir/comments");
	}
	print "\$currentDir/comments:$currentDir/comments","\n";
	my $comment_num=0;
	for my $commentDir (glob "$currentDir/comments/*"){
		$comment_num++;
	}
	make_path("$currentDir/comments/$comment_num");
	print "\$currentDir/comments/\$comment_num:$currentDir/comments/$comment_num","\n";

	my $filename="$currentDir/comments/$comment_num/comment.txt";
	open F,'>',$filename;
	print F "from=$zidCurrentUser\n";
	print F "message=$content\n";
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
	print F "time="."$year\-$mon\-$mday"."T"."$hour:$min:$sec\+0000";

	close F;
	
	#send notification, if the notification flag is set to 1
	if($content=~/z[0-9]{7}/){
		my @matesZid = ($content =~ /z[0-9]{7}/g);
		foreach my $mateZid (@matesZid){
			sendNotificationWhenZidMentioned($mateZid,"$currentDir/comments/$comment_num/comment.txt");
		}
	}
	

	print redirect("matelook.cgi?showUserPage=1");

}elsif(defined param("makeReply")){
	#currentDir like "dataset-medium/zid/posts/0/comments/0"
	if(! -d "$currentDir/replies"){
		make_path("$currentDir/replies");
	}
	my $reply_num=0;
	for my $replyDir (glob "$currentDir/replies/*"){
		#print "$post_num\n";
		$reply_num++;
	}
	make_path("$currentDir/replies/$reply_num");

	my $filename="$currentDir/replies/$reply_num/reply.txt";
	open F,'>',$filename;
	print F "from=$zidCurrentUser\n";
	print F "message=$content\n";
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
	print F "time="."$year\-$mon\-$mday"."T"."$hour:$min:$sec\+0000";

	close F;
	
	#send notification, if the notification flag is set to 1
	if($content=~/z[0-9]{7}/){
		my @matesZid = ($content =~ /z[0-9]{7}/g);
		foreach my $mateZid (@matesZid){
			sendNotificationWhenZidMentioned($mateZid,"$currentDir/replies/$reply_num/reply.txt");
		}
	}

	print redirect("matelook.cgi?showUserPage=1");

}else{
	die "neither makeComment or makeReply";
}

#print end_html;

