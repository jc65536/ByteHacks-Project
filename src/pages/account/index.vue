<template>
  <div>
    <h2 class="text-teal-500 text-6xl text-center">
      Account Dashboard
    </h2>
    <p class="text-center">{{ $store.state.user.email }}</p>
    <div v-if="jobs.length">
      <h3 class="text-4xl text-center border-t border-gray-500 mt-5 pt-4">Job Listings</h3>
      <div v-for="job in jobs" :key="job.id">
        <Card
          :title="job.title"
          :toptag="job.positions + ' position(s) left'"
          :subtitle="'By ' + job.employer"
          :subtitle2="'pays ' + job.wage"
          :location="job.location"
          :startdate="job.start_date"
          :enddate="job.end_date"
          :editlink="'/jobs/' + job.id + '/edit'"
        >
          {{ job.description }}
        </Card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/plugins/axios'
import { EventBus } from '@/plugins/event'

export default {
  data () {
    return {
      jobs: []
    }
  },
  mounted () {
    if (!this.$store.getters.isValidJWT()) this.$router.push('/account/login')
    axios.get('/api/get-jobs', { email: this.$store.state.user.email })
    .then((res) => {
      this.jobs = res.data.jobs
    })
  },
  beforeDestoy () {
    EventBus.$off('userChanged')
  }
}
</script>
