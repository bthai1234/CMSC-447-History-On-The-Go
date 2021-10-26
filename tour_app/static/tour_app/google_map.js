var infowindow;
let service;
let map;
let bounds;

var placesList = [];//Stores the array of locations returned from the google maps API
var markerList = [];//Stores the list of markers that have been placed on the map
var resultList = [];//Stores the list of HTML <li> list elements shown in the sidebar result list with id = 'places'  
var search_radus = '10000';//default value
var searchlocation;

function initMap() {
  //initialize the base map from google map api.
  searchlocation = { lat: 39.290385, lng: -76.612189 }; //default location baltimore eventual todo: gett location based on user gps  
  map = new google.maps.Map(document.getElementById("map"), {
    center: searchlocation,
    zoom: 15,
    mapId: "b93bdcaff9612ab5",
  });

  // Create the places service.
  service = new google.maps.places.PlacesService(map);

  //Gets search box with id="map-input" and appys google maps api search prediction and auto fill
  const input = document.getElementById("map-input");
  const searchBox = new google.maps.places.SearchBox(input);

  //Adds Search box to to the map bounds. Comment out if you want the placment else where 
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(input);
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });

  //event Listener for the search box when the user selects a search prediction and
  //clears out the markers on the map and clears the makreList and placesList array and
  //calls the google maps api for a new search 
  searchBox.addListener("places_changed", () => {
    //retrieves the search 
    var places = searchBox.getPlaces(); 
    searchlocation = places[0].geometry.location;

    //clean up previous search if any
    // Deletes markers on the map from previous search result.
    markerList.forEach((marker) => {
      marker.setMap(null);
    });
    //clear out sidebar search results
    while(resultList.firstChild){
      resultList.removeChild(resultList.firstChild);
    }
    resultList = [];
    markerList = [];
    placesList = [];

    //calls the getPlaces function with multiple keyword strings, which will call the google maps api
    getPlaces("historical location", searchlocation, search_radus);
    getPlaces("historical", searchlocation, search_radus);
    getPlaces("museum", searchlocation, search_radus);
  });
}

//keyword search string, location takes google api location object(lat and long), radius in meters.
function getPlaces(searchKeyword, searchLocation, searchRadius){
  var request = {
    location: searchLocation,
    radius: searchRadius,
    keyword: searchKeyword,
  };

  //Defines a new bounding box for the map
  bounds = new google.maps.LatLngBounds();
  
  service.nearbySearch(request, (results, status) => { 
    if (status !== "OK" || !results)return;
    placesList = results;
    addMarkers(results, map);
  });
}

//takes a list of locations returned by the google maps api and the map object  
function addMarkers(places, map) {
  //add specific marker for search position
  const icon = { 
    url: "../../static/tour_app/images/map_home.png",
    scaledSize: new google.maps.Size(40, 40),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(0, 40),
  };
  const marker = new google.maps.Marker({
    map,
    icon: icon,
    animation: google.maps.Animation.DROP,
    position: searchlocation,
  });
  //adds marker to marker array
  markerList.push(marker);

  for (const place of places) {
    if (place.geometry && place.geometry.location) {
      //first check if marker was already added berfore adding marker to map and to sidebar list.
      if(!containsMarker(place)){
        //creates new marker and adds to map
        const marker = new google.maps.Marker({
          map,
          title: place.name,
          animation: google.maps.Animation.DROP,
          position: place.geometry.location,
        });
        //adds marker to marker array
        markerList.push(marker);

        //keeps track of marker bounds to zoom map out if needed
        if (place.geometry.viewport) {
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }

        //adds each location name to the sidebar in a HTML tag <li> with id="li". In a unordered list <ul> with id='places'. And store access to them in the array resultList  
        resultList = document.getElementById("places");
        const li = document.createElement("li");
        li.textContent = place.name;
        resultList.appendChild(li);
        li.addEventListener("click", () => { //adds event listiner to center map to location when location name is clicked from the sidebar
          map.setCenter(place.geometry.location);
          map.zoom(30);
        });
      }

    }else{
      console.log("Returned place contains no geometry");
      return;
    }
  }
  //zoom map out or in based on the markers placed
  map.fitBounds(bounds);
}

//compares the name of a google maps place object and a markers title which contains the name of its location. returns true if the name matches, otherwise false  
function containsMarker(place){
  for (const obj of markerList){
    if(place.name === obj.title){
      return true;
    }
  }
  return false;
}