<?php
define('CLI_SCRIPT', true);
require('/var/www/moodle/config.php');
$USER = get_admin();

$css = <<<'CSS'
.homepage-carousel .slide-text {
    border-radius: 18px !important;
    background: linear-gradient(90deg, rgba(8,30,55,0) 0%, rgba(8,30,55,0.45) 30%, rgba(8,30,55,0.72) 100%) !important;
}
.homepage-carousel .slide-text .heading-content {
    padding: 22px !important;
}
.homepage-carousel .slide-text h1 {
    text-shadow: 0 2px 8px rgba(0,0,0,0.35);
}
CSS;

set_config('customcss', $css, 'theme_academi');
theme_reset_all_caches();
purge_all_caches();
echo "customcss softened\n";
