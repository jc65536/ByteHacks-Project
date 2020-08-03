<template>
  <div>
    <div class="text-center m-10">
      <h1 class="text-center text-5xl m-5">
        Aid App
      </h1>
      <p v-if="$store.state.user && $store.state.user.name">
        Hello, {{ $store.state.user.name }}
      </p>
      <p>
        Welcome to Great Depression Aid app. Find jobs, trade, and more.
      </p>
      <p>
        Created for Byte Hacks 2020
      </p>
      <p class="my-5">
        The Great Depression is tough. That's why we created this app for you. Do you need a job quickly but don't want to spend time knocking on doors or filling out time-consuming applications or interviews? <n-link to='/jobs'>Look here!</n-link> Need info about government aid programs, employment agencies, and other helpful organizations and resources? <n-link to='/help'>We've got you covered!</n-link>
      </p>
      <p>We have more features coming soon - for example, do you need something but don't have the money? You can trade for it</p>
    </div>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
  a {
    color: dodgerblue;
    text-decoration: underline;
  }
</style>
