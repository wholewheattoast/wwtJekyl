<?php

/******************************************************************************
 Pepper

 Developer: Maxime Valette
 Plug-in Name: Status Board Helper

 More info at: http://github.com/maximevalette/MintStatusBoardHelper
 ******************************************************************************/

define('MINT_ROOT', str_replace('pepper/maximevalette/statusboard/stats.php', '', __FILE__));
define('MINT', true);

require MINT_ROOT.'app/lib/mint.php';
require MINT_ROOT.'app/lib/pepper.php';
require MINT_ROOT.'config/db.php';

$Mint->loadPepper();

$SBHelper =& $Mint->getPepperByClassName('MV_StatusBoard_Helper');

$debug = isset($_GET['debug']) && !$Mint->paranoid ? true : false;

$SBHelper->verifyKey($_GET['key']);

if (isset($_GET['list'])) {

    $SBHelper->showLinks();

}

foreach ($_GET as $k => $v) {

    if (preg_match('/^visits-(.+)$/', $k, $r)) {

        $SBHelper->showVisits($r[1]);

    }

}