<template>
  <div>
    <h2 class="text-teal-500 text-6xl text-center">
      Find a Job Here
    </h2>
    <Card
      title="Farm worker"
      toptag="1 position left"
      subtitle="By Strawberry Farms"
      subtitle2="pays $5/hour"
      location="somewhere"
      startdate="2020-08-18T10:15:00.000-07:00"
    >
      This a really great, well-paying job. You should totally get it.
    </Card>
  </div>
</template>

<script>
// import axios from '@/plugins/axios'
import Card from '@/components/Card'

export default {
  components: {
    Card
  }
}
</script>
