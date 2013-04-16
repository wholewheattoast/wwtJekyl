<?php

/******************************************************************************
Pepper

Developer: Maxime Valette
Plug-in Name: Status Board Helper

More info at: http://github.com/maximevalette/MintStatusBoardHelper
 ******************************************************************************/

if (!defined('MINT'))
{
    header('Location: /');
    exit();
};

$installPepper = 'MV_StatusBoard_Helper';

class MV_StatusBoard_Helper extends Pepper
{

    public $version = 102;

    public $info = array(
        'pepperName'	=> 'Status Board Helper',
        'pepperUrl'		=> 'http://github.com/maximevalette/MintStatusBoardHelper',
        'pepperDesc'	=> 'Helps Status Board work with Mint.',
        'developerName'	=> 'Maxime Valette',
        'developerUrl'	=> 'http://www.maximevalette.com'
    );

    public $panes = array();
    public $prefs = array('key' => '000000');
    public $data = array();
    public $manifest = array();

    /**
     * Update
     */
    public function update()
    {

        if ($this->Mint->version < 200) {

            $this->Mint->logError('This version of Status Board Helper requires Mint v2.00.', 2);

        }

    }

    /**
     * Is compatible
     *
     * @return array
     */
    public function isCompatible()
    {

        if ($this->Mint->version < 200) {

            return array('isCompatible' => false, 'explanation' => '<p>This Pepper requires Mint v2.00.</p>');

        } else {

            return array('isCompatible' => true);

        }

    }

    /**
     * Preferences
     *
     * @return mixed
     */
    public function onDisplayPreferences()
    {

        $mintUrl = $this->curServerURL() . $this->Mint->cfg['installDir'];
        $pepperUrl = $mintUrl . '/pepper/maximevalette/statusboard/stats.php?key=' . $this->prefs['key'];

        $html = '';

        $html .= '<table>';

        $html .= '<tr><th scope="row">Key</th><td>'.$this->prefs['key'].'</td></tr>';

        $html .= '<tr><th scope="row">&nbsp;</th><td><a href="'.$mintUrl.'?custom&sb_keygen">Generate a new key</a></td></tr>';

        $html .= '<tr><th scope="row">&nbsp;</th><td><a href="'.$pepperUrl.'&list">See the list of available URLs for Status Board</a></td></tr>';

        $html .= '</table>';

        $preferences['Status Board URLs'] = $html;

        $html = '';
        $html .= '<table>';

        $html .= '<tr><th scope="row">Past hour visits</th><td><a href="panicboard://?url='.urlencode($pepperUrl . '&visits-hour').'&panel=graph
&sourceDisplayName=Mint">Click this link</a></td></tr>';

        $html .= '<tr><th scope="row">Past day visits</th><td><a href="panicboard://?url='.urlencode($pepperUrl . '&visits-day').'&panel=graph
&sourceDisplayName=Mint">Click this link</a></td></tr>';

        $html .= '<tr><th scope="row">Past week visits</th><td><a href="panicboard://?url='.urlencode($pepperUrl . '&visits-week').'&panel=graph
&sourceDisplayName=Mint">Click this link</a></td></tr>';

        $html .= '<tr><th scope="row">Past month visits</th><td><a href="panicboard://?url='.urlencode($pepperUrl . '&visits-month').'&panel=graph
&sourceDisplayName=Mint">Click this link</a></td></tr>';

        $html .= '</table>';

        $preferences['Direct links'] = $html;

        return $preferences;

    }

    /**
     * Custom
     */
    public function onCustom()
    {

        if (isset($_GET['sb_keygen'])) {

            $this->prefs['key']	= rand(100000, 999999);

        }

        header('Location: '.$this->Mint->cfg['installDir'].'?preferences');

    }

    /**
     * Show stats
     *
     * @param int $timespan
     */
    public function showVisits($timespan)
    {

        $json = array();
        $visits = $this->Mint->data[0]['visits'];

        $index = 1;
        $display = 'Past hour';
        $format = 'ga';

        switch ($timespan) {

            case 'hour':

                $index = 1;
                $display = 'Past hour';
                $format = 'ga';
                break;

            case 'day':

                $index = 2;
                $display = 'Past day';
                $format = 'D j';
                break;

            case 'week':

                $index = 3;
                $display = 'Past week';
                $format = 'M j';
                break;

            case 'month':

                $index = 4;
                $display = 'Past month';
                $format = 'M ’y';
                break;

        }

        header('Content-type: application/json');

        $totals = array();
        $uniques = array();

        foreach ($visits[$index] as $timestamp => $data) {

            if ($timespan == 'week') {
                $title = $this->Mint->formatDateRelative($timestamp, "week");
            } else {
                $title = $this->Mint->offsetDate($format, $timestamp);
            }

            $totals[] = array(
                'title' => $title,
                'value' => (int) $data['total']
            );

            $uniques[] = array(
                'title' => $title,
                'value' => (int) $data['unique']
            );

            $json['graph']['datasequences'] = array();

        }

        $json['graph'] = array(
            'title' => $display . ' visits on ' . $this->Mint->cfg['siteDisplay'],
            'total' => true,
            'datasequences' => array(
                array(
                    'title' => 'Total',
                    'datapoints' => $totals
                ),
                array(
                    'title' => 'Unique',
                    'datapoints' => $uniques
                )
            )
        );

        echo json_encode($json);

    }

    /**
     * Return current server's URL
     *
     * @return string
     */
    public function curServerURL()
    {

        $pageURL = 'http';

        if ($_SERVER["HTTPS"] == "on") {
            $pageURL .= "s";
        }

        $pageURL .= "://";

        if ($_SERVER["SERVER_PORT"] != "80") {

            $pageURL .= $_SERVER["SERVER_NAME"].":".$_SERVER["SERVER_PORT"];

        } else {

            $pageURL .= $_SERVER["SERVER_NAME"];

        }

        return $pageURL;

    }

    /**
     * Verify key
     *
     * @param string $key
     */
    public function verifyKey($key)
    {

        if (urldecode($key) != $this->prefs['key']) {

            die('Wrong key.');

        }

    }

    /**
     * Show links
     */
    public function showLinks()
    {

        header('Content-type: text/plain');

        $mintUrl = $this->curServerURL() . $this->Mint->cfg['installDir'];
        $pepperUrl = $mintUrl . '/pepper/maximevalette/statusboard/stats.php?key=' . $this->prefs['key'];

        echo 'Here are all the available URLs for your Status Board app.' . PHP_EOL . PHP_EOL;

        echo '## VISITS' . PHP_EOL . PHP_EOL;
        echo 'Past hour: ' . $pepperUrl . '&visits-hour' . PHP_EOL;
        echo 'Past day: ' . $pepperUrl . '&visits-day' . PHP_EOL;
        echo 'Past week: ' . $pepperUrl . '&visits-week' . PHP_EOL;
        echo 'Past month: ' . $pepperUrl . '&visits-month' . PHP_EOL;

    }

}
