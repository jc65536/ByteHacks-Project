<template>
  <div>
    <Navbar />
    <div class="container">
      <Nuxt />
    </div>
  </div>
</template>

<script>
import { EventBus } from '@/plugins/event'
import axios from '@/plugins/axios'
import Navbar from '../components/Navbar'

export default {
  components: {
    Navbar
  },
  created () {
    // Check for saved jwt and verify it
    const jwt = localStorage.getItem('jwt')
    if (jwt && this.$store.getters.isValidJWT(jwt)) {
      this.$store.commit('setJWT', jwt)
      this.$store.commit('setUserData', {
        email: this.$store.getters.JWTProperty('sub'),
        name: this.$store.getters.JWTProperty('name')
      })

      axios.post('/api/verify-token', {}, this)
      .catch((err) => {
        if (err.response.status === 401) this.$store.dispatch('logout')
      })
    }
    EventBus.$emit('userChanged')
  }
}
</script>

<style>
</style>
