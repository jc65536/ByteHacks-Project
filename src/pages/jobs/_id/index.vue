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
    <div v-if="$store.state.user && job.creator !== $store.state.user.email" class="text-center max-w-xs mx-auto">
      <textarea v-model="message" rows="5" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500"  placeholder="Send a message to the employer, or type your application here"></textarea>
      <p class="text-sm text-green-600">{{ messageSuccess }}</p>
      <p class="text-sm text-red-600">{{ messageError }}</p>
      <button class="bg-blue-600 rounded-md m-2 p-2 font-bold text-gray-200" @click="sendMessage">Send Message</button>
      <button class="bg-orange-600 rounded-md m-2 p-2 font-bold text-gray-200" @click="apply">Apply</button>
    </div>
    <p v-if="!$store.state.user" class="text-center text-gray-600 text-sm"><n-link to='/account/login'>Sign in to apply or send a message to the employer</n-link></p>
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
      error: '',
      message: '',
      messageSuccess: '',
      messageError: ''
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
      if (!confirm("Are you sure you want to delete this job?")) return
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
    },
    sendMessage (application) {

      const subject = application === true ? `APPLICATION for: ${this.job.title}` : `Job listing: ${this.job.title}` // why is this redundant condition necesarry, wtf js
  
      axios.post('/api/send-message', { recipient: this.job.creator, subject, message: this.message }, this)
      .then((res) => {
        this.messageSuccess = 'Sent successfully!'
        this.messageError = ''
        this.message = ''
      })
      .catch((err) => {
        if (err.response.status === 400) {
          this.messageError = 'Unable to send message :('
          this.messageSuccess = ''
        } else if (err.response.status === 401) {
          this.messageError = 'Please sign in again and try again.'
          this.messageSuccess = ''
        }
      })
    },
    apply () {
      if (!confirm("Are you sure you want to submit your application?")) return
      this.sendMessage(true)
    }
  }
}
</script>
