var infowindow;
let service;
let map;
let bounds;

var placesList = [];//Stores the array of locations returned from the google maps API
var markerList = [];//Stores the list of markers that have been placed on the map
var resultList = [];//Stores the list of HTML <li> list elements shown in the sidebar result list with id = 'places'  
var search_radus = '25000';//default value
var searchlocation;


function initMap() {
  //initialize the base map from google map api.
  searchlocation = { lat: 39.290385, lng: -76.612189 }; //default location baltimore eventual todo: gett location based on user gps  
  map = new google.maps.Map(document.getElementById("map"), {
    center: searchlocation,
    zoom: 15,
    mapId: "b93bdcaff9612ab5",
  });

  service = new google.maps.places.PlacesService(map); // Create the places service.

  //Gets search box with id="map-input" and appys google maps api search prediction and auto fill
  const input_container = document.getElementById("input_container");
  const input_address = document.getElementById("map-input-address");
  const searchBox = new google.maps.places.SearchBox(input_address);

  //Adds Search box to to the map bounds. Comment out if you want the placment else where 
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(input_container);
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });

  //event Listener for the search box when the user selects a search prediction and
  //clears out the markers on the map and clears the makreList and placesList array and
  //calls the google maps api for a new search 
  document.getElementById("search_figure").addEventListener("click", function() {
    var place = searchBox.getPlaces(); //retrieves the search
    searchlocation = place[0].geometry.location;

    cleanUp();//clears data from previous search

    loadMapMarkersAndPlaces();
  });
}

//calls the google api and loads map markers by calling the getPlaces, addmarkers, and the addPlacesToResultSidebar functions 
async function loadMapMarkersAndPlaces(){

  var input_figure = document.getElementById("map-input-Figure").value;

  //perform multiple searches with diffrent keywords, and combine each result
  results = await getPlaces(input_figure + " historical", searchlocation, search_radus); 
  placesList = results;
  results = await getPlaces(input_figure + " museum", searchlocation, search_radus); 
  placesList = concatResults(placesList, results);

  //If no search results are matched do nothing.
  if(placesList.length == 0){
    return;
  }
  
  addMarkers(placesList, map); //adds all markers to the map
  addPlacesToResultSidebar(placesList); //add location names to the sidebar result list if one is defined in the HTML with the <ul id="places"></ul> tag
}

//keyword search string, location takes google api location object(lat and long), radius in meters.
function getPlaces(searchKeyword, searchLocation, searchRadius){
  var request = {
    location: searchLocation,
    radius: searchRadius,
    keyword: searchKeyword,
  };

  return new Promise((resolve, reject) => {
    service.nearbySearch(request, (results, status) => { 
      if (status == google.maps.places.PlacesServiceStatus.OK || results){
        resolve(results);
      }else{
        reject(status);
      }
    });
  });
}

//takes a list of locations returned by the google maps api and the map object  
function addMarkers(places, map) {
  //add specific special marker icon for search position
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

  markerList.push(marker); //adds marker to marker array

  for (const place of places) {
    if (place.geometry && place.geometry.location) {
      if(!containsMarker(place, markerList)){ //first check if marker was already added berfore adding marker to map 
        const marker = new google.maps.Marker({ //creates new marker and adds to map
          map,
          title: place.name,
          animation: google.maps.Animation.DROP,
          position: place.geometry.location,
        });

        markerList.push(marker); //adds marker to marker array

        //checks marker bounds to zoom map out if needed
        if (place.geometry.viewport) {
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }
      }

    }else{
      console.log("Returned place contains no geometry");
      return;
    }
  }
  map.fitBounds(bounds);   //zoom map out or in based on the markers placed
}

//Param: places - array of locations returned by google maps api
//if there is a sidebar defined in the HTML with a <ul id="places"></ul> tag, to display a list of the results, add the names of the given locations to the sidebar  
function addPlacesToResultSidebar(places){
  if(document.getElementById("places")){
    for (const place of places) {
      if (place.geometry && place.geometry.location) {
        resultList = document.getElementById("places");
        const li = document.createElement("li");
        li.textContent = place.name;
        resultList.appendChild(li);
        li.addEventListener("click", () => { //adds event listiner to center map to location when location name is clicked from the sidebar
          map.setCenter(place.geometry.location);
          //TODO zoom in?
        });
      }
    }
  }
  return resultList;
}

//compares the name of a google maps place object and a markers title which contains the name of its location. returns true if the name matches, otherwise false  
function containsMarker(place, markerList){
  for (const obj of markerList){
    if(place.name == obj.title){
      return true;
    }
  }
  return false;
}

//checks if A place list contains a specific loctation obj, by comparing names
function placeListHas(place, placesList){
  for(const obj of placesList){
    if(place.name == obj.name){
      return true
    }
  }
  return false;
}

//combines two placelist 
function concatResults(placesListA, placesListB){
  var result = placesListA;
  for(const placeB of placesListB){
    if(!placeListHas(placeB, placesListA)){
      result.push(placeB);
    }
  }

  return result;
}

//clears the markers on the map and the result list and the arrays storing the locations, markers, and result list, 
function cleanUp(){
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
  //Defines a new bounding box for the map
  bounds = new google.maps.LatLngBounds();
}