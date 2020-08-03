<template>
  <div>
    <h2 class="text-teal-500 text-6xl text-center">
      Find a Job Here
    </h2>
    <div class="container my-5 mx-auto px-4 md:px-12">
      <div class="flex flex-wrap -mx-1 lg:-mx-4">
        <div v-for="i in [0, 1, 2]" :key="i" class="my-1 px-1 w-full md:w-1/2 lg:my-4 lg:px-4 lg:w-1/3">
          <div v-for="[jindex, job] of Object.entries(jobs)" :key="jindex">
            <Card
              v-if="(jindex - i) % 3 === 0"
              :title="job.title"
              :titlelink="'/jobs/' + job.id"
              :toptag="job.positions + ' position(s) left'"
              :subtitle="'By ' + job.employer"
              :subtitle2="'pays ' + job.wage"
              :location="job.location"
              :startdate="job.start_date"
              :enddate="job.end_date"
            >
              {{ job.description }}
            </Card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/plugins/axios'
import Card from '@/components/Card'

export default {
  components: {
    Card
  },
  data () {
    return {
      jobs: []
    }
  },
  asyncData (ctx) {
    return axios.get('/api/get-jobs')
    .then((res) => {
      return res.data
    })
  }
}
</script>
