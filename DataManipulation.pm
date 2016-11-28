package DataManipulation;

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

require      Exporter;

our @ISA       = qw(Exporter);
our @EXPORT    = qw($users_dir $suspend_dir returnUserNameWithZid returnUserImgWithZid searchForNameAndPostHtml logoutHtml displayPostWithDir unmateTwoUser checkUsrsMateRelationship sendEmail sendMateRequest makeMateTwoUser createDefaultNPStxt sendNotificationWhenZidMentioned getEmailByZid mateSuggestion);  # Symbols to be exported by default
our @EXPORT_OK = qw($users_dir $suspend_dir returnUserNameWithZid returnUserImgWithZid searchForNameAndPostHtml logoutHtml displayPostWithDir unmateTwoUser checkUsrsMateRelationship sendEmail sendMateRequest makeMateTwoUser createDefaultNPStxt sendNotificationWhenZidMentioned getEmailByZid mateSuggestion);  # Symbols to be exported on request
our $VERSION   = 1.00;         # Version number

#use Image::Thumbnail;


$users_dir = "dataset-medium";
$suspend_dir = "suspend";


sub returnUserNameWithZid{
	my $user_zid = $_[0];
	open F,"<$users_dir/$user_zid/user.txt";
	#print "$user_zid";
	while(my $line = <F>){
		#print "$line";
		if($line =~ /full_name/){
			chomp $line;
			my $name = $line;
			$name =~ s/\s*full_name\s*=\s*//;
			return $name;
		}
	}
	close F;
	return undef;
}

##if jpg file exist and be thumbnailed, return file name , else return 0, stands for do not exist
sub returnUserImgWithZid{
	my $user_zid = $_[0];
	
	foreach my $file (glob "$users_dir/$user_zid/*"){
		#i must match profile\.jpg instead of \.jpg, since there could be two images, profile.jpg and background.jpg
		if($file =~ /profile\.jpg/){
			#my $fileName = $1;
			#my $t = new Image::Thumbnail;
			#$t -> thumbnail(
			#	input  => "$file",
			#	output => "$fileName_Thumbnail\.jpg",
			#	size   => 128,
			#) or die $t -> error;
			#$t ->create or die "Could not create thumbnail.\n";
			return $file;
		}
	}
	#means do not exist the corresponding jpg file, you don't need to print out
	return 0;
}

#return the html code for searching for name and post
#so I can add it to the webpage I wish to have search function
sub searchForNameAndPostHtml{
	return  "<strong>Search:</strong>", "\n",
		"<form action=\"search.cgi\">","\n",
		textfield(-name=>'SearchKey',-size=>100,-maxlength=>100),"\n",
		"<INPUT type=\"submit\" value=\"Search Name\" name=\"SearchName\" method=\"POST\">","\n",
		"<INPUT type=\"submit\" value=\"Search Post\" name=\"SearchPost\" method=\"POST\">","\n",
		"</form>";
}


#return logout html code
sub logoutHtml{
	return "<form action=\"matelook.cgi\">
    		<input type=\"submit\" name=\"logout\"value=\"logout\" />
	     </form>";
}


##display a post with given directory
##assuem dir = $user_dir/$zid/posts/0 , no / in the end.
##integrate comment/reply and delete post functions 
##return content with hyper link embeded
sub displayPostWithDir{
	my $dir = $_[0];
	
	my $zid_For_Delete = $_[1];
	
	my @tempArrayForAnchorTag;

	my $outputString="";

	###this used in javascript, element id
	my $jsId1 = $dir;
	my $jsId2 = $dir;
	$jsId1 =~ s/.*?([0-9]+)$/$1/;
	$jsId2 =~ s/.*?(z[0-9]{7}).*/$1/;
	#print "\$jsId2 :$jsId2","\n";
	$jsId2 =returnUserNameWithZid($jsId2);
	$jsId2 =~ s/\W//g;
	my $jsId = "$jsId1$jsId2";

	#add post content into outputString
	open F,'<',"$dir/post.txt";
	while(my $line = <F>){
		if($line =~ /message/){
			chomp $line;
			$line =~ s/\s*message\s*=\s*//;
			$outputString.="<b>post message:</b><span>$line\n</span>"."<a href=\"#\" onclick=\"document.getElementById(\'hiddenForm$jsId\').style.display = 'block'; return false;\">Make a comment</a><br/>
   <form action=\"makeCommentAndReply.cgi\" id=\"hiddenForm$jsId\" style=\"display: none;\">
      <textarea cols=\"50\" rows=\"10\" name=\"content\"></textarea><br />
      <input type=\"hidden\" name=\"currentDir\" value='\"$dir\"'/>
      <input type=\"hidden\" name=\"makeComment\" value=\"1\" />   
      <input type=\"submit\" value=\"submit Comment\" />
   </form>";
			#last;
		}
		if($line =~ /from=(z[0-9]{7})/i){
			if($zid_For_Delete eq $1){
				push @tempArrayForAnchorTag,"<span><a href=\"deletePost.cgi?directory=$dir\">Delete</a></span><br/>";
			}
		}
	}
	if(@tempArrayForAnchorTag){
		$outputString.= shift @tempArrayForAnchorTag;
	}
	close F;


	#check comments directory exists
	if(-d "$dir/comments"){
		foreach my $underComments (glob "$dir/comments/*"){
			open F,'<',"$underComments/comment.txt";
			##this used in javascript, element id, plus comment id to distinguish from each other
			my $jsCommentId = $underComments;
			$jsCommentId =~ s/.*?([0-9]+)$/$1/;
			#print "\$jsCommentId:$jsCommentId","\n";

			while(my $line = <F>){
				if($line =~ /message/){
					chomp $line;
					$line =~ s/\s*message\s*=\s*//;
					$outputString.="<b> comment message:</b><span>$line\n</span>"."<a href=\"#\" onclick=\"document.getElementById(\'hiddenFormComment$jsId$jsCommentId\').style.display = 'block'; return false;\">Make a Reply</a><br/>
   <form action=\"makeCommentAndReply.cgi\" id=\"hiddenFormComment$jsId$jsCommentId\" style=\"display: none;\">
      <textarea cols=\"50\" rows=\"10\" name=\"content\"></textarea><br />
      <input type=\"hidden\" name=\"currentDir\" value='\"$underComments\"'/>
      <input type=\"hidden\" name=\"makeReply\" value=\"1\" />   
      <input type=\"submit\" value=\"submit Reply\" />
   </form>";
					#last;
				}
				if($line =~ /from=(z[0-9]{7})/i){
					if($zid_For_Delete eq $1){
						push @tempArrayForAnchorTag,"<span><a href=\"deletePost.cgi?directory=$underComments\">Delete</a></span><br/>";
					}
				}
			}
			
			if(@tempArrayForAnchorTag){
				$outputString.= shift @tempArrayForAnchorTag;
			}
			close F;

			if(-d "$underComments/replies"){
				foreach my $underReplies (glob "$underComments/replies/*"){
					open F,'<',"$underReplies/reply.txt";
					while(my $line = <F>){
						if($line =~ /message/){
							chomp $line;
							$line =~ s/\s*message\s*=\s*//;
							$outputString.="<b >reply message:</b><span>$line\n</span><br/>";
							#last;
						}
						if($line =~ /from=(z[0-9]{7})/i){
							if($zid_For_Delete eq $1){
								#$outputString.="<a href=\"deletePost.cgi?directory=$underReplies\"> Delete </a>";
								push @tempArrayForAnchorTag,"<a href=\"deletePost.cgi?directory=$underReplies\">Delete</a><br/>";
							}
						}
					}
					if(@tempArrayForAnchorTag){
						$outputString.= shift @tempArrayForAnchorTag;
					}
					close F;
				}
			}
		}
	}

	return $outputString;
}





sub makeMateTwoUser{
	my ($user1,$user2)=@_;
	
	open F,'<',"$users_dir/$user1/user.txt";
	my @lines = <F>;
	close F;
	
	open F,'>',"$users_dir/$user1/user.txt";
	foreach my $line (@lines){
		if($line =~ /^\s*mates\s*=/){
			chomp $line;
			$line =~ s/\]//;
			$line .= ",$user2]\n";
			print F $line;
		}else{
			print F $line;
		}	
	}
	
	##empty the @lines array
	@lines=();
	
	open F,'<',"$users_dir/$user2/user.txt";
	@lines = <F>;
	close F;
	
	open F,'>',"$users_dir/$user2/user.txt";
	foreach my $line (@lines){
		if($line =~ /^\s*mates\s*=/){
			chomp $line;
			$line =~ s/\]//;
			$line .= ",$user1]\n";
			print F $line;
		}else{
			print F $line;
		}	
	}
	
	return 1;
}

sub unmateTwoUser{
	my ($user1,$user2)=@_;
	
	open F,'<',"$users_dir/$user1/user.txt";
	my @lines = <F>;
	close F;
	
	open F,'>',"$users_dir/$user1/user.txt";
	foreach my $line (@lines){
		if($line =~ /^\s*mates\s*=/){
			#if there is a preceding comma(,), should remove the comma as well
			$line =~ s/(,\Q$user2\E)|(\Q$user2\E)//;
			print F $line;
		}else{
			print F $line;
		}	
	}
	
	##empty the @lines array
	@lines=();
	
	open F,'<',"$users_dir/$user2/user.txt";
	@lines = <F>;
	close F;
	
	open F,'>',"$users_dir/$user2/user.txt";
	foreach my $line (@lines){
		if($line =~ /^\s*mates\s*=/){
			$line =~ s/(,\Q$user1\E)|(\Q$user1\E)//;
			print F $line;
		}else{
			print F $line;
		}	
	}
	
	return 1;
}

sub checkUsrsMateRelationship{
	my ($user1, $user2)=@_;
	
	open F,'<',"$users_dir/$user1/user.txt";
	while(my $line = <F>){
		if($line =~ /^\s*mates\s*=/ && $line =~ /\Q$user2\E/){
			return 1;
		}
	}
	
	return 0;	
}

sub sendEmail{
	my ($to,$from,$subject,$message)=@_;
	
	open(MAIL, "|/usr/sbin/sendmail -t");
	 
	# Email Header
	print MAIL "To: $to\n";
	print MAIL "From: $from\n";
	print MAIL "Subject: $subject\n\n";
	print MAIL "Content-type: text/html; charset=UTF-8\n\n";
	print MAIL "
	";
	# Email Body
	print MAIL "\n".$message;

	close(MAIL);
}

sub sendMateRequest{
	#$to and $from are zid.
	my ($to,$from,$url) = @_;
	$url =~ s/^(.*)\/.*$/$1/;
	#http://www.cse.unsw.edu.au/~z5089812/ass2/matelook.cgi
	my $sendMessageHtml .= "<html><title><Mate Request from $from</title><body>";
	$sendMessageHtml .= "<p>Mate Request from $from</p>";
	$sendMessageHtml .= "<a href=\"$url/matelook.cgi?acceptMateRequest=1&to=$to&from=$from\">accept</a>";
	$sendMessageHtml .= "<a href=\"$url/matelook.cgi?declineMateRequest=1&to=$to&from=$from\">decline</a>";
	$sendMessageHtml .= "</body></html>";
	
	my $toEmail="";
	open F,'<',"$users_dir/$to/user.txt";
	while(my $line = <F>){
		if($line =~ /^\s*email\s*=(.*)\n*/){
			$toEmail = $1;
			last;
		}
	}
	close F;
	
	sendEmail($toEmail,'z5089812@ad.unsw.edu.au',"Mate Request from $from",$sendMessageHtml);
	
	open 'F','>',"$users_dir/$zid_cookie_value/notificationAndPrivacySetting.txt";
	while(my $line = <F>){
		if($line =~ /notified when get a mate request=(\d)/){
			if($1){
				sendEmail($toEmail,'z5089812@ad.unsw.edu.au',"Mate Request from $from","It's a nofication, you can choose to turn it off in nofication and privacy toggle");
			}else{
				next;
			}
			last;
		}
	}
	close F;
}

##create default notificationAndPrivacy.txt
sub createDefaultNPStxt{
	my $zid=$_[0];

	open F,'>',"$users_dir/$zid/notificationAndPrivacySetting.txt";
	## 1 means get notifcation, 0 means no
	## default is get all the notications
	print F "notified when zid is mentioned=1\n";
	print F "notified when get a mate request=1\n";
	## 1 means open to public, 0 means open only to mates
	## default set to 1
	## doesn't cover all the field, only fields bellow.
	print F "profile=1\n";
	print F "home_suburb=1\n";
	print F "courses=1\n";
	print F "program=1\n";
	print F "birthday=1\n";
	print F "email=1\n";
	
	close F;
}

sub getEmailByZid{
	my $zid = $_[0];
	my $toEmail="";
	open F,'<',"$users_dir/$zid/user.txt";
	while(my $line = <F>){
		if($line =~ /^\s*email\s*=(.*)\n*/){
			$toEmail = $1;
			return $toEmail;
			last;
		}
	}
	close F;
	return undef;
}

sub sendNotificationWhenZidMentioned{
	my $zid = $_[0];
	my $dir = $_[1];
	
	##does not exist then create a default one
	if(! -e "$users_dir/$zid/notificationAndPrivacySetting.txt"){
		createDefaultNPStxt($zid);
	}
		
	open F,'<',"$users_dir/$zid/notificationAndPrivacySetting.txt";
	while(my $line = <F>){
		if($line=~ /notified when zid is mentioned=(\d)/){
			if($1){
				sendEmail(getEmailByZid($zid),'z5089812@ad.unsw.edu.au',"your zid is mentiond","you are mentioned in $dir");
			}
		}
	}
	close F;
}


sub mateSuggestion{
	my $zid = $_[0];
	
	my %mateSuggestionMark=();
	
	##find his mates' mates
	##give higher weights to friend's friend when doing suggestion
	##increase by 3 each time
	open F,"<$users_dir/$zid/user.txt";
	my @matesZid;
	while(my $line = <F>){
		if($line =~ /^\s*mates/){
			@matesZid = ($line =~ /z[0-9]{7}/g);
			foreach my $mateZid (@matesZid){
				open F2,"<","$users_dir/$mateZid/user.txt";
				while(my $tempLine = <F2>){
					if($tempLine =~ /^\s*mates/){
						@matesmatesZid = ($tempLine =~ /z[0-9]{7}/g);
						foreach my $matemateZid (@matesmatesZid){
							my @tempCheckZidIn = grep {$_ =~ /$matemateZid/} @matesZid;
							if(! @tempCheckZidIn && $matemateZid ne $zid){
								##they not friend and not himself, it could be someone may be suggested
								if($mateSuggestionMark{$matemateZid}){
									$mateSuggestionMark{$matemateZid}+=3;
								}else{
									$mateSuggestionMark{$matemateZid}=3;
								}
							}
						}
						last;
					}
				}
				close F2;
			}
			last;
		}
	}
	
	close F;
	
	##check people in %mateSuggestionMark, the courses they have.
	open F,"<$users_dir/$zid/user.txt";
	my %courses;
	while(my $line = <F>){
		if($line =~ /^\s*courses/){
			my @coursesTaken = ($line =~ /[0-9]{4} \w\d [\w]{4}[\d]{4}/g);
			foreach my $course (@coursesTaken){
				$course = lc $course;
				$courses{$course}=1;
			}
			last;
		}
	}
	close F;
	
	for my $mate (keys %mateSuggestionMark){
		open F,"<$users_dir/$mate/user.txt";
		while(my $line = <F>){
			if($line =~ /^\s*courses/){
				my @coursesTaken = ($line =~ /[0-9]{4} \w\d [\w]{4}[\d]{4}/g);
				foreach my $course (@coursesTaken){
					$course = lc $course;
					if($courses{$course}){
						$mateSuggestionMark{$mate}+=2;
					}	
				}
				last;
			}
		}
		close F;
	}
	
	my @outputZid;
	foreach my $zid (sort { $mateSuggestionMark{$a} <=> $mateSuggestionMark{$b} } keys %mateSuggestionMark) {
		push @outputZid,$zid;
	}
	
	return \@outputZid;
}













