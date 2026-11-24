<?php
define('CLI_SCRIPT', true);
require('/var/www/moodle/config.php');
$USER = get_admin();

$dir = '/var/www/moodle/brand/';
$fs = get_file_storage();
$ctx = context_system::instance();

// core_admin_pluginfile() membaca file dari itemid=0, filepath='/'.
// theme revision hanya dipakai sebagai argumen URL untuk cache-busting.
$map = [
    'logo'        => ['moodle-logo.png', 'logo.png'],
    'logocompact' => ['moodle-logo-compact.png', 'logocompact.png'],
    'favicon'     => ['favicon.png', 'favicon.png'],
];

foreach ($map as $area => [$local, $stored]) {
    if (!file_exists($dir . $local)) {
        throw new moodle_exception('missingfile', 'error', '', $local);
    }
    $fs->delete_area_files($ctx->id, 'core_admin', $area);
    $info = [
        'contextid'    => $ctx->id,
        'component'    => 'core_admin',
        'filearea'     => $area,
        'itemid'       => 0,
        'filepath'     => '/',
        'filename'     => $stored,
        'userid'       => 2,
        'timecreated'  => time(),
        'timemodified' => time(),
    ];
    $fs->create_file_from_pathname($info, $dir . $local);
    set_config($area, '/' . $stored, 'core_admin');
    echo "$area -> /$stored itemid=0 (" . filesize($dir . $local) . " bytes)\n";
}

theme_reset_all_caches();
echo 'theme_revision=' . theme_get_revision() . "\n";
