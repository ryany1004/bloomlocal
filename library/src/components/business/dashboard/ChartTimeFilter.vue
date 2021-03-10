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
  name: "ChartTimeFilter",
  props: {
    value: {
      type: String,
      default: 'day'
    }
  },
  data() {
    return {
      time_range: [
        {value: 'by_day', text: "By Day"},
        {value: 'by_week', text: "By Week"},
        {value: 'by_month', text: "By Month"},
      ],
    }
  },
  computed: {
    selected_time() {
      if (this.value == "by_day") {
        return "By Day";
      } else if (this.value == "by_week") {
        return "By Week";
      } else {
        return "By Month";
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
