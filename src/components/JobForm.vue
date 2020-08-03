<template>
<form class="max-w-lg text-center m-10 mx-auto">
  <div class="md:items-center mb-6">
    <label class="block text-gray-700 text-xl font-bold mb-2">
      Job
    </label>
    <input v-model="form.title" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" type="text" placeholder="Ex. Farm worker">
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
    <input v-model="form.positions" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" type="number" placeholder="How many people can you hire?">
  </div>
  <div class="md:items-center mb-6">
    <label class="block text-gray-700 text-xl font-bold mb-2">
      Job starting date/time
    </label>
    <Datetime
      type="datetime"
      v-model="form.start_date"
      :minute-step="15"
      use12-hour
      value-zone="America/Los_Angeles"
      class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500"
      placeholder="Click here to pick"
    ></Datetime>
  </div>
  <div class="md:items-center mb-6">
    <label class="block text-gray-700 text-xl font-bold mb-2">
      Job ending date/time
    </label>
    <Datetime
      type="datetime"
      v-model="form.end_date"
      :minute-step="15"
      use12-hour
      value-zone="America/Los_Angeles"
      class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500"
      placeholder="Click here to pick"
    ></Datetime>
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
    <input v-model="form.wage" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500" type="text" placeholder="Ex. $1 per hour">
  </div>
  <div class="md:items-center mb-6">
    <label class="block text-gray-700 text-xl font-bold mb-2" for="inline-full-name">
      Description of the job
    </label>
    <textarea v-model="form.description" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500"  placeholder="Short Job Description"></textarea>
    <p class="text-sm text-red-600">{{ error }}</p>
  </div>
  <div class="md:items-center">
    <button class="shadow bg-teal-500 hover:bg-teal-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded" type="button" @click="submit">
      Save Job
    </button>
  </div>
</form>
</template>

<script>
import { Datetime } from 'vue-datetime'

export default {
  components: {
    Datetime
  },
  props: {
    form: {
      type: Object,
      default: () => { return {} }
    },
    error: {
      type: String
    }
  },
  methods: {
    submit () {
      for (const field in this.form) {
        if (this.form[field].length < 1) {
          this.error = 'Please make sure you have filled every field'
          return
        }
      }

      this.$emit('submitForm', this.form)
    }
  }
}
</script>
