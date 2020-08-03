<template>
  <div>
    <h2 class="text-teal-500 text-6xl text-center">
      Job Details
    </h2>
    <!-- <p class="text-center">{{ $store.state.user.email }}</p> -->
    <Card
      :title="job.title"
      :toptag="job.positions + ' position(s) left'"
      :subtitle="'By ' + job.employer"
      :subtitle2="'pays ' + job.wage"
      :location="job.location"
      :startdate="job.start_date"
      :enddate="job.end_date"
    >
      {{ job.description }}
    </Card>
    <div v-if="$store.state.user && job.creator === $store.state.user.email" class="text-center w-full">
      <p class="text-sm text-red-600">{{ error }}</p>
      <n-link :to="'/jobs/' + job.id + '/edit'">
        <button class="bg-teal-600 rounded-md m-2 p-2 font-bold text-gray-200">Edit Job</button>
      </n-link>
      <button class="bg-red-600 rounded-md m-2 p-2 font-bold text-gray-200" @click="deleteJob">Delete Job</button>
    </div>
  </div>
</template>

<script>
import axios from '@/plugins/axios'

export default {
  data () {
    return {
      job: {},
      error: ''
    }
  },
  asyncData (ctx) {
    return axios.get('/api/get-jobs', { id: ctx.route.params.id })
    .then((res) => {
      return { job: res.data.jobs[0] }
    })
  },
  methods: {
    deleteJob () {
      axios.post('/api/update-job', { id: this.job.id, delete: true }, this)
      .then((res) => {
        if (res.data.success) {
          alert('Deleted successfully')
          this.$router.push('/account')
        }
      })
      .catch((err) => {
        if (err.response.status === 401) {
          this.error = 'You no longer have permission to do this. Please sign in again.'
        } else alert(err)
      })
    }
  }
}
</script>
