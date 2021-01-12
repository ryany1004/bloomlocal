<template>
  <div v-loading="loading">

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Receipt",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    uuid: {
      type: String,
      required: true
    }
  },
  data: function () {
    return {
      loading: false,
      order: {}
    }
  },
  watch: {
    uuid: {
      immediate: true,
      handler(val) {
        this.get_order(val);
      }
    }
  },
  methods: {
    get_order() {
      let that = this;
      that.loading = true;
      axios.get(`/api/order/${this.uuid}/details/`).then((res) => {
        that.order = res.data;
        that.loading = false
      }).catch(() => {
        alert("Unable to load data");
      })
    }
  }
}
</script>

<style scoped>

</style>
