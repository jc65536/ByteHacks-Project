<template>
  <div>
      <h2 class="text-teal-500 text-6xl text-center">
        Create a new job
      </h2>
      <h3 class="text-center text-lg">
        Fill out the form below to create a job listing. Prospective employees will be able to see your email and send messages and applications to you.
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
        this.$router.push('/jobs/' + res.data.id)
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
