<?php
// Dibuat untuk E-Learning Anaksepaku.
namespace local_autoenrol;

defined('MOODLE_INTERNAL') || die();

global $CFG;
require_once($CFG->libdir . '/enrollib.php');

class observer {

    public static function user_loggedin(\core\event\user_loggedin $event): void {
        global $DB;

        $userid = (int) $event->userid;
        if ($userid <= 2) {
            return; // guest & admin
        }

        $courseid = 2; // Bahasa Jepang Bulan Pertama
        $context = \context_course::instance($courseid);

        if (is_enrolled($context, $userid, '', true)) {
            return;
        }

        $instances = $DB->get_records('enrol', [
            'courseid' => $courseid,
            'enrol'    => 'self',
            'status'   => 0,
        ]);

        $method = 'self';
        if (!$instances) {
            $instances = $DB->get_records('enrol', [
                'courseid' => $courseid,
                'enrol'    => 'manual',
                'status'   => 0,
            ]);
            $method = 'manual';
        }
        if (!$instances) {
            return;
        }

        $instance = reset($instances);
        $plugin = enrol_get_plugin($method);
        if ($plugin) {
            $plugin->enrol_user($instance, $userid, 5); // roleid 5 = student
        }
    }
}
