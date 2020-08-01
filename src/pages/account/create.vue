<template>
  <div>
    <div class="w-full max-w-lg mx-auto my-10">
      <h2 class="text-2xl text-center m-5">Create Account</h2>
      <p class="text-center mb-5">Create an account to list jobs, trade, and more</p>
      <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Email
          </label>
          <input v-model="form.email" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="email" placeholder="someone@example.com">
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Your name
          </label>
          <input v-model="form.name" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" placeholder="Ex. John Smith">
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Password
          </label>
          <input v-model="form.password" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="password" placeholder="******************">
        </div>
        <div class="flex items-center justify-between">
          <button class="bg-teal-400 hover:bg-teal-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" @click="submit">
            Create Account
          </button>
          <n-link to='/account/login' class="inline-block align-baseline font-bold text-sm text-teal-400 hover:text-teal-600" href="#">
            Sign in
          </n-link>
        </div>
        <div class="md:flex md:items-center">
          <div class="md:w-1/3"></div>
    <div class="md:w-2/3">
    </div>
  </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      form: {}
    }
  },
  methods: {
    submit () {
      this.$store.dispatch('register', this.form)
      .then((res) => {
        if (res.registered) this.$router.push('/')
        else alert(res.message)
      })
    }
  }
}
</script>
