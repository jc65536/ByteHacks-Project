<template>
<div>
  <div class="w-full max-w-xs mx-auto my-10 bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
    <div class="text-white font-bold text-xs bg-gray-500 px-1 rounded-lg inline-block">{{ toptag }}</div>
    <span class="my-2 block">
      <div v-if="titlelink" class="text-gray-900 font-bold text-xl my-2 border-b-2 border-blue-700 inline"><n-link :to="titlelink">{{ title }}</n-link></div>
      <div v-else class="text-gray-900 font-bold text-xl my-2">{{ title }}</div>
    </span>
    <p class="text-gray-600 text-sm">{{ subtitle }}</p>
    <p class="text-gray-600 text-sm">{{ subtitle2 }}</p>
    <p class="text-justify text-sm font-sans my-3">
      <slot></slot>
    </p>
    <div class="text-sm font-bold text-gray-600">
      <p>Starts {{ convertedStartdate }}</p>
      <p>Ends {{ convertedEnddate }}</p>
    </div>
    <p class="text-sm my-2">At {{ location }}</p>
    <n-link v-if='editlink' :to='editlink' class="text-sm my-2 border-2 border-blue-700 p-1 rounded-md mr-1 hover:text-blue-600">Edit</n-link>
    <n-link v-if='deletelink' :to='deletelink' class="text-sm my-2 border-2 border-blue-700 p-1 rounded-md mr-1 hover:text-blue-600">Delete</n-link>
    <n-link v-if="applylink" :to="applylink" class="text-sm my-2 border-2 border-blue-700 p-1 rounded-md mr-1 hover:text-blue-600">Apply</n-link>
  </div>
</div>
</template>

<script>
import DateTime from 'luxon/src/datetime.js'

function dtString (iso) {
  if (!iso) return 'N/A'
  const dt = DateTime.fromISO(iso)
  const suffix = dt.hour >= 12 ? 'PM' : 'AM'
  const hour = (dt.hour + 11) % 12 + 1 // Convert to 12-hour (couldn't figure out how to do this with luxon)
  return `${dt.monthLong} ${dt.day}, ${hour}:${dt.minute} ${suffix}`
}

export default {
  props: [
    'title',
    'subtitle',
    'subtitle2',
    'toptag',
    'startdate',
    'enddate',
    'location',
    'editlink',
    'deletelink',
    'titlelink',
    'applylink'
  ],
  computed: {
    convertedStartdate () {
      return dtString(this.startdate)
    },
    convertedEnddate () {
      return dtString(this.enddate)
    }
  }
}
</script>

<style scoped>
</style>
