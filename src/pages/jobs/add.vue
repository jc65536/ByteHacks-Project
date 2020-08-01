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
        <label class="block text-gray-700 text-xl font-bold mb-2" for="inline-full-name">
          Job
        </label>
        <input v-model="form.job" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" id="inline-full-name" type="text" placeholder="What is the job?">
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2" for="inline-password">
          Employer
        </label>
        <input v-model="form.employer" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" id="inline-full-name" type="text" placeholder="What Company/Name is hosting the job?">
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2" for="inline-full-name">
          # of Positions
        </label>
        <input v-model="form.postions" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" id="inline-full-name" type="text" placeholder="How many people can you hire?">
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2" for="inline-full-name">
          Job starting time
        </label>
        <Datetime type="datetime" v-model="form.start" use12-hour class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" placeholder="Click here to choose time"></Datetime>
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2" for="inline-full-name">
          Job ending time
        </label>
        <Datetime type="datetime" v-model="form.end" use12-hour class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" placeholder="Click here to choose time"></Datetime>
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2" for="inline-full-name">
          Location job will be hosted
        </label>
        <input v-model="form.location" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" id="inline-full-name" type="text" placeholder="Where does the job take place in?">
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2" for="inline-full-name">
          Salary job will be giving
        </label>
        <input v-model="form.salary" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" id="inline-full-name" type="text" placeholder="Answer in _____(money) in _____(time) format">
      </div>
      <div class="md:items-center mb-6">
        <label class="block text-gray-700 text-xl font-bold mb-2" for="inline-full-name">
          Description of the job
        </label>
        <input v-model="form.description" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" id="inline-full-name" type="text" placeholder="Give a tiny description about the job.">
      </div>
      <div class="md:items-center">
        <button class="shadow bg-teal-500 hover:bg-teal-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded" type="button">
          Create Job
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { Datetime } from 'vue-datetime'

export default {
  components: {
    Datetime
  },
  data () {
    return {
      form: {}
    }
  },
  methods: {
    submit () {
      //
    }
  }
}
</script>

<style scoped>
.txt {
  background: url('');
}
</style>
