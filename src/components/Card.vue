<template>
<div>
  <div :class="['w-full max-w-xs mx-auto bg-white shadow-md rounded px-8', compact ? 'my-2 py-1' : 'my-4 pt-6 pb-8']">
    <p class="text-sm text-orange-600 font-bold">{{ topwarning }}</p>
    <div :class="['text-white font-bold text-xs bg-gray-500 rounded-lg inline-block', compact ? 'py-0 px-1' : 'px-1']">{{ toptag }}</div>
    <span class="block" v-if="!compact">
      <div v-if="titlelink" class="text-gray-900 font-bold text-xl my-2 border-b-2 border-blue-700 inline"><n-link :to="titlelink">{{ title }}</n-link></div>
      <div v-else class="text-gray-900 font-bold text-xl my-2">{{ title }}</div>
    </span>
    <p class="text-gray-600 text-sm">{{ subtitle }}</p>
    <p class="text-gray-600 text-sm">{{ subtitle2 }}</p>
    <p :class="['text-justify', 'text-sm', 'font-sans', !compact ? 'my-3' : 'm-0']">
      <slot></slot>
    </p>
    <div class="text-sm font-bold text-gray-600">
      <p v-if="startdate">Starts {{ convertedStartdate }}</p>
      <p v-if="enddate">Ends {{ convertedEnddate }}</p>
    </div>
    <p v-if="location" class="text-sm my-2">At {{ location }}</p>
    <n-link v-if='editlink' :to='editlink' class="text-sm my-2 border-2 border-blue-700 p-1 rounded-md mr-1 hover:text-blue-600">Edit</n-link>
    <n-link v-if='deletelink' :to='deletelink' class="text-sm my-2 border-2 border-blue-700 p-1 rounded-md mr-1 hover:text-blue-600">Delete</n-link>
    <n-link v-if="applylink" :to="applylink" class="text-sm my-2 border-2 border-blue-700 p-1 rounded-md mr-1 hover:text-blue-600">Apply</n-link>
    <a href="#" @click.prevent="showBottom = !showBottom" class="underline text-green-700 font-bold">{{ showbottomtext }}</a>
    <button v-if="replyemail" @click="showReplyBox = !showReplyBox" :class="['text-sm border-2 border-blue-700 p-1 rounded-md mr-1 hover:text-blue-600', !compact? 'my-2' : ' ']">{{ showReplyBox ? 'Hide reply' : 'Reply' }}</button>
    <button v-if="closeid" @click="$emit('submitClose', closeid)" :class="['text-sm border-2 border-blue-700 p-1 rounded-md mr-1 hover:text-blue-600', !compact? 'my-2' : ' ']">Accept application</button>
    <div v-if="showReplyBox">
      <textarea v-model="message" class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-teal-500"  placeholder="Reply here..."></textarea>
      <p class="text-sm text-green-600">{{ replysuccess }}</p>
      <p class="text-sm text-red-600">{{ replyerror }}</p>
      <button class="bg-blue-600 rounded-md m-1 p-1 font-bold text-gray-200" @click="$emit('submitReply', message, replyemail, replysubject, replyid)">Send</button>
    </div>
    <div v-if="showBottom">
      <slot name="bottom-content"></slot>
    </div>
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
  data () {
    return {
      showReplyBox: false,
      showBottom: false
    }
  },
  props: [
    'title',
    'compact',
    'subtitle',
    'subtitle2',
    'toptag',
    'topwarning',
    'startdate',
    'enddate',
    'location',
    'editlink',
    'deletelink',
    'titlelink',
    'applylink',
    'replyerror',
    'replysuccess',
    'replyemail',
    'replysubject',
    'replyid',
    'showbottomtext',
    'closeid'
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
