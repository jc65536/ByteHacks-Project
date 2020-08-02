<template>
  <div class.txt= "txt">
      <h2 class="text-teal-500 text-6xl text-center">
        Create a new job
      </h2>
      <h3 class="text-center text-teal-500 text-xl">
        Answer the questions below and type the answers in the box below.  Once you are done, click on Submit.
      </h3>
    <form class="max-w-lg text-center m-10 mx-auto">
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2">
          Job
        </label>
        <input v-model="form.job" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" type="text" placeholder="Ex. Farm worker">
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2">
          Employer
        </label>
        <input v-model="form.employer" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" type="text" placeholder="Ex. Bill's Farms">
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2">
          Positions Available
        </label>
        <input v-model="form.postions" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" type="number" placeholder="How many people can you hire?">
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2">
          Job starting date/time
        </label>
        <Datetime type="datetime" v-model="form.start" use12-hour class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" placeholder="Click here to pick"></Datetime>
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2">
          Job ending date/time
        </label>
        <Datetime type="datetime" v-model="form.end" use12-hour class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" placeholder="Click here to pick"></Datetime>
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2">
          Job location
        </label>
        <input v-model="form.location" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" type="text" placeholder="Where does the job take place at?">
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2" for="inline-full-name">
          Base salary
        </label>
        <input v-model="form.salary" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" type="text" placeholder="Ex. $1 per hour">
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2" for="inline-full-name">
          Description of the job
        </label>
        <textarea v-model="form.description" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500"  placeholder="Short Job Description"></textarea>
      </div>
      <div class="md:items-center">
        <button class="shadow bg-teal-500 hover:bg-teal-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded" type="button" @click="submit">
          Create Job
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { Datetime } from 'vue-datetime'
import axios from '@/plugins/axios'

export default {
  components: {
    Datetime
  },
  data () {
    return {
      form: {}
    }
  },
  mounted () {
    if (!this.$store.getters.isValidJWT()) this.$router.push('/account/login')
  },
  methods: {
    submit () {
      axios.post('/api/add-job', this.form, this)
      .then((res) => {
        alert(`Job posted! Job id ${res.data.id}`)
      })
      .catch(err => alert(err))
    }
  }
}
</script>

<style scoped>
</style>
