<?php

// config
define(FAL_DATADIR,'/home/mfalncfm/public_html/falbanners/data/');
define(FAL_DATAPATTERN,'week*.txt');


// the data class
class FALData {

	public $teams; // associative array of team names to rank
	public $week;  // stores the most current week number
	private $datafile; // stores path to current week data file
	
	//////
	
	public function __construct($dir=FAL_DATADIR) {
		// find most recent data file
		//if ( !file_exists($dir) ) display_error('Could not open data directory!');
		$weekfiles = glob(FAL_DATADIR . FAL_DATAPATTERN, GLOB_NOSORT);
		natcasesort($weekfiles);
		if (count($weekfiles) > 0) {
			$this->datafile = array_pop($weekfiles); // only want the most recent
			$this->week = preg_replace('@[^0-9]@','',basename($this->datafile));
			// parse the data
			$this->teams = parse_ini_file($this->datafile,true);
		} else $this->week = -1;
	}

	public function isTeam($team) {
		return array_key_exists($team,$this->teams);
	}
	
	public function getRank($team) {
		return $this->teams[$team];
	}
	
} // end class FALData
