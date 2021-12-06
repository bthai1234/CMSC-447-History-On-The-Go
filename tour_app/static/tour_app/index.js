var searchlocation = "";

function init() {
    searchlocation = { lat: 39.290385, lng: -76.612189 }; //default location baltimore eventual todo: gett location based on user gps  

    if(!document.getElementById("map-input-address")){throw new Error('Text box with HTML id = map-input-address not found');}
    if(!document.getElementById("map-input-Figure")){throw new Error('Text box with HTML id = map-input-Figure not found');}

    var input_address = document.getElementById("map-input-address");
    var searchBox = new google.maps.places.SearchBox(input_address);
    searchlocation = "";
    var input_figure = "";

    document.getElementById("submitbutton").addEventListener("click", function() {
        searchlocation = searchBox.getPlaces()[0]; //retrieves the search
        var placeName = searchlocation.name;
        var lat = searchlocation.geometry.location.lat;
        var lng = searchlocation.geometry.location.lng; 
        input_figure = document.getElementById("map-input-Figure").value;
        let radiusSelect = document.getElementById("map-input-radius");
     
        let searchRadius = parseInt(radiusSelect.value) * 1000;
        var csrftoken = getCookie('csrftoken');

        var redirect = document.getElementById("mapPageUrl").textContent;

        var form = $(document.createElement('form')).attr({'action': redirect, 'method': "POST", 'style': "display: none"});

        var latForm = $(document.createElement("input")).attr({'type': "hidden", 'name': 'lat', 'value': lat});
        var lngForm = $(document.createElement("input")).attr({'type': "hidden", 'name': 'lng', 'value': lng});
        var place_name = $(document.createElement("input")).attr({'type': "hidden", 'name': 'placeName', 'value': placeName});
        var figure = $(document.createElement("input")).attr({'type': "hidden", 'name': 'figure', 'value': input_figure});
        var radius = $(document.createElement("input")).attr({'type': "hidden", 'name': 'radius', 'value': searchRadius});
        var csrf = $(document.createElement("input")).attr({'type': "hidden", 'name': 'csrfmiddlewaretoken', 'value': csrftoken});

        form.append(latForm,lngForm,place_name,figure,radius,csrf);
        $('body').append(form);
        form.submit();

    });
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

