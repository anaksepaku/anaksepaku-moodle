<?php
define('CLI_SCRIPT', true);
require('/var/www/moodle/config.php');
$USER = get_admin();
set_config('themestyleheader', 0, 'theme_academi'); // MOODLEBASED
theme_reset_all_caches();
purge_all_caches();
echo "header style = moodlebased\n";
