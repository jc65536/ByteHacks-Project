<template>
  <div>
    <h2 class="text-teal-500 text-6xl text-center">
      Account Dashboard
    </h2>
    <p class="text-center">{{ $store.state.user.email }}</p>
    <div v-if="messages.length">
      <h3 class="text-4xl text-center border-t border-gray-500 mt-5 pt-4">Incoming Messages</h3>
      <div v-for="msg in messages" :key="msg.id">
        <p>{{ msg.message }}</p>
      </div>
    </div>
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
          :deletelink="'/jobs/' + job.id"
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
      jobs: [],
      messages: []
    }
  },
  mounted () {
    if (!this.$store.getters.isValidJWT()) this.$router.push('/account/login')
    axios.get('/api/get-jobs', { email: this.$store.state.user.email })
    .then((res) => {
      this.jobs = res.data.jobs
    })
    axios.get('/api/get-messages', {}, this)
    .then((res) => {
      this.messages = res.data.received
    })
  },
  beforeDestoy () {
    EventBus.$off('userChanged')
  }
}
</script>
