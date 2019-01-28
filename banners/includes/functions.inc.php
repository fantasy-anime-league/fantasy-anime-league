<?php

// ordinal() returns number $num with its ordinal suffix
function ordinal($num) {
  $sfx = array('th','st','nd','rd','th','th','th','th','th','th');
  if (($num / 10) % 10 == 1) return $num . 'th';
  else return $num . $sfx[$num % 10];
}

// textlimit($string, $length) takes any $string you pass it and returns it shortened to $length characters (use it to limit printed string length)
function textlimit($string, $length=25) {
	return ( strlen(trim($string)) > $length ? trim( substr(trim($string),0,$length-3) )."..." : $string );
}

// textlimitpx($string, $pixels, $font, $size) returns the shortened $string that fits within exactly $pixels width horizontally when using $font and $size
function textlimitpx($string, $pixels, $font, $size) {
	for($k = strlen(trim($string)); $k > 0; $k--) {	if (textwidth(textlimit($string,$k), $font, $size) <= $pixels) break;	}
	return textlimit($string,$k);
}

// textwidth() returns the pixel width of the horizontal text with those parameters
function textwidth($string, $font, $size) {
	$box = imagettfbbox($size,0,$font,$string);
	return $box[2] - $box[0];
}

// textheight() find the pixel height of the horizontal text with those parameters
function textheight($string,$font,$size) {
		$box = imagettfbbox($size,0,$font,$string);
		return $box[1] - $box[5];
}

// textfit() finds the text size less than $maxsize and greater than $minsize such that the text is
//  no longer than $maxwidth pixels wide, trimming and returning text if it hits the minimum size
function textfit($text,$font,$maxwidth,$maxsize=40,$minsize=7) {
	// find the largest font size that will fit in the bounds, or trim if it hits the minimum
	for ($size = $maxsize; $size > $minsize && textwidth($text,$font,$size) > $maxwidth; $size--) {
		if ($size == $minsize+1) $text = textlimitpx($text,$maxwidth,$font,$size-1);
	}
	return array($text,$size);
}

// overlay_image($baseimage,$overlaypath,$x,$y) opens the image at $imagepath and overlays it onto $sigimage at position ($x, $y)
// most image types should work, but 24-bit/true color PNG is recommended if you need transparency
function overlay_image($overlaypath,$x=0,$y=0) {
	global $sigimage;
	$overlay = is_string($overlaypath)?open_image($overlaypath):$overlaypath; // open, or assume opened if non-string
	imagecopy($sigimage, $overlay, $x, $y, 0, 0, imagesx($overlay), imagesy($overlay)); // overlay onto our base image
	@imagedestroy($overlay); // clean up memory, since we don't need the overlay image anymore
}

// open_image($path) will load an image into memory so we can work with it, and die with an error if we fail
function open_image($path) {
	$image = @imagecreatefromstring(file_get_contents($path));
	if (!$image) die("could not open image ($path) make sure it exists");
	imagealphablending($image,true); imagesavealpha($image,true); // preserve transparency
	return $image;
}

// imagettftextalign() is basically a wrapper for imagettftext() to add the ability to center/right-align text to a point
// the $align argument can be 'c' for center, 'r' for right align, or 'l' for left align (default)
function imagettftextalign(&$img,$size,$angle,$x,$y,$c,$font,$string,$align='l') {
	$box = imagettfbbox($size,$angle,$font,$string);
	$w = $box[2] - $box[0];
	$h = $box[3] - $box[1];
	switch (strtolower($align)) {
		case 'r': $x -= $w; $y -= $h; break;
		case 'c': $x -= $w/2; $y -= $h/2; break;
	}
	imagettftext($img,$size,$angle,$x,$y,$c,$font,$string);
}

// create_image() creates a transparent image of the specified width and height
function create_image($width,$height) {
	$im = imagecreatetruecolor($width,$height);
	imagealphablending($im,false);
	imagefilledrectangle($im,0,0,imagesx($im)-1,imagesy($im)-1,0x7fffffff); // transparent white
	imagealphablending($im,true); imagesavealpha($im,true);
	return $im;
}

// imagettfstroke() draws the $text with the specified $font and $textcolor, with an added stroke of $strokecolor and $radius
function imagettfstroke(&$image, $size, $angle, $x, $y, $textcolor, $fontfile, $text, $strokecolor, $radius) {
	$radius = abs(round($radius));
	if($radius>0) {
		for($i = -$radius; $i <= $radius; $i++)
			for($j = -$radius; $j <= $radius; $j++)
				if(sqrt($i*$i+$j*$j)<=$radius) imagettftext($image, $size, $angle, $x+$i, $y+$j, $strokecolor, $fontfile, $text);
	}
	return imagettftext($image, $size, $angle, $x, $y, $textcolor, $fontfile, $text);
}

// imagettfstrokealign() is the same as imagettfstroke(), but with alignment to a point
function imagettfstrokealign(&$image, $size, $angle, $x, $y, $textcolor, $fontfile, $text, $align, $strokecolor, $radius) {
	$radius = abs(round($radius));
	if($radius>0) {
		for($i = -$radius; $i <= $radius; $i++)
			for($j = -$radius; $j <= $radius; $j++)
				if(sqrt($i*$i+$j*$j)<=$radius) imagettftextalign($image, $size, $angle, $x+$i, $y+$j, $strokecolor, $fontfile, $text, $align);
	}
	return imagettftextalign($image, $size, $angle, $x, $y, $textcolor, $fontfile, $text, $align);
}

// textglowalign() renders glowing text onto $im with the specified attributes and alignment
function textglowalign(&$im,$size,$angle,$x,$y,$font,$color,$text,$glowcolor,$align='l',$radius=3,$glowopacity=100) {
	$box = imagettfbbox($size,$angle,$font,$text);
	$w = $box[2] - $box[0];
	$h = $box[3] - $box[1];
	switch (strtolower($align)) {
		case 'r': $x -= $w; $y -= $h; break;
		case 'c': $x -= $w/2; $y -= $h/2; break;
	}
	
	textglow($im,$size,$angle,$x,$y,$font,$color,$text,$glowcolor,$radius,$glowopacity);
}

// textglow() renders glowing text onto $im with the specified attributes
function textglow( &$im, $size, $angle, $x, $y, $font, $color, $text, $glowcolor, $radius, $glowopacity=100 ) {
	$radius = round($radius);
	$glowopacity = max(0,min(100,$glowopacity));
	if( !imageistruecolor($im) ) return;
	
	//$box = boundingbox($size,$angle,$x,$y,$font,$text);
	// ...
	
	if($radius > 0 && $glowopacity > 0) {
		$w = imagesx($im);
		$h = imagesy($im);
		
		// create blank image
		$tmpim = imagecreatetruecolor($w+2*$radius,$h+2*$radius); // edges cropped later
		$trans = ($glowcolor & 0xFFFFFF) | 127 << 24; // same rgb with 127 alpha
		imagesavealpha($tmpim,true);imagealphablending($tmpim,false);
		imagefilledrectangle($tmpim,0,0,$w+2*$radius,$h+2*$radius,$trans);
		imagealphablending($tmpim, true);
		
		// imagettftext($tmpim,$size,$angle,$x+$radius,$y+$radius,$glowcolor,$font,$text);
		
		// box blur approximates gaussian within 3% after three iterations
		$subrad = $radius/3.0;
		$rads = array(floor($subrad),round($subrad),ceil($subrad)); // sum of these is equal to $radius
		$glowcolor = ($glowcolor & 0xFFFFFF) | round(127-127*($glowopacity/100)) << 24;
		for($i = 0; $i < count($rads); $i++) {
			imagettftext($tmpim,$size,$angle,$x+$radius,$y+$radius,$glowcolor,$font,$text); // XXX closer to ps glow
			bluralpha($tmpim,$rads[$i]);
		}

		// mask off inside text (if inside text has alpha)
		if ( (($color & 0x7F000000) >> 24) > 0 ) {
			imagesavealpha($tmpim, false);
			imagettftext($tmpim,$size,$angle,$x+$radius,$y+$radius,$trans,$font,$text);
			imagesavealpha($tmpim,true);
		}
		
		imagesavealpha($im,true); imagealphablending($im,true);
		imagecopy($im,$tmpim,0,0,$radius,$radius,$w,$h);
	}
	
	// draw the inside text
	imagettftext($im,$size,$angle,$x,$y,$color,$font,$text);
	
}


// box blurs the alpha channel of a true color image $im with blur radius of $radius
function bluralpha( &$im, $radius ) {
	if(!$im or $radius<=0) return false;
	$radius = (int)round($radius);
	
	$width = imagesx($im);
	$height = imagesy($im);
	
	$copy = imagecreatetruecolor($height,$width); // transposed first pass
	imagesavealpha($copy,true); imagealphablending($copy,false);
	
	imagesavealpha($im,true); imagealphablending($im,false);
	
	// blur alpha horizontal from original into transpose
	for ($y = 0; $y < $height; $y++) {
		$total = 0;
		
		// average entire window for first pixel
		for ($kx = -$radius; $kx <= $radius; $kx++) {
			$total += (imagecolorat($im,$kx,$y) & 0x7F000000) >> 24; // tally alpha value
		}
		// set 0,y
		$rgb = imagecolorat($im,0,$y) & 0xFFFFFF; // rgb part
		$newalpha = $total / (($radius << 1) + 1); // tot / (rad*2 + 1)
		imagesetpixel($copy,$y,0, $newalpha << 24 | $rgb );

		// for other pixels in row just update window total
		for ($x = 1; $x < $width; $x++) {
			$total -= (imagecolorat($im,$x - $radius - 1, $y) & 0x7F000000) >> 24; // subtract pixel leaving window
			$total += (imagecolorat($im,$x + $radius, $y) & 0x7F000000) >> 24; // add pixel entering window
			// set x,y
			$rgb = imagecolorat($im,$x,$y) & 0xFFFFFF; // rgb part
			$newalpha = $total / (($radius << 1) + 1); // tot / (rad*2 + 1)
			imagesetpixel($copy,$y,$x, $newalpha << 24 | $rgb );
		}
	}
	
	// blur alpha horizontal from transpose back to original
	for ($y = 0; $y < $width; $y++) {
		$total = 0;
		
		// average entire window for first pixel
		for ($kx = -$radius; $kx <= $radius; $kx++) {
			$total += (imagecolorat($copy,$kx,$y) & 0x7F000000) >> 24; // tally alpha value
		}
		// set 0,y
		$rgb = imagecolorat($copy,0,$y) & 0xFFFFFF; // rgb part
		$newalpha = $total / (($radius << 1) + 1); // tot / (rad*2 + 1)
		imagesetpixel($im,$y,0, $newalpha << 24 | $rgb );

		// for other pixels in row just update window total
		for ($x = 1; $x < $height; $x++) {
			$total -= (imagecolorat($copy,$x - $radius - 1, $y) & 0x7F000000) >> 24; // subtract pixel leaving window
			$total += (imagecolorat($copy,$x + $radius, $y) & 0x7F000000) >> 24; // add pixel entering window
			// set x,y
			$rgb = imagecolorat($copy,$x,$y) & 0xFFFFFF; // rgb part
			$newalpha = $total / (($radius << 1) + 1); // tot / (rad*2 + 1)
			imagesetpixel($im,$y,$x, $newalpha << 24 | $rgb );
		}
	}
	
	imagesavealpha($im,true); imagealphablending($im,true);

	return true;
}




