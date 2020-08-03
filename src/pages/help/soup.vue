<template>
  <div style="display: flex; flex-grow: 1; flex-direction: column; margin-bottom: 300px">
    <div>
      <div class="control"><input type="radio" value="list" v-model="view" checked />List view</div>
      <div class="control"><input type="radio" value="map" v-model="view" />Map view</div>
      <div class="control">How far to search: {{radius}} miles <input type="range" min="1" max="25" value="5" v-model="radius" /></div>
      <div class="control"><button id="place-search" @click="newSearch()">Search</button></div>
    </div>
    <ul v-if="view=='list'">
      <li class="place-card" v-for="(place, index) in places" v-bind:key="index" @click="toggleCard(index)">
        <div style="display: flex; flex-direction: row">
          <div style="height: 50px; width: 50px; overflow: clip; margin-right: 10px; ">
          <img v-bind:src="place.image" style="height: 50px; object-fit: cover" />
          </div>
          <div>
            <p class="place-name">{{ place.name }}</p>
            <p class="place-address">{{ place.address }}</p>
          </div>
        </div>
        <div v-if="place.expanded"><!--Details go here--></div>
        <!--<input type="text" v-model="place.one" />
        - {{ place.one }}
        <input type="text" v-model="place.two" />
        - {{ place.two }}-->
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
            {{place.name}} <br/>
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
            this.places[i].expanded = false;        // is this card currently expanded?
            this.places[i].details = false;         // initially false since we haven't gotten details yet
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
        if (place.expanded) {
            if (place.gotDetails) {

            } else {
                // make request for details for this place
                console.log(place.id);
                axios.get("http://localhost:5000/api/soup-info", {
                    params: {
                        id: place.id
                    }
                }).then((response) => {
                    var data = response.data;
                    console.log(data);
                });
            }
        } else {

        }
    }
  },
  mounted() {
    this.newSearch();
  },
};
</script>

<style scoped>
.place-card {
  padding: 10px;
  margin: 10px 0px;
  border-radius: 10px;
  box-shadow: 0px 1px 3px 0px #333;
  cursor: pointer;
}

.control {
    display: inline-block;
    margin: 5px 0px;
}

.control::after {
    content: "";
    display: inline-block;
    width: 40px;
}

#place-search {
    border: 2px solid #70ddff;
    border-radius: 10px;
    padding: 2px 10px;
}
</style>