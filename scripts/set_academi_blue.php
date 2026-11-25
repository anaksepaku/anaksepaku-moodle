<?php
define('CLI_SCRIPT', true);
require('/var/www/moodle/config.php');
$USER = get_admin();

set_config('primarycolor', '#1269B2', 'theme_academi');
set_config('secondarycolor', '#0E82BE', 'theme_academi');

theme_reset_all_caches();
purge_all_caches();
echo "theme colors set to blue\n";
