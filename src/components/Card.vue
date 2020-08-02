<template>
<div>
  <div class="w-full max-w-xs mx-auto my-10 bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
    <div class="text-white font-bold inline-block text-xs bg-gray-500 px-1 rounded-lg">{{ toptag }}</div>
    <span class="mb-2">
      <div class="text-gray-900 font-bold text-xl my-2">{{ title }}</div>
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
    <p class="text-sm m-2">At {{ location }}</p>
  </div>
</div>
</template>

<script>
import DateTime from 'luxon/src/datetime.js'

function dtString (iso) {
  if (!iso) return 'N/A'
  const dt = DateTime.fromISO(iso)
  const suffix = dt.hour >= 12 ? 'PM' : 'AM'
  const hour = (dt.hour + 11) % 12 + 1 // Convert to 12-hour (couldn't figure out how to do this wit luxon)
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
    'location'
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
