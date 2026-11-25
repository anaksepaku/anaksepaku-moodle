<?php
define('CLI_SCRIPT', true);
require('/var/www/moodle/config.php');
$USER = get_admin();

set_config('theme', 'academi');

$fs = get_file_storage();
$ctx = context_system::instance();
$dir = '/var/www/moodle/brand/';

$slides = [
    1 => ['Belajar Bareng', 'Ilmu dibagikan, bukan ditimbun. Materi umum dan swadaya dari komunitas Anak Sepaku.'],
    2 => ['Swadaya Komunitas', 'Dari komunitas, untuk komunitas. Belajar bisa dimulai dari siapa saja, di mana saja.'],
    3 => ['Akses Terbuka', 'Moodle untuk belajar bersama. Kursus, latihan, dan materi bisa diakses kapan saja.'],
];

set_config('toggleslideshow', 1, 'theme_academi');
set_config('autoslideshow', 1, 'theme_academi');
set_config('numberofslides', 3, 'theme_academi');
set_config('slideinterval', 5500, 'theme_academi');
set_config('slideOverlay', '0.45', 'theme_academi');

foreach ($slides as $i => [$caption, $desc]) {
    $area = 'slide' . $i . 'image';
    $filename = 'slide' . $i . '.png';
    if (!file_exists($dir . $filename)) {
        throw new moodle_exception('missingfile', 'error', '', $filename);
    }
    $fs->delete_area_files($ctx->id, 'theme_academi', $area);
    $info = [
        'contextid'    => $ctx->id,
        'component'    => 'theme_academi',
        'filearea'     => $area,
        'itemid'       => 0,
        'filepath'     => '/',
        'filename'     => $filename,
        'userid'       => 2,
        'timecreated'  => time(),
        'timemodified' => time(),
    ];
    $fs->create_file_from_pathname($info, $dir . $filename);
    set_config($area, '/' . $filename, 'theme_academi');
    set_config('slide' . $i . 'status', 1, 'theme_academi');
    set_config('slide' . $i . 'contentstatus', 1, 'theme_academi');
    set_config('slide' . $i . 'caption', $caption, 'theme_academi');
    set_config('slide' . $i . 'desc', $desc, 'theme_academi');
    set_config('slide' . $i . 'btntext', 'Lihat Kursus', 'theme_academi');
    set_config('slide' . $i . 'btnurl', 'https://elearning.anaksepaku.my.id/course/index.php', 'theme_academi');
    echo "slide$i configured\n";
}

theme_reset_all_caches();
purge_all_caches();
echo 'theme=academi, caches purged\n';
