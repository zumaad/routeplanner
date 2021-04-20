
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
    posMarker.bindTooltip("start location", {permanent: true})
    posMarker.openTooltip()

})

function getStuff() {
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
    //http://ec2-54-160-116-97.compute-1.amazonaws.com:8000/locations
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
                let m = L.marker([lat,long]).bindTooltip(number + ". " + geoJSON["properties"]["type"], {permanent: true});
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


