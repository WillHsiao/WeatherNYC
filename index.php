<!DOCTYPE html>
<head>
<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.css" />
<link rel="stylesheet" type="text/css" href="styles.css" />
<script src="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.js"></script>
<script src="https://code.jquery.com/jquery-2.1.4.min.js"></script>

<script src='https://api.mapbox.com/mapbox.js/v2.2.1/mapbox.js'></script>
<link href='https://api.mapbox.com/mapbox.js/v2.2.1/mapbox.css' rel='stylesheet' />

</head>

<body>
	<table width="1200">
		<tr>
		<td>
			<div id="mapframe" class="column"></div>
		</td>
		<td align=left>
			<div class="column">
				<form class="dark-matter">
				<h1>NYC Weather 7 Days Forecast<span>modify threshold to refresh warnings </span></h1>
				<label><span>Lowest Temperature: </span><input type="text" id="templow" value="32"><img src='img/cold.png'></label>
				<label><span>Highest Temperature: </span><input type="text" id="temphigh" value="100"><img src='img/sunny.png'></label>
				<label><span>Highest Heat Index: </span><input type="text" id="heathigh" value="100"><img src='img/heat.png'></label>
				<label><span>Highest Wind Speed: </span><input type="text" id="windhigh" value="12"><img src='img/windy.png'></label>
				<label><span>Highest Snow Fall (inches): </span><input type="text" id="snowhigh" value="5"><img src='img/snowy.png'></label>
				<label><span>Highest Rain Fall (inches): </span><input type="text" id="rainhigh" value="3"><img src='img/rainy.png'></label>
				<label><span></span><input type="button" class="button" onclick="myFunction()" value="Refresh"></label>
				</form>
			</div>
			<hr><div class='rtxt'>Forecast Range: <? include("range.txt"); ?></div>
		</td>
		</tr>
	</table>
<script>
function myFunction() {
    var x = document.getElementById("templow").value;
	drawMap();
}
window.onload = function () {
	drawMap();
}
function drawMap() {
    document.getElementById('mapframe').innerHTML = "<div id='my-map' style='width: 800px; height: 800px;'></div>";
    var basemap = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	});

    L.mapbox.accessToken = 'pk.eyJ1Ijoid2hzaWFvIiwiYSI6ImNqbTlmcHdwYjR1NXozcWxpaDBzNjAyMHkifQ._ID-U6L4Li7uMOSY8EI9Gw';

//    var basemap = L.tileLayer('https://api.mapbox.com/v4/mapbox.mapbox-streets-v7/{z}/{x}/{y}.png?access_token=' + L.mapbox.accessToken, {
//        attribution: '<a href="https://www.mapbox.com/tos/">Mapbox</a>'
//      });

    $.getJSON("geojson.json", function(data) {

    var sunnyIcon = new L.Icon({
      iconUrl: 'img/sunny.png', shadowUrl: 'img/marker-shadow.png',
      iconSize: [32, 37], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    });
    var snowyIcon = new L.Icon({
      iconUrl: 'img/snowy.png', shadowUrl: '/img/marker-shadow.png',
      iconSize: [32, 37], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    });
    var coldIcon = new L.Icon({
      iconUrl: 'img/cold.png', shadowUrl: 'img/marker-shadow.png',
      iconSize: [32, 37], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    });
    var greyIcon = new L.Icon({
      iconUrl: 'img/marker-icon-grey.png', shadowUrl: 'img/marker-shadow.png',
      iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    });
    var windyIcon = new L.Icon({
      iconUrl: 'img/windy.png', shadowUrl: 'img/marker-shadow.png',
      iconSize: [32, 37], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    });
    var rainyIcon = new L.Icon({
      iconUrl: 'img/rainy.png', shadowUrl: 'img/marker-shadow.png',
      iconSize: [32, 37], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    });
    var heatIcon = new L.Icon({
      iconUrl: 'img/heat.png', shadowUrl: 'img/marker-shadow.png',
      iconSize: [32, 37], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    });

    var geojson = L.geoJson(data, {


      onEachFeature: function (feature, layer) {
        layer.bindPopup('<b> ' + feature.properties.Area + '</b>'
			+ '<br>Lowest Temp: ' + getColor('TL',feature.properties.TempLowV) + feature.properties.TempLow + '</font> (' + feature.properties.TempLowTime + ')' + getDetail('TL',feature.properties.TempLowV, feature.properties.TempLowTimeDesc) 
			+ '<br>Highest Temp: ' + getColor('TH',feature.properties.TempHighV) + feature.properties.TempHigh + '</font> (' + feature.properties.TempHighTime + ')' + getDetail('TH',feature.properties.TempHighV, feature.properties.TempHighTimeDesc) 
			+ '<br>Highest HeatIndex: ' + getColor('HH',feature.properties.HeatHighV) + feature.properties.HeatHigh + '</font> (' + feature.properties.HeatHighTime + ')' + getDetail('HH',feature.properties.HeatHighV, feature.properties.HeatHighTimeDesc) 
			+ '<br>Highest Wind Speed: ' + getColor('WH',feature.properties.WindHighV) + feature.properties.WindHigh + '</font> (' + feature.properties.WindHighTime + ')' + getDetail('WH',feature.properties.WindHighV,feature.properties.WindHighTimeDesc) 
			+ '<br>Highest Snow Fall: ' + getColor('SH',feature.properties.SnowHighV) + feature.properties.SnowHigh + '</font> (' + feature.properties.SnowHighTime + ')' + getDetail('SH',feature.properties.SnowHighV,feature.properties.SnowHighTimeDesc) 
			+ '<br>Highest Rain Fall: ' + getColor('RH',feature.properties.RainHighV) + feature.properties.RainHigh + '</font> (' + feature.properties.RainHighTime + ')' + getDetail('RH',feature.properties.RainHighV,feature.properties.RainHighTimeDesc) );
        layer.setIcon(getIcon(feature.properties.TempLowV,
                              feature.properties.TempHighV,
                              feature.properties.HeatHighV,
                              feature.properties.WindHighV,
                              feature.properties.SnowHighV,
                              feature.properties.RainHighV
                     ));
      }
    });

    //get icons based on difficulty rating
    function getIcon(TL,TH,HH,WH,SH,RH) {
      if(SH >= document.getElementById("snowhigh").value) { return snowyIcon; }
      if(TL <= document.getElementById("templow").value) { return coldIcon; }
      if(TH >= document.getElementById("temphigh").value) { return sunnyIcon; }
      if(HH >= document.getElementById("heathigh").value) { return heatIcon; }
      if(WH >= document.getElementById("windhigh").value) { return windyIcon; }
      if(RH >= document.getElementById("rainhigh").value) { return rainyIcon; }
      return greyIcon;
    }
    function getColor(target, v) {
      switch(target){
	case 'TL':
          if(v <= document.getElementById("templow").value) { return '<font color=red>' } break;
	case 'TH':
          if(v >= document.getElementById("temphigh").value) { return '<font color=red>' } break;
	case 'HH':
          if(v >= document.getElementById("heathigh").value) { return '<font color=red>' } break;
	case 'WH':
          if(v >= document.getElementById("windhigh").value) { return '<font color=red>' } break;
	case 'RH':
          if(v >= document.getElementById("rainhigh").value) { return '<font color=red>' } break;
	case 'SH':
          if(v >= document.getElementById("snowhigh").value) { return '<font color=red>' } break;
      }
      return '<font>';
    }
    function getDetail(target, v, txt) {
      return '';
      switch(target){
	case 'TL':
          if(v <= document.getElementById("templow").value) { return '<br><font color=gray>' + txt + '</font><br>' } break;
	case 'TH':
          if(v >= document.getElementById("temphigh").value) { return '<br><font color=gray>' + txt + '</font><br>' } break;
	case 'HH':
          if(v >= document.getElementById("heathigh").value) { return '<br><font color=gray>' + txt + '</font><br>' } break;
	case 'WH':
          if(v >= document.getElementById("windhigh").value) { return '<br><font color=gray>' + txt + '</font><br>' } break;
	case 'RH':
          if(v >= document.getElementById("rainhigh").value) { return '<br><font color=gray>' + txt + '</font><br>' } break;
	case 'SH':
          if(v >= document.getElementById("snowhigh").value) { return '<br><font color=gray>' + txt + '</font><br>' } break;
      }
      return '';
    }

    var map = L.map('my-map')
    //.fitBounds(geojson.getBounds());
    .setView([40.709980,-73.937529], 11);

    basemap.addTo(map);
    geojson.addTo(map);
  });

};
</script>
</body>
</html>
