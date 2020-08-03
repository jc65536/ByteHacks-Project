<template>
  <div>
    <h2 class="text-teal-500 text-6xl text-center">
      Account Dashboard
    </h2>
    <p class="text-center">{{ $store.state.user.email }}</p>
    <div v-if="messages.length" class="text-center">
      <h3 class="text-4xl text-center border-t border-gray-500 mt-5 pt-4">Messages &amp; Applications</h3>
      <a href="#" @click="showMessages = !showMessages" class="underline">{{ showMessages ? 'Hide messages' : 'Show messages' }}</a>
      &middot;
      <a href="#" @click="showMyReplies = !showMyReplies" class="underline">{{ showMyReplies ? 'Hide sent messages' : 'Show sent messages' }}</a>
      &middot;
      <a href="#" @click="onlyShowApps = !onlyShowApps" class="underline">{{ onlyShowApps ? 'Show all messages' : 'Only show applications' }}</a>
      <div v-if="showMessages">
        <div v-for="msg in messages" :key="msg.id">
          <Card
            v-if="msg.sender_email !== $store.state.user.email && !onlyShowApps && !msg.subject.startsWith('APPLICATION')" 
            :toptag="'from ' + msg.sender_email"
            :subtitle="msg.subject"
            :replyemail="msg.sender_email"
            :replysubject="msg.subject"
            :replyerror="replyError"
            :replysuccess="replySuccess"
            @submitReply="reply"
          >
            {{ msg.message }}
          </Card>
          <Card
            v-else-if="msg.sender_email !== $store.state.user.email && msg.subject.startsWith('APPLICATION')" 
            :toptag="'from ' + msg.sender_email"
            topwarning="Application"
            :subtitle=" msg.subject"
            subtitle2="Please make sure to update your job listing with available positions."
            :replyemail="msg.sender_email"
            :replysubject="msg.subject"
            :replyerror="replyError"
            :replysuccess="replySuccess"
            @submitReply="reply"
          >
            {{ msg.message }}
          </Card>
          <Card
            v-else-if="msg.subject.startsWith('APPLICATION')" 
            :toptag="'to ' + msg.receiver_email"
            topwarning="You sent this application"
            :subtitle="msg.subject"
            @submitReply="reply"
          >
            {{ msg.message }}
          </Card>
          <Card
            v-else-if="showMyReplies && !onlyShowApps" 
            :toptag="'Sent to ' + msg.receiver_email"
            :subtitle="msg.subject"
            @submitReply="reply"
          >
            {{ msg.message }}
          </Card>
        </div>
      </div>
    </div>
    <div v-if="jobs.length">
      <h3 class="text-4xl text-center border-t border-gray-500 mt-5 pt-4">My Job Listings</h3>
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
      messages: [],
      replyError: '',
      replySuccess: '',
      showMessages: true,
      showMyReplies: false,
      onlyShowApps: false
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
      this.messages = res.data.all_messages
    })
  },
  methods: {
    reply (message, recipient, subject) {
      axios.post('/api/send-message', { recipient, message, subject: `Re: ${subject}` }, this)
      .then((res) => {
        this.replySuccess = 'Message sent!'
        this.replyError = ''
      })
      .catch((err) => {
        if (err.response.status === 400) {
          this.replyError = 'Unable to send message :('
          this.replySuccess = ''
        } else if (err.response.status === 401) {
          this.replyError = 'Please sign in again and try again.'
          this.replySuccess = ''
        }
      })
    }
  },
  beforeDestoy () {
    EventBus.$off('userChanged')
  }
}
</script>
