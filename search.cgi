#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

use DataManipulation;

use List::MoreUtils qw(uniq);

$key = param("SearchKey") or die "no input keyword";


print header(-charset => "utf-8"),start_html(-title => 'search');

print h2("Search Result");

print logoutHtml();
print "<br/>";

print "<form action=\"matelook.cgi?showUserPage=1\">",
    	"<input type='submit' action = \"matelook.cgi?showUserPage=1\" value=\"Go Back To My Page\" name=\"showUserPage\">",
      "</form>";
print "<br/>";


print searchForNameAndPostHtml();


if (defined param("SearchName")){
	foreach my $tempZid (glob "$users_dir/*"){
		$tempZid =~ s/\Q$users_dir\E//;
		$tempZid =~ s/\///;
		my $tempName = returnUserNameWithZid($tempZid);
		if($tempName =~ /\Q$key\E/){
			print "<a href=\"matelook.cgi?showUserPage=1&userZid=$tempZid\">$tempName</a>";
			my $tnjpgfile = returnUserImgWithZid($tempZid);
			if($tnjpgfile){
				print "<a href=\"matelook.cgi?showUserPage=1&userZid=$tempZid\"><img src=\"$tnjpgfile\" alt=\"go to $tempZid \" width=\"50\" height=\"30\"></a>"; 
			}
			print "<br/>","\n";
		}
	}
}elsif (defined param("SearchPost")){
	my $string="";
	my $tempZid="";
	my $tempPost="";
	my $tempComment="";
	my $tempReply="";
	my $outputString="";
	
	##for pagination
	my $display_post_num=8;
	my $display_stop_num;
	if(defined param("pageNum")){
		$display_stop_num = scalar(param("pageNum"))*8;
	}else{
		$display_stop_num = 8;
	}
	my $display_start_num = $display_stop_num-$display_post_num;
	my $post_counter=0;
	
	foreach $tempZid (glob "$users_dir/*"){
		if(-d "$tempZid/posts"){
			foreach $tempPost (glob "$tempZid/posts/*"){
				open F,'<',"$tempPost/post.txt";
				while(my $line = <F>){
					if($line =~ /message/){
						chomp $line;
						$line =~ s/\s*message\s*=\s*//;
						$string.=$line."    ";
					}
				}	
				close F;
				if(-d "$tempPost/comments"){
					foreach $tempComment (glob "$tempPost/comments/*"){
						open F,'<',"$tempComment/comment.txt";
						while(my $line = <F>){
							if($line =~ /message/){
								chomp $line;
								$line =~ s/\s*message\s*=\s*//;
								$string.=$line."    ";
							}
						}
						close F;
						if(-d "$tempComment/replies"){
							foreach $tempReply (glob "$tempComment/replies/*"){
								open F,'<',"$tempReply/reply.txt";
								while(my $line = <F>){
									if($line =~ /message/){
										chomp $line;
										$line =~ s/\s*message\s*=\s*//;
										$string.=$line."    ";
									}
								}
								close F;
							}
						}
					}
				}
				#print "$tempPost","\n";
				if($string =~ /\Q$key\E/){
					if($post_counter >= $display_start_num && $post_counter<$display_stop_num){
						$outputString .= "<div style=\"background:#F9EECF;border:10px splash black;text-align:left\">".displayPostWithDir($tempPost)."</div>", "\n";
					}
				}
				$post_counter++;
				$string="";
			}
		}			
	}
	
	##process the outputString, change znumber , display links.
	##eliminate the case, /z5089812/ as a directory in html, as support info transmit to server
	my @zidsInOutputPosts = ($outputString =~ /[^\/]z[0-9]{7}/g);
	my @uniqZidsInOutputPosts = uniq @zidsInOutputPosts;

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
		$outputString =~ s/\Q$tempZidWithPreceeding\E/$substituteString/eg;
	}

	#display hyper link properly
	if($outputString =~ /(https)|(http):\/\//){
		$outputString =~ s/(.*?)(http[^ ,]*)(.*)/$1 \<a href=\"$2\"\>$2\<\/a\> $3/g;
	}
	
	print $outputString;
	
	##display the page numbers
	$outputPageNums="Pages:";
	for(my $i=1; $i<=($post_counter/$display_post_num + 1);$i++){
		$outputPageNums .= "<a href=\"search.cgi?pageNum=$i&SearchKey=$key&SearchPost=1\" style=\"border:10px; border:solid;\">$i</a>  ";
	}
	print $outputPageNums;
	
}else{
	die "neither search Post or search Name";
}

print end_html;

