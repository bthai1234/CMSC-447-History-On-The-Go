var infowindow;
let service;
let map;
let bounds;
let directionsService;
let directionsRenderer;

var placesList = [];//Stores the array of locations returned from the google maps API
var markerList = [];//Stores the list of markers that have been placed on the map
var resultList = [];//Stores the list of HTML <li> list elements shown in the sidebar result list with id = 'places'  
var searchlocation = "";

function initMap() {
  //initialize the base map from google map api.
  searchlocation = { lat: 39.290385, lng: -76.612189 }; //default location baltimore eventual todo: gett location based on user gps  
  if(!document.getElementById("map")){ throw new Error('HTML element with id = map not found');}
  map = new google.maps.Map(document.getElementById("map"), {
    center: searchlocation,
    zoom: 15,
    mapId: "8d193001f940fde3", //b93bdcaff9612ab5
  });

  service = new google.maps.places.PlacesService(map); // Create the places service.
  //makes a Google maps Direction service endpoint
  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);

  try{
    getSearchBox();
  }catch(e){
    throw new Error(e);
  }
}

function getSearchBox(){
  if(!document.getElementById("map-input-address")){throw new Error('Text box with HTML id = map-input-address not found');}
  if(!document.getElementById("searchSubmitButton")){throw new Error('HTML Button element with HTML id = searchSubmitButton not found');}
  if(!document.getElementById("map-input-Figure")){throw new Error('Text box with HTML id = map-input-Figure not found');}
  
  //Gets search box with id="map-input" and appys google maps api search prediction and auto fill
  var input_address = document.getElementById("map-input-address");
  var searchBox = new google.maps.places.SearchBox(input_address);
  searchlocation = "";
  var input_figure = "";
    
  //event Listener for the button with id searchSubmitButton and
  //gets the values in the search box and
  //calls the loadMapMarkersAndPlaces() 
  document.getElementById("searchSubmitButton").addEventListener("click", function() {
    searchlocation = searchBox.getPlaces()[0].geometry.location; //retrieves the search
    input_figure = document.getElementById("map-input-Figure").value;

    try{
        loadMapMarkersAndPlaces(searchlocation, input_figure);
    }catch(e){
      throw new Error(e);
    }
  });

  //event listener for google maps address search box, will do the same as pressing the search button
  $("#map-input-address").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#searchSubmitButton").click();
    }
  });
  //event listener for radius select to , will do the same as pressing the search button
  $("#map-input-radius").change(function() {
      $("#searchSubmitButton").click();
  });
  //event listener for figure input, will do the same as pressing the search button
  $("#map-input-Figure").keyup(function() {
    if (event.keyCode === 13) {
      $("#searchSubmitButton").click();
    }
  });
  

  var inputs = {
    address: document.getElementById("map-input-address"),
    figure: document.getElementById("map-input-Figure")
  }
  return inputs;
}


//calls the google api and loads map markers by calling the getPlaces, addmarkers, and the addPlacesToResultSidebar functions 
async function loadMapMarkersAndPlaces(searchlocation, input_figure){
  cleanUp();//clears data from previous search
  
  let radiusSelect = document.getElementById("map-input-radius");
  // Value needs to multipled by 1000 to get meters -> kilometers
  let searchRadius = parseInt(radiusSelect.value) * 1000;

  //perform multiple searches with diffrent keywords, and combine each result
  await getPlaces(input_figure + " historical", searchlocation, searchRadius).then(function(results){
    placesList = results;
  }, function(err){
    throw new Error(err);
  });
  await getPlaces(input_figure + " museum", searchlocation, searchRadius).then(function(results){
    placesList = concatResults(placesList, results);
  }, function(err){
    throw new Error(err);
  });


  //If no search results are matched return 1.
  if(placesList.length == 0){
    alert("No locations found")
    return 1;
  }
  
  addMarkers(placesList, map); //adds all markers to the map
  addPlacesToResultSidebar(placesList); //add location names to the sidebar result list if one is defined in the HTML with the <ul id="places"></ul> tag
  
  //add specific special marker icon for original search position
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
  return 0;
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
        //console.error(status);
        reject(Error(status));
      }
    });
  });
}

//takes a list of locations returned by the google maps api for the first parameter and a refrence to the map object in the second and adds markers to the map    
function addMarkers(places, map) {
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
      //console.log("Returned place contains no geometry");
      throw new Error("A location in the places list doesn't contain location data.");
    }
  }
  map.fitBounds(bounds);   //zoom map out or in based on the markers placed
  return markerList;
}

//Param: places - array of locations returned by google maps api
//if there is a sidebar defined in the HTML with a <ul id="places"></ul> tag, to display a list of the results, add the names of the given locations to the sidebar  
function addPlacesToResultSidebar(places){
  if(!document.getElementById("places")){throw new Error('HTML ul list element with id = places  not found ');}


  $(document).ready(function() {
    for (const place of places) {
      if (place.geometry && place.geometry.location) {
        resultList = document.getElementById("places");
        var csrftoken = getCookie('csrftoken');


        var placeCard = $(document.createElement('div')).attr({'class':'card'});
        var cardBody = $(document.createElement('div')).attr({'class':'card-body'});

        //var locationImg = $(document.createElement('img')).attr({'src': '' ,'class': 'card-img-top', 'alt': ''});
        var cardHeader = $(document.createElement('h5')).attr({"class":"card-header"});

        var cardTitle = $(document.createElement('h5')).attr({"class":"card-title"});
        var cardText = $(document.createElement('p')).attr({"class":"card-text"});
        var submitButton = $(document.createElement('input')).attr({"id": place.name + "_id" , "class":"btn btn-primary", "type":"submit", "value":"Save to Itinerary"});
        
        cardHeader.text(place.name);
        cardText.text("Lorem ipsum dolor sit amet, consectetur adipiscing elit");
        cardTitle.text(place.name);


        cardBody.append(cardText,submitButton);
        placeCard.append(cardHeader,cardBody); //saveForm



        $("#places").append(placeCard);
        placeCard.click(function(){
          calculateAndDisplayRoute(directionsService, directionsRenderer, searchlocation, place.geometry.location)
        });
        placeCard.hover(function(){
          $(this).css('cursor','pointer');
        });
        
        submitButton.click(function(){
          $.ajax(
            {
              type:"POST",
              url: "/saveLocation/",
              dataType: "json",
              data:{
                place_name: place.name,
                lat: place.geometry.location.lat,
                lng: place.geometry.location.lng,
                csrfmiddlewaretoken: csrftoken,
              },
              success: function( data ) 
              {
                //alert(data.message); 
              },
              error: function(error){
                alert(error.message); // the message
              }
             })
            
             $(this).hide();
        });
        
      }else{
        throw new Error("A location in the places list doesn't contain location data.");
      }
    }
  });
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

//checks if A array contains a specific loctation obj, by comparing names
function placeListHas(place, placesList){
  for(const obj of placesList){
    if(place.name == obj.name){
      return true
    }
  }
  return false;
}

//combines two arrays that contain google maps api location data 
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

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function calculateAndDisplayRoute(directionsService, directionsRenderer, start, end) {
  const waypts = [];

  directionsService
    .route({
      origin: start,
      destination: end,
      waypoints: waypts,
      optimizeWaypoints: true,
      travelMode: google.maps.TravelMode.DRIVING,
    })
    .then((response) => {
      directionsRenderer.setDirections(response);
    })
    .catch((e) => window.alert("Directions request failed due to " + e.message));
}