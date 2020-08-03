<template>
  <div class.txt= "txt">
      <h2 class="text-teal-500 text-6xl text-center">
        Create a new job
      </h2>
      <h3 class="text-center text-teal-500 text-xl">
        Answer the questions below and type the answers in the box below.  Once you are done, click on Submit.
      </h3>
      <JobForm @submitForm="submit" :error="error" />
  </div>
</template>

<script>
import JobForm from '@/components/JobForm'
import axios from '@/plugins/axios'

export default {
  components: {
    JobForm
  },
  data () {
    return {
      error: ''
    }
  },
  mounted () {
    if (!this.$store.getters.isValidJWT()) this.$router.push('/account/login')
  },
  methods: {
    submit (form) {
      axios.post('/api/add-job', form, this)
      .then((res) => {
        alert(`Job posted! Job id is ${res.data.id}`)
        this.$router.push('/account')
      })
      .catch((err) => {
        console.log(err)
        if (err.response.status === 401) this.error = 'Your session has been invalidated. Please sign in again.'
        else if (err.response.status === 400) this.error = 'Please make sure all fields are valid'
        else alert(err)
      })
    }
  }
}
</script>

<style scoped>
</style>
