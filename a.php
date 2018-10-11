<?
$str = file_get_contents('wdata/alerts');
$json = json_decode($str, true);
//echo '<pre>' . print_r($json, true) . '</pre>';
foreach ($json['features'] as $k => $v){
	$tmp .= '<button class="collapsible">';
	$tmp .=  $json['features'][$k]['properties']['headline'];
	$tmp .= '</button>';
	$tmp .= '<div class="content">';
	$tmp .=  $json['features'][$k]['properties']['description'];
	$tmp .= '</div>';
}
?>
