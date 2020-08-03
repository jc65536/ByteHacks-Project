<template>
<div>
  <h2 class="text-teal-500 text-6xl text-center">
      Edit Job
    </h2>
    <JobForm :form='job' @submitForm="submit" />
</div>
</template>

<script>
import axios from '@/plugins/axios'
import JobForm from '@/components/JobForm'

export default {
  components: {
    JobForm
  },
  data () {
    return {
      job: {}
    }
  },
  asyncData (ctx) {
    return axios.get('/api/get-jobs', { id: ctx.route.params.id })
    .then((res) => {
      return { job: res.data.jobs[0] }
    })
  },
  methods: {
    submit (form) {
      axios.post('/api/update-job', form, this)
      .then((res) => {
        alert(`Job updated! Job id ${res.data.id}`)
      })
      .catch((err) => {
        if (err.response.status === 401) {
          alert('not authorized')
        }
        alert(err)
      })
    }
  }
}
</script>

<style scoped>
</style>
