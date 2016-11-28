#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

use DataManipulation;

use File::Path;

if(defined param("directory")){
	rmtree(param("directory"));
}

print redirect("matelook.cgi?showUserPage=1")

