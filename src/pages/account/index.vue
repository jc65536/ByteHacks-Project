<template>
  <div>
    <h2 class="text-teal-500 text-6xl text-center">
      Account Dashboard
    </h2>
    <p class="text-center">{{ $store.state.user.email }}</p>
  </div>
</template>

<script>
export default {
  mounted () {
    if (!this.$store.getters.isValidJWT()) this.$router.push('/account/login')
  }
}
</script>
