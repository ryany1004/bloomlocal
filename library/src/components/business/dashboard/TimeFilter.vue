<template>
  <div class="dropdown time-filter">
    <a class="dropdown-toggle" href="#" role="button" id="dropdownMenuLink1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
      {{ selected_time }}
    </a>
    <div class="dropdown-menu" aria-labelledby="dropdownMenuLink1">
      <a v-show="t.value != value" class="dropdown-item" href="javascript:void(0)" v-for="t in time_range" :key="t.value"
        @click="handleClick(t)">
        {{ t.text }}
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "TimeFilter",
  props: {
    value: {
      type: String,
      default: 'today'
    }
  },
  data() {
    return {
      time_range: [
        {value: 'today', text: "Today"},
        {value: 'this_week', text: "This week"},
        {value: 'this_month', text: "This month"},
      ],
    }
  },
  computed: {
    selected_time() {
      if (this.value == "today") {
        return "Today";
      } else if (this.value == "this_week") {
        return "This week";
      } else {
        return "This month";
      }
    }
  },
  methods: {
    handleClick(t) {
      this.$emit('input', t.value);
    }
  }
}
</script>

<style lang="scss">
.time-filter {
  font-size: 14px;
  a {
    font-size: 14px;
    color: #919EAB;
    text-decoration: none !important;
  }
}
</style>
