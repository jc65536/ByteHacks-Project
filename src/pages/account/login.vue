<template>
  <div>
    <div class="w-full max-w-xs mx-auto my-10">
      <h2 class="text-2xl text-center m-5">Sign in</h2>
      <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Email
          </label>
          <input v-model="form.email" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="email" placeholder="someone@example.com">
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Password
          </label>
          <input v-model="form.password" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" type="password" placeholder="******************">
          <p class="text-sm text-red-600">{{ error }}</p>
        </div>
        <div class="flex items-center justify-between">
          <button class="bg-teal-400 hover:bg-teal-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" @click="submit">
            Sign In
          </button>
          <n-link to='/account/create' class="inline-block align-baseline font-bold text-sm text-teal-400 hover:text-teal-600">
            Create account
          </n-link>
          <!-- <n-link to='/account/create' class="inline-block align-baseline font-bold text-sm text-teal-400 hover:text-teal-600 my-5">
            Create account
          </n-link> -->
        </div>
      </form>
      <p class="text-center text-sm text-gray-500">
        Don't have an account?
        <n-link to='/account/create'><u>Create one!</u></n-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      form: {},
      error: ''
    }
  },
  methods: {
    submit () {
      this.$store.dispatch('login', this.form)
      .then((res) => {
        if (res.authenticated) this.$router.push('/')
        else if (res.message.response.status === 401) this.error = 'Incorrect email or password'
        else alert(res.message)
      })
    }
  }
}
</script>
