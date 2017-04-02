var map, marker, waypointByID = {};
var currentObject;
var map;
var geocoder;
function initialize() {
  map = new google.maps.Map(document.getElementById('map'), {
      zoom: 15,
      center: new google.maps.LatLng(30.049956, 31.244395),
      mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  geocoder = new google.maps.Geocoder();
}
{% for waypoint in point_cores %}
waypointByID[{{waypoint.auto_id}}] = {
  name: "{{waypoint.store_code}}",
  lat: {{waypoint.point_location.y}},
  lng: {{waypoint.point_location.x}}
};
{% endfor %}
$(document).ready(function () {
  function searchWaypoints() {
  geocoder.geocode({
      'address': $('#address').val()
  }, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
          var position = results[0].geometry.location;
          $.get("{% url 'waypoints-search' %}", {
              lat: position.lat(),
              lng: position.lng()
          }, function (data) {
              if (data.isOk) {
                  $('#waypoints').html(data.content);
                  waypointByID = data.waypointByID;
                  activateWaypoints();
              } else {
                  alert(data.message);
              }
          }, 'json');
      } else {
          alert('Could not find geocoordinates for the following reason: ' + status);
      }
  });
}
$('#searchWaypoints').click(searchWaypoints);
$('#address').keydown(function(e) {
  if (e.keyCode == 13) searchWaypoints();
});
  function activateWaypoints() {
      // Add waypoint click handler
      $('.waypoint').each(function () {
          $(this).click(function() {
              var waypoint = waypointByID[this.id];
              var center = new google.maps.LatLng(waypoint.lat, waypoint.lng);
              currentObject = $(this);
              if (marker) marker.setMap();
              marker = new google.maps.Marker({map: map, position: center, draggable: true});
              google.maps.event.addListener(marker, 'dragend', function() {
                  var position = marker.getPosition();
                  waypoint.lat = position.lat();
                  waypoint.lng = position.lng();
                  currentObject.html(waypoint.name +
                      ' (' + waypoint.lat +
                      ', ' + waypoint.lng + ')');
                  $('#saveWaypoints').removeAttr('disabled');
              });
              map.panTo(center);
          }).hover(
              function () {this.className = this.className.replace('OFF', 'ON');},
              function () {this.className = this.className.replace('ON', 'OFF');}
          );
      });
  }
  $('#saveWaypoints').click(function () {
      var waypointStrings = [];
      for (id in waypointByID) {
          waypoint = waypointByID[id];
          waypointStrings.push(id + ' ' + waypoint.lng + ' ' + waypoint.lat);
      };
      $.post("{% url 'waypoints-save' %}",
      {
          waypointsPayload: waypointStrings.join('\n')
      }, function (data) {
          if (data.isOk) {
              $('#saveWaypoints').attr('disabled', 'disabled');
          } else {
              alert(data.message);
          }
      }, 'json');
  });
  activateWaypoints();
});
