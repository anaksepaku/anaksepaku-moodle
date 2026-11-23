<?php
// Dipanggil installer: php set_mail_sender.php <host>
define('CLI_SCRIPT', true);
require('/var/www/moodle/config.php');
require_once($CFG->dirroot . '/user/lib.php');

$name = $argv[1] ?? preg_replace('#^https?://#', '', $CFG->wwwroot);
$name = rtrim($name, '/');
$email = 'noreply@' . $name;

$support = $DB->get_record('user', ['username' => 'support']);
if (!$support) {
    $support = new stdClass();
    $support->username   = 'support';
    $support->firstname  = $name;
    $support->lastname   = '';
    $support->email      = $email;
    $support->auth       = 'nologin';
    $support->confirmed  = 1;
    $support->mnethostid = 1;
    $support->lang       = 'id';
    $support->password   = AUTH_PASSWORD_NOT_CACHED;
    $supportid = \core\user::create_user($support, false, false);
} else {
    $supportid = $support->id;
    $DB->set_field('user', 'firstname', $name, ['id' => $supportid]);
    $DB->set_field('user', 'lastname', '', ['id' => $supportid]);
    $DB->set_field('user', 'email', $email, ['id' => $supportid]);
}

set_config('supportuserid', $supportid);
set_config('supportname', $name);
set_config('emailfromvia', 0);
set_config('supportemail', $email);
set_config('noreplyaddress', $email);

$admin = get_admin();
$DB->set_field('user', 'firstname', $name, ['id' => $admin->id]);
$DB->set_field('user', 'lastname', '', ['id' => $admin->id]);

purge_all_caches();
echo "mail_sender=$name supportid=$supportid\n";
