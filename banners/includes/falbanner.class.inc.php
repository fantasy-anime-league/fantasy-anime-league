<?php

// includes
require_once($_SERVER['DOCUMENT_ROOT'].'/falbanners/includes/faldata.class.inc.php');
require_once($_SERVER['DOCUMENT_ROOT'].'/falbanners/includes/functions.inc.php');

// config
define(FALB_DEFAULTTYPE,1);  // banner to use if none specified
define(FALB_BANNERDIR,'/home/mfalncfm/public_html/falbanners/banners/'); // banner information directory
define(FALB_BANNEREXT,'.ini'); // banner data file extension
define(FALB_BANNERCACHEDIR,'/home/mfalncfm/public_html/falbanners/generated_banners/'); // cache directory for banners
define(FALB_BANNERIMGEXT,'.png'); // banner cache image extension
define(FALB_FONTDIR,'/home/mfalncfm/public_html/falbanners/fonts/');

// the banner class
class FALBanner {
	private $team; // team name (same as user for now)
	private $type; // banner type
	private $fal; // copy of current FAL week data
	private $im;  // banner image
	private $cache; // path to cached image for this week, user, and type
	private $fields; // an array containing the fields accessible in the templates
	
	//////
	
	public function __construct($team,$type,$dir=FAL_DATADIR) {
		// get FAL data
		$this->fal = new FALData($dir);
		//error_log(print_r($this->fal, true));
		error_log("FALData complete", 0);
		// make sure we're in an active round
		
		/*switch ($this->fal->week) {
			case 0: // registration
				$this->display_error('Register today for Fantasy Anime League');
				error_log('Register today for Fantasy Anime League');
				break;
				
			case -1: // disabled or no data
				$this->display_error('Visit the FAL club for ranks and information');
				error_log('Visit the FAL club for ranks and information');
				break;
		}*/
		
		// populate class members
		$this->team = $this->check_team($team);
		error_log(print_r($this->team, true));
		$this->type = $this->check_type($type);
		error_log(print_r($this->type, true));
		
		// populate the template fields
		$this->fields['team'] = $this->team;
		$this->fields['rank'] = $this->fal->teams[$this->team];
		$this->fields['week'] = $this->fal->week;
		$this->fields['ordrank'] = ordinal($this->fal->teams[$this->team]);
		$this->fields['ordweek'] = ordinal($this->fal->week);

		error_log("Pop complete", 0);
		// saves generated image to cache
		
		// username.bannertype.png (overrides image every week)
		$this->cache = FALB_BANNERCACHEDIR . $this->team . '.' . $this->type . FALB_BANNERIMGEXT;
		
		// week.username.bannertype.png (creates new images for every week)
		//$this->cache = FALB_BANNERCACHEDIR . $this->fal->week . '.' . $this->team . '.' . $this->type . FALB_BANNERIMGEXT;
		
		// if cache is fresh, use cached image
		//$this->check_cache();
		
		// otherwise generate new banner
		error_log("constructing", 0);
		$this->generate_banner();
	}
	
	public function display() {
		header("Content-type: image/png");
		imagepng($this->im); // echo image data
		imagepng($this->im,$this->cache); // save a copy to banner cache
	}
	
	// display_error() returns an image with specified $error
	public function display_error($error) {
		$this->im = create_image(350,75);
		
		// draw the error text
		$size = 12;
		$fontpath = realpath('../fonts/');
		putenv('GDFONTPATH='.$fontpath);
		$font = FALB_FONTDIR . 'arialbd.ttf';
		
		imagettftextalign($this->im,$size,0,imagesx($this->im)/2,imagesy($this->im)/2+($size/2),0x222299,$font,$error,'c');
		
		// display the image and quit
		$this->display();
		exit(0);
	}
	
	// check_user() verifies that $team is a valid team name
	public function check_team($team) {
		if ( !$this->fal->isTeam($team) ) {
			$this->display_error('Invalid team name');
		}
		// mal usernames cannot exceed 16 characters and only contain alphanumeric, underscore, or hyphen
		/*if ( preg_match('/^[^a-z0-9_-]$/i',$raw) || strlen($team) > 16) {
			display_error('Invalid MAL user name');
		}*/
		return $team;
	}

	// check_type() verifies that this is an existing banner type
	public function check_type($type) {
		if ( !file_exists(FALB_BANNERDIR . $type . FALB_BANNEREXT) ) $this->display_error('Invalid banner type!');
		return $type;
	}
	
	// check_cache() returns a cached image and stops execution if image exists for this week, user, and type
	private function check_cache() {	
		if ( !( is_writable($this->cache) or is_writable(dirname($this->cache)) and !file_exists($this->cache) ) )
			die("The banner cache is not writable; please change write permissions using FTP.\n<br />\cache = " . realdir($this->cache));
		if ( file_exists($this->cache) ) {
			header("Content-type: image/png");
			echo file_get_contents($this->cache);
			exit(0);
		}
	}
		
	// generate_banner() creates a banner image from template specified by type
	private function generate_banner() {
		// load the background
		$this->im = open_image(FALB_BANNERDIR . $this->type . FALB_BANNERIMGEXT);
		
		// load default text style
		$bs = parse_ini_file(FALB_BANNERDIR . 'default' . FALB_BANNEREXT,true);
		
		// parse the custom banner style
		$bt = parse_ini_file(FALB_BANNERDIR . $this->type . FALB_BANNEREXT,true);
		foreach($bt as $key => $value) {
			// if valid template element, write it to image
			if (is_array($value)) {
				if (isset($this->fields[$key])) {
					// set style with fallback to defaults
					$text  = isset($bt[$key]['text'])  ? $bt[$key]['text']  : $bs['text'];
					$size  = isset($bt[$key]['size'])  ? $bt[$key]['size']  : $bs['size'];
					$angle = isset($bt[$key]['angle']) ? $bt[$key]['angle'] : $bs['angle'];
					$x     = isset($bt[$key]['x'])     ? $bt[$key]['x']     : $bs['x'];
					$y     = isset($bt[$key]['y'])     ? $bt[$key]['y']     : $bs['y'];
					$color = isset($bt[$key]['color']) ? $bt[$key]['color'] : $bs['color'];
					$font  = isset($bt[$key]['font'])  ? $bt[$key]['font']  : $bs['font'];
					$align = isset($bt[$key]['align']) ? $bt[$key]['align'] : $bs['align'];
					// stroke
					$stroke      = isset($bt[$key]['stroke'])      ? $bt[$key]['stroke']      : $bs['stroke'];
					$strokecolor = isset($bt[$key]['strokecolor']) ? $bt[$key]['strokecolor'] : $bs['strokecolor'];
					// glow
					$glow        = isset($bt[$key]['glow'])        ? $bt[$key]['glow']        : $bs['glow'];
					$glowcolor   = isset($bt[$key]['glowcolor'])   ? $bt[$key]['glowcolor']   : $bs['glowcolor'];
					$glowopacity = isset($bt[$key]['glowopacity']) ? $bt[$key]['glowopacity'] : $bs['glowopacity'];
					// fit to width
					$maxwidth = isset($bt[$key]['maxwidth']) ? $bt[$key]['maxwidth'] : $bs['maxwidth'];
					// if smooth is set we'll need to upscale
					$upscale = isset($bt[$key]['smooth']) ? $bt[$key]['smooth'] + 1 : $bs['smooth'] + 1;
					if ($upscale > 1 && !$upscaled) { // upscale only once
						$x *= $upscale; $y *= $upscale; $size *= $upscale; $maxwidth *= $upscale; $glow *= $upscale; $stroke *= $upscale;
						$orig_w = imagesx($this->im); $orig_h = imagesy($this->im);
						$tempim = create_image($upscale*$orig_w,$upscale*$orig_h);
						imagecopyresampled($tempim,$this->im,0,0,0,0,$upscale*$orig_w,$upscale*$orig_h,$orig_w,$orig_h);
						imagedestroy($this->im);
						$this->im = $tempim;
						$upscaled = true;
					}
					
					// substitute values and clean up
					$text        = sprintf($text,$this->fields[$key]);
					$color       = (int) hexdec($color);
					$strokecolor = (int) hexdec($strokecolor);
					$glowcolor   = (int) hexdec($glowcolor);
					$font        = FALB_FONTDIR . $font;
					
					// enforce max width if set
					if($maxwidth) list($text,$size) = textfit($text,$font,$maxwidth,$size,7);
					
					// add glow if applicable
					if($glow) textglowalign($this->im,$size,$angle,$x,$y,$font,$color,$text,$glowcolor,$align,$glow,$glowopacity);
					
					// add stroke if applicable
					if($stroke) imagettfstrokealign($this->im,$size,$angle,$x,$y,$color,$font,$text,$align,$strokecolor,$stroke);
					
					// write the text onto the image
					imagettftextalign($this->im,$size,$angle,$x,$y,$color,$font,$text,$align);
				}
			}
			// otherwise override default style with value
			else {
				$bs[$key] = $value;
			}
			// if we upscaled, we need to put it back to normal size when done
			if ($upscale > 1) {
				$tempim = create_image($orig_w,$orig_h);
				imagecopyresampled($tempim,$this->im,0,0,0,0,$orig_w,$orig_h,imagesx($this->im),imagesy($this->im));
				imagedestroy($this->im);
				$this->im = $tempim;
			}
		}
	}
		
} // end class FALBanner
