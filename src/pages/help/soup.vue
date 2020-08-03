<template>
  <div style="display: flex; flex-grow: 1; flex-direction: column; margin-bottom: 300px">
    <div>
      <div class="control">
        <input type="radio" id="list" value="list" v-model="view" checked />
        <label for="list">List view</label>
        <input type="radio" id="map" value="map" v-model="view" />
        <label for="map">Map view</label>
      </div>
      <div class="control">
        How far to search: {{radius}} miles
        <input type="range" min="1" max="25" value="5" v-model="radius" />
      </div>
      <div class="control">
        <button @click="newSearch()">Search</button>
      </div>
    </div>
    <ul v-if="view=='list'">
      <li
        class="card"
        v-for="(place, index) in places"
        v-bind:key="index"
        @click="toggleCard(index)"
      >
        <div style="display: flex; flex-direction: row">
          <div class="place-img-frame">
            <img v-bind:src="place.image" style="height:100%; object-fit: cover" />
          </div>
          <div style="display: flex; flex-direction: column; justify-content: space-evenly">
            <p class="place-name">{{ place.name }}</p>
            <p class="place-address">{{ place.address }}</p>
          </div>
        </div>
        <div style="overflow: hidden; white-space: pre" v-bind:class="place.expanded ? 'expanding' : 'collapsing'">{{place.details}}</div>
      </li>
    </ul>
    <l-map
      v-if="view=='map'"
      :zoom="zoom"
      :center="center"
      :options="mapOptions"
      style="height: 500px"
      @update:center="centerUpdate"
      @update:zoom="zoomUpdate"
    >
      <l-tile-layer :url="url" :attribution="attribution" />
      <l-marker v-for="(place, index) in places" v-bind:key="index" :lat-lng="place.coordinates">
        <l-popup>
          <div @click="innerClick">
            {{place.name}}
            <br />
            {{place.address}}
          </div>
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup, LTooltip } from "vue2-leaflet";
import axios from "axios";

export default {
  name: "Example",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    LTooltip,
  },
  data() {
    return {
      zoom: 13,
      center: latLng(47.41322, -1.219482),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      withPopup: latLng(47.41322, -1.219482),
      withTooltip: latLng(47.41422, -1.250482),
      currentZoom: 11.5,
      currentCenter: latLng(47.41322, -1.219482),
      showParagraph: false,
      mapOptions: {
        zoomSnap: 0.5,
      },
      showMap: true,
      places: [],
      view: "list",
      radius: 5,
    };
  },
  methods: {
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },
    showLongText() {
      this.showParagraph = !this.showParagraph;
    },
    innerClick() {
      alert("Click!");
    },
    searchSoup() {
      axios
        .get("http://localhost:5000/api/soup", {
          params: {
            longitude: this.center.lng,
            latitude: this.center.lat,
            radius: this.radius,
          },
        })
        .then((response) => {
          this.places = response.data;
          for (var i in this.places) {
            this.places[i].coordinates = latLng(
              this.places[i].latitude,
              this.places[i].longitude
            );
            this.places[i].expanded = false; // is this card currently expanded?
            this.places[i].details = false; // initially false since we haven't gotten details yet
          }
        });
    },
    newSearch() {
      // get user location in browser and make call to api
      navigator.geolocation.getCurrentPosition((pos) => {
        var userLong = pos.coords.longitude;
        var userLat = pos.coords.latitude;
        this.center = latLng(userLat, userLong);
        this.searchSoup();
      });
    },
    toggleCard(i) {
      var place = this.places[i];
      place.expanded = !place.expanded;
      if (!place.details) {
        // make request for details for this place
        axios
          .get("http://localhost:5000/api/soup-info", {
            params: {
              id: place.id,
            },
          })
          .then((response) => {
            var data = response.data;
            var detailsString = "";
            if (data.successful) {
              if (data.open_now) {
                detailsString +=
                  "Open now.\nOpen today from " +
                  numToTime(data.open) +
                  " to " +
                  numToTime(data.close);
              } else {
                var weekdays = [
                  "Monday",
                  "Tuesday",
                  "Wednesday",
                  "Thursday",
                  "Friday",
                  "Saturday",
                  "Sunday",
                ];
                detailsString +=
                  "Not open now.\nNext opening is " +
                  weekdays[data.next_open] +
                  " from " +
                  numToTime(data.open) +
                  " to " +
                  numToTime(data.close);
              }
            } else {
              detailsString =
                "No opening or closing data was found for this place, sorry.";
            }
            place.details = detailsString;
            this.$set(this.places, i, place);
          });
      } else {
        this.$set(this.places, i, place);
      }
    },
  },
  mounted() {
    this.newSearch();
  },
};

function numToTime(n) {
  var hours = Math.floor(n / 100);
  var mins = n % 100;
  var am = hours < 12 ? "a.m." : "p.m.";
  if (hours > 12) hours -= 12;
  if (hours == 0) hours = 12;
  if (mins < 10) mins = "0" + mins;
  return hours + ":" + mins + " " + am;
}
</script>

<style scoped>
.card {
  padding: 10px;
  margin: 10px 0px;
  border-radius: 10px;
  box-shadow: 0px 1px 3px 0px #333;
  cursor: pointer;
}

input[type=radio] {
  display: none;
}

input[type=radio]+label {
  width: 100px;
  text-align: center;
  display: inline-block;
  cursor: pointer;
}

input[type=radio]+label::after {
  content: "";
  width: 0px;
  display: block;
  border: none;
}

input[type=radio]:checked+label::after {
  width: 100%;
  margin: auto;
  border-top: 2px solid #2b67cd;
  transition: width 0.2s;
}

input[type=radio]:checked+label {
  font-weight: bold;
  background-color: rgba(43, 103, 205, 0.1);
  transition: background-color 0.2s;
}

input[type=range] {
  margin-left: 10px;
}

.control {
  display: inline-flex;
  margin: 5px 0px;
}

.control::after {
  content: "";
  display: inline-block;
  width: 30px;
}

.place-name {
  font-size: 1.2rem;
}

button, input[type="button"] {
  border: 1px solid #2b67cd;
  padding: 2px 10px;
  border-radius: 5px;
  box-shadow: 0px 1px 1px 0px #333;
}

button:hover, input[type="button"]:hover {
  background-color: rgba(43, 103, 205, 0.1);
  box-shadow: 0px 1px 3px 0px #333;
  transition: box-shadow 0.15s, background-color 0.15s;
}

button:focus, input[type="button"]:focus {
  outline: none;
}

.place-img-frame {
  height: 64px;
  width: 64px;
  overflow: hidden;
  margin-right: 10px; 
}

.collapsing {
  height: auto;
  max-height: 0px;
  transition: max-height 0.2s cubic-bezier(0.1, 1.1, 0.5, 0.95);
}

.expanding {
  height: auto;
  max-height: 50px;
  transition: max-height 0.2s cubic-bezier(0.1, 1.1, 0.5, 0.95);
}
</style>