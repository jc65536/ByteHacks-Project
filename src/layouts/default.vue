<template>
  <div>
    <Navbar />
    <div class="container">
      <Nuxt />
    </div>
  </div>
</template>

<script>
import Navbar from '../components/Navbar'

export default {
  components: {
    Navbar
  },
  mounted () {
    // Check for saved jwt and verify it
    const jwt = localStorage.getItem('jwt')
    if (jwt && this.$store.getters.isValidJWT(jwt)) {
      this.$store.commit('setJWT', jwt)
      this.$store.commit('setUserData', {
        email: this.$store.getters.JWTProperty('sub'),
        name: this.$store.getters.JWTProperty('name')
      })
    }
  }
}
</script>

<style>
</style>
