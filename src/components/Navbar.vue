<template>
  <div>
    <nav class="flex items-center justify-between flex-wrap bg-teal-500 p-6">
      <div class="flex items-center flex-shrink-0 text-white mr-6">
        <!-- <svg class="fill-current h-8 w-8 mr-2" width="54" height="54" viewBox="0 0 54 54" xmlns="http://www.w3.org/2000/svg"><path d="M13.5 22.1c1.8-7.2 6.3-10.8 13.5-10.8 10.8 0 12.15 8.1 17.55 9.45 3.6.9 6.75-.45 9.45-4.05-1.8 7.2-6.3 10.8-13.5 10.8-10.8 0-12.15-8.1-17.55-9.45-3.6-.9-6.75.45-9.45 4.05zM0 38.3c1.8-7.2 6.3-10.8 13.5-10.8 10.8 0 12.15 8.1 17.55 9.45 3.6.9 6.75-.45 9.45-4.05-1.8 7.2-6.3 10.8-13.5 10.8-10.8 0-12.15-8.1-17.55-9.45-3.6-.9-6.75.45-9.45 4.05z"/></svg> -->
        <n-link to='/'><span class="font-semibold text-xl tracking-tight">Aid App</span></n-link>
      </div>
      <div class="block lg:hidden">
        <button class="flex items-center px-3 py-2 border rounded text-teal-200 border-teal-400 hover:text-white hover:border-white">
          <svg class="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><title>Menu</title><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"/></svg>
        </button>
      </div>
      <div class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
        <div class="text-sm lg:flex-grow">
          <div class="block mt-4 lg:inline-block lg:mt-0 hover:text-white mr-4 dropdown">
            <button class="text-teal-200 rounded inline-flex items-center">
              <span class="mr-1">Jobs</span>
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/> </svg>
            </button>
            <ul class="dropdown-menu absolute hidden text-gray-700 pt-1">
              <li class=""><n-link to='/jobs' class="bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap">Find a job</n-link></li>
              <li class=""><n-link to='/jobs/add' class="bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap rounded-b ">Add a new job</n-link></li>
            </ul>
          </div>
          <div class="block mt-4 lg:inline-block lg:mt-0 hover:text-white mr-4 dropdown">
            <button class="text-teal-200 rounded inline-flex items-center">
              <span class="mr-1">Get Help</span>
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/> </svg>
            </button>
            <ul class="dropdown-menu absolute hidden text-gray-700 pt-1">
              <li class=""><n-link to='/help/soup' class="bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap">Soup kitchens &amp; Shelters</n-link></li>
              <li class=""><n-link to='/help' class="bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap rounded-b ">Helpful resources</n-link></li>
            </ul>
          </div>
          <div class="block mt-4 lg:inline-block lg:mt-0 hover:text-white mr-4 dropdown">
            <button class="text-teal-200 rounded inline-flex items-center">
              <span class="mr-1">Trade</span>
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/> </svg>
            </button>
            <ul class="dropdown-menu absolute hidden text-gray-700 pt-1">
              <li class=""><n-link to='/trade' class="bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap">Look for trades</n-link></li>
              <li class=""><n-link to='/trade/request' class="bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap">Request an item</n-link></li>
              <li class=""><n-link to='/trade/add' class="bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap rounded-b ">Add an item</n-link></li>
            </ul>
          </div>
        </div>
      <div v-if="$store.state.user && $store.state.user.email">
        <n-link to="/account" class="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4">
          My account
        </n-link>
        <a href="#" class="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0" @click="$store.dispatch('logout')">Sign out</a>
      </div>
      <div v-else>
        <n-link to="/account/login" class="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4">
          Sign in
        </n-link>
        <n-link to='/account/create' class="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0">Create account</n-link>
      </div>
      </div>
    </nav>
  </div>
</template>

<style scoped>
.dropdown:hover .dropdown-menu {
  display: block;
}
</style>
