
var map = L.map('map', {
    center: [42.3370, -71.0892],
    zoom: 12
});

L.tileLayer(
    'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://osm.org/copyright">\
			   OpenStreetMap</a> contributors, &copy;\
			   <a href="https://carto.com/attribution">CARTO</a>'
    }).addTo(map);

markerGroup = new L.LayerGroup();
posMarker = L.marker([42.3370, -71.089], {opacity: 0}).addTo(map);

// lets you fill lat and long by clicking on the map
map.on('click', function (e) {
    // fills the lat and long fields
    document.getElementById('lat').value = e.latlng.lat;
    document.getElementById('long').value = e.latlng.lng;

    // places a marker where you click
    // posMarker = L.marker([e.latlng.lat,e.latlng.lng]).addTo(map);
    posMarker.setLatLng([e.latlng.lat, e.latlng.lng]).setOpacity(1);
    posMarker.bindTooltip("start location", {permanent: false})
    posMarker.openTooltip()

})


function returnIcon(string) {
	switch(string) {
	// food - red
	case 'ice_cream':
		return L.AwesomeMarkers.icon({icon : 'ice-cream', markerColor : 'red'});
	break;
	
	case 'pub':
	case 'bar':
	case 'biergarten':
		return L.AwesomeMarkers.icon({icon : 'beer', markerColor : 'red'});
	break;
	
	case 'fast_food':
	return L.AwesomeMarkers.icon({icon : 'fast-food', markerColor : 'red'});
	
	break;
	
	case 'restaurant':
	case 'cafe': 
	case 'food_court':
	return L.AwesomeMarkers.icon({icon : 'pizza', markerColor : 'red'});
	
	break;
	
	//utility - blue
	case 'waste_basket':
	return L.AwesomeMarkers.icon({icon : 'trash', markerColor : 'blue'});
	break;
	
	case 'toilets':
	return L.AwesomeMarkers.icon({icon : 'water-outline', markerColor : 'blue'});
	break;
	
	case 'drinking_water':
	return L.AwesomeMarkers.icon({icon : 'water', markerColor : 'blue'});
	break;
	
	case 'shower':
	return L.AwesomeMarkers.icon({icon : 'rainy', markerColor : 'blue'});
	break;
	
	case 'telephone':
	
	break;
	
	case 'waste_disposal':
	return L.AwesomeMarkers.icon({icon : 'trash-outline', markerColor : 'blue'});
	break;
	
	case 'bicycle_rental':
	case 'bicycle_parking':
	case 'bicycle_parking':
	return L.AwesomeMarkers.icon({icon : 'bicycle-outline', markerColor : 'blue'});
	break;
	
	case 'post_box':
	return L.AwesomeMarkers.icon({icon : 'mail', markerColor : 'blue'});
	break;
	
	//parking - black
	case 'parking':
	case 'parking_space':
	case 'parking_entrance':
	return L.AwesomeMarkers.icon({icon : 'car', markerColor : 'black'});
	break;
	
	//recreation - orange
	case 'planetarium':
	return L.AwesomeMarkers.icon({icon : 'planet', markerColor : 'orange'});
	break;
	
	case 'arts_center':
	return L.AwesomeMarkers.icon({icon : 'brush', markerColor : 'orange'});
	break;
	
	case 'cinema':
	return L.AwesomeMarkers.icon({icon : 'videocam', markerColor : 'orange'});
	break;
	
	case 'dive_centre':
	return L.AwesomeMarkers.icon({icon : 'boat', markerColor : 'orange'});
	break;
	
	case 'theatre':
	return L.AwesomeMarkers.icon({icon : 'accessibility', markerColor : 'orange'});
	break;
	
	case 'fountain':
	return L.AwesomeMarkers.icon({icon : 'water', markerColor : 'orange'});
	break;
	
	case 'nightclub':
	return L.AwesomeMarkers.icon({icon : 'happy', markerColor : 'orange'});
	break;
	
	case 'internet_cafe':
	return L.AwesomeMarkers.icon({icon : 'wifi', markerColor : 'orange'});
	break;
	
	case 'marketplace':
	return L.AwesomeMarkers.icon({icon : 'cash', markerColor : 'orange'});
	break;
	
	//government - grey
	case 'public_building':
	return L.AwesomeMarkers.icon({icon : 'business', markerColor : 'grey'});
	break;
	
	case 'fire_station':
	return L.AwesomeMarkers.icon({icon : 'flame', markerColor : 'grey'});
	break;
	
	case 'police':
	return L.AwesomeMarkers.icon({icon : 'alert-circle', markerColor : 'grey'});
	break;
	
	case 'post_office':
	return L.AwesomeMarkers.icon({icon : 'mail', markerColor : 'grey'});
	break;
	
	// religion - brown
	case 'place_of_worship':
	return L.AwesomeMarkers.icon({icon : 'business', markerColor : 'star'});
	
	break;


	
	default:
	return L.AwesomeMarkers.icon({icon : 'alert', markerColor : 'yellow'})
	} 
	}

function placeLocationMarkers() {
    let checkboxes = document.querySelectorAll("input[name='preferences']")
    let preferences = []
    checkboxes.forEach(p => {
        if (p.checked) {
            preferences.push(p.value)
        }
    })
    const data = {
        "start_lon": parseFloat(document.getElementById("long").value),
        "start_lat": parseFloat(document.getElementById("lat").value),
        "radius": parseInt(document.getElementById("distance").value),
        "preferences": preferences
    };
    console.log(data)
    fetch('http://0.0.0.0:8000/route', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            data.forEach(obj => obj["properties"] = obj["tags"])
            data.forEach(obj => delete obj["tags"])
            let markers = []
            data.forEach((geoJSON, idx) => {

                let long = geoJSON["geometry"]["coordinates"][0]
                let lat = geoJSON["geometry"]["coordinates"][1]
                let number = idx + 1
                let m = L.marker([lat,long], {icon : returnIcon(geoJSON["properties"]["amenity"])}).bindTooltip(number + ". " + geoJSON["properties"]["type"], {permanent: true});
                m.addTo(map)
                markers.push(m)

            })
            markers.forEach(marker => marker.openTooltip())
            console.log("after cleaning", data)
        })
        .catch((error) => {
            console.error('Error:', error);
        })
}


function updateTextInput(val) {
    document.getElementById('textInput').value = val;
}


