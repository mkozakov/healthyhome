  
google.maps.event.addDomListener(window, 'load', initialize);

function initialize() {

	var bounds = new google.maps.LatLngBounds();
	var mapOptions = {
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		disableDefaultUI: true,
		panControl: true,
  		zoomControl: true
	}
	var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

	//TODO: replace mock data with API call  
	var buildingList = [
	{
		"lat" 	: 43.667576,
		"lng" 	: -79.391868,
		"id"  	: "1",
		"title" : "building1"
	},
	{
		"lat" 	: 43.663991,
		"lng"	: -79.398580,
		"id"  	: "2",
		"title" : "building2"
	},
	{
		"lat"	: 43.651230,
		"lng" 	: -79.409866,
		"id"  	: "3",
		"title" : "building3"
	},
	{
		"lat" 	: 43.665326,
		"lng" 	: -79.411154,
		"id"  	: "4",
		"title" : "building4"
	},
	{
		"lat"	: 43.775326,
		"lng" 	: -79.411154,
		"id"  	: "5",
		"title" : "building5"
	}	
	];

	//Place buildings on the map
	$.each(buildingList, function(index, value) {
		var latLong = new google.maps.LatLng(value.lat, value.lng);
		bounds.extend(latLong);
		var marker = new google.maps.Marker({
			position: latLong,
			map: map,
			title: value.title
		});
		google.maps.event.addListener(marker, 'click', function() {
	    	window.location = "/building/" + value.id;
  		});
	});
	map.fitBounds(bounds);
	map.panToBounds(bounds);
}
