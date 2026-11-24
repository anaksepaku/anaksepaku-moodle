<?php
define('CLI_SCRIPT', true);
require('/var/www/moodle/config.php');
$USER = get_admin();

$quizid = 6;
$quiz = $DB->get_record('quiz', ['id' => $quizid], '*', MUST_EXIST);
$structure = \mod_quiz\quiz_settings::create($quizid)->get_structure();

$filtercondition = [
    'filter' => [
        'category' => [
            'jointype' => 1, // ANY
            'values' => [9, 14], // Latihan Bulan Pertama + 5 Tambahan
            'filteroptions' => ['includesubcategories' => false],
        ],
    ],
    'cat' => '9,46', // kategori 9 berada di context 46
];

$n = 0;
foreach ($structure->get_slots() as $s) {
    if (!empty($s->random)) {
        $structure->update_random_question($s->id, $filtercondition);
        $n++;
    }
}
purge_all_caches();
echo "updated_random_slots=$n\n";
echo "filter=" . json_encode($filtercondition) . "\n";
