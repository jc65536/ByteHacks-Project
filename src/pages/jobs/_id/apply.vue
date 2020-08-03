<template>
<div>
  <h2 class="text-teal-500 text-6xl text-center">
      Apply
    </h2>
    <form @submit="submit()">
        <div class="form-entry">
        Full Name: <input v-model="application.name" type="text"/>
        </div>
        <div class="form-entry">
        Email: <input v-model="application.email" type="text"/>
        </div>
        <div class="form-entry">
        Anything else to say?<br/>
        <textarea v-model="application.description"/>
        </div>
        <div class="form-entry">
        <input type="submit" value="Apply now">
        </div>
    </form>
</div>
</template>

<script>
import axios from "axios"

export default {
  components: {
  },
  data () {
    return {
      application: {}
    }
  },
  asyncData (ctx) {
    return axios.get('/api/get-jobs', { id: ctx.route.params.id })
    .then((res) => {
      return { job: res.data.jobs[0] }
    })
  },
  methods: {
    submit() {
      axios.post("http://localhost:5000/api/");
    }
  }
}
</script>

<style scoped>
* {
    border: 1px solid black;
}
    input[type=text] {
        width: 300px;
        height: 30px;
    }

    textarea {
        width: 500px;
        height: 200px;
    }
</style>
