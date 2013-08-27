#!/usr/bin/perl

use CGI;
use CGI::Carp ('fatalsToBrowser');
use strict;

require "settings.conf";
require "common.pl";

our %GLOBAL;

my $q = new CGI;
print $q->header();

my $dbh = connect_database();

my $name   = trim($q->param('name'));
my $mobile = $q->param('mobile');
my $email  = $q->param('email');
$mobile    =~ s/\D//g;
$email     =~ s/\s//g;

if (!$name || (!$mobile && !$email)) {
    print 'Required inputs missing';
    exit;
}

(my $ten_digit = $mobile) =~ s/^0+//;

my ($user_exits) = $dbh->selectrow_array(qq{
    SELECT
        COUNT(*)
    FROM
        users
    WHERE
        (mobile IS NOT NULL AND mobile = ?)
    OR
        (email IS NOT NULL AND email = ?)
}, undef, $ten_digit, $email);

if ($user_exits) {
    print '<font color="red">Already registered.</font>';
}
else {
    my $time = time;
    $time   += 34200; # 34200 seconds = 9.5 hours. Converting server time to Indian time.

    my $localtime = scalar localtime($time);

    my $rows = $dbh->do("INSERT INTO users VALUES (?, ?, ?, ?)", undef, $name, $mobile, $email, $localtime);
    if ($rows == 1) {
        print 'Registered successfully.';
    }
    else {
        print '<font color="red">An error occured.</font>';
    }
}