<?php
define('CLI_SCRIPT', true);
require('/var/www/moodle/config.php');
require_once($CFG->libdir . '/accesslib.php');
$USER = get_admin();

$courseid = 2;
$now = time();
$src = '/var/www/moodle/import-v2';

function add_cm($DB, $courseid, $moduleid, $instanceid, $sectionnum) {
    $now = time();
    $section = $DB->get_record('course_sections', ['course' => $courseid, 'section' => $sectionnum], '*', MUST_EXIST);
    $cm = $DB->get_record('course_modules', ['course' => $courseid, 'module' => $moduleid, 'instance' => $instanceid]);
    if (!$cm) {
        $cmid = $DB->insert_record('course_modules', (object)[
            'course' => $courseid,
            'module' => $moduleid,
            'instance' => $instanceid,
            'section' => $section->id,
            'added' => $now,
            'visible' => 1,
            'visibleoncoursepage' => 1,
            'visibleold' => 1,
        ]);
    } else {
        $cmid = $cm->id;
    }
    $seq = array_filter(explode(',', $section->sequence));
    if (!in_array($cmid, $seq)) {
        $seq[] = $cmid;
        $DB->set_field('course_sections', 'sequence', implode(',', $seq), ['id' => $section->id]);
    }
    return $cmid;
}

// 1. Hapus resource PDF yang bermasalah
$DB->delete_records('files', ['component' => 'mod_resource', 'filearea' => 'content']);
$DB->delete_records('course_modules', ['course' => $courseid, 'module' => 18]);
$DB->delete_records('resource', ['course' => $courseid]);
echo "pdf_resources_removed\n";

// 2. Buat Page berisi materi langsung per sesi
$sessions = [
    1 => ['Materi Minggu 1 — Hiragana', ['01-pengantar-dan-rencana.html','02-hiragana.html','02a-cara-berlatih-menulis-kana.html']],
    2 => ['Materi Minggu 2 — Katakana', ['03-katakana.html']],
    3 => ['Materi Minggu 3 — Kanji & Partikel', ['04-kanji.html','06-partikel.html','08-kata-tanya-dan-penunjuk.html']],
    4 => ['Materi Minggu 4 — Pola Kalimat & Listening', ['05-sapaan-dan-perkenalan.html','07-pola-kalimat.html','09-angka-dan-waktu.html','10-kata-kerja-langkah-demi-langkah.html','11-kata-sifat.html','12-dialog-mini.html']],
    5 => ['Materi Latihan & Sumber Belajar', ['13-sumber-belajar.html']],
];

foreach ($sessions as $num => [$name, $files]) {
    $existing = $DB->get_record_select('page', 'course = ? AND name = ?', [$courseid, $name]);
    if ($existing) {
        echo "exists name=$name\n";
        continue;
    }

    $content = '<h2>' . htmlspecialchars($name, ENT_QUOTES | ENT_HTML5, 'UTF-8') . '</h2>';
    foreach ($files as $file) {
        $raw = file_get_contents($src . '/' . $file);
        preg_match('/<title>(.*?)<\/title>/is', $raw, $tm);
        $title = isset($tm[1]) ? trim(html_entity_decode(strip_tags($tm[1]))) : $file;
        $body = preg_replace('/^.*?<body[^>]*>/is', '', $raw);
        $body = preg_replace('/<\/body>\s*<\/html>\s*$/is', '', $body);
        $content .= '<h3>' . htmlspecialchars($title, ENT_QUOTES | ENT_HTML5, 'UTF-8') . '</h3>' . $body . '<hr />';
    }

    $pageid = $DB->insert_record('page', (object)[
        'course'        => $courseid,
        'name'          => $name,
        'intro'         => 'Materi ditulis langsung di Moodle — tidak perlu PDF.',
        'introformat'   => 1,
        'content'       => $content,
        'contentformat' => 1,
        'display'       => 0,
        'revision'      => 1,
        'timemodified'  => $now,
    ]);
    $cmid = add_cm($DB, $courseid, 15, $pageid, $num);
    echo "added section=$num cmid=$cmid page=$pageid name=$name\n";
}

rebuild_course_cache($courseid, true);
echo "done\n";
