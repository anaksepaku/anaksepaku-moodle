<?php
define('CLI_SCRIPT', true);
require('/var/www/moodle/config.php');
$USER = get_admin();

$settings = [
    'phoneno'            => '',
    'emailid'            => '',
    'address'            => '',
    'footnote'           => 'E-learning komunitas Anak Sepaku. Belajar bareng dengan materi swadaya komunitas.',
    'copyright_footer'   => '© 2026 Komunitas Anak Sepaku. Dibangun dengan Moodle.',
    'promotedtitle'      => 'Materi Komunitas',
    'promotedcoursedesc' => 'Kursus dan materi swadaya dari komunitas Anak Sepaku. Belajar bisa dimulai dari siapa saja.',
    'footerbtitle1'      => 'Komunitas',
    'footerbtitle2'      => 'Belajar',
    'footerbtitle3'      => 'Materi',
    'footerbtitle4'      => 'Bantuan',
];

foreach ($settings as $name => $value) {
    set_config($name, $value, 'theme_academi');
}

for ($i = 1; $i <= 4; $i++) {
    set_config('socialmedia' . $i . '_status', 0, 'theme_academi');
}

theme_reset_all_caches();
purge_all_caches();
echo "academi dummy content cleaned\n";
