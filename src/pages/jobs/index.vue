<template>
  <div>
    <h2 class="text-teal-500 text-6xl text-center">
      Find a Job Here
    </h2>
    <div v-for="job in jobs" :key="job.id">
      <Card
      :title="job.title"
      :titlelink="'/jobs/' + job.id"
      :toptag="job.positions + ' position(s) left'"
      :subtitle="'By ' + job.employer"
      :subtitle2="'pays ' + job.wage"
      :location="job.location"
      :startdate="job.start_date"
      :enddate="job.end_date"
      :applylink="'/jobs/'+job.id+'/apply'"
    >
      {{ job.description }}
    </Card>
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
