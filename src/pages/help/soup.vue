<template>
  <div style="display: flex; flex-grow: 1; flex-direction: column; margin-bottom: 300px">
      <div>
          <input type="radio" value="list" v-model="view" checked>List view
          <input type="radio" value="map" v-model="view">Map view
      </div>
    <ul v-if="view=='list'">
      <li class="place-card" v-for="(place, index) in places" v-bind:key="index">
        <div style="display: flex; flex-direction: row">
          <img v-bind:src="place.image" style="height: 50px" />
          <div>
            <p class="place-name">{{ place.name }}</p>
            <p class="place-address">{{ place.address }}</p>
          </div>
        </div>
        <!--<input type="text" v-model="place.one" />
        - {{ place.one }}
        <input type="text" v-model="place.two" />
        - {{ place.two }}-->
      </li>
    </ul>
    <button @click="showLongText">Toggle long popup</button>
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
            I am a popup
            <p v-show="showParagraph">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque
              sed pretium nisl, ut sagittis sapien. Sed vel sollicitudin nisi.
              Donec finibus semper metus id malesuada.
            </p>
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
      view: "list"
    };
  },
  mounted() {
    // get user location in browser and make call to api
    navigator.geolocation.getCurrentPosition((pos) => {
      var userLong = pos.coords.longitude;
      var userLat = pos.coords.latitude;
      this.center = latLng(userLat, userLong);
      console.log("User location:" + userLong + " " + userLat);
      axios
        .get("http://localhost:5000/api/soup", {
          params: {
            longitude: userLong,
            latitude: userLat,
          },
        })
        .then((response) => {
          this.places = response.data;
          for (var i in this.places) {
              this.places[i].coordinates = latLng(this.places[i].latitude, this.places[i].longitude)
          }
        });
    });
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
  },
};
</script>

<style scoped>
.place-card {
  padding: 10px;
  margin: 10px 0px;
  border-radius: 10px;
  box-shadow: 0px 1px 3px 0px #333;
}
</style>