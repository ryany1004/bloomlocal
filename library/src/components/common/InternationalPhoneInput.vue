<template>
  <vue-phone-number-input ref="phone_input" id="phone" @update="onUpdate"
                          v-model="phone" :required="required" />
</template>

<script>
import {parsePhoneNumberFromString} from "libphonenumber-js";

export default {
  name: "InternationalPhoneInput",
  props: {
    value: {
      type: String,
      default: ''
    },
    required: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      phone: "",
    }
  },
  mounted() {
    let parsed = parsePhoneNumberFromString(this.value);
    this.$refs.phone_input.countryCode = parsed.country;
    this.$refs.phone_input.phoneNumber = this.value;
  },
  methods: {
    onUpdate(payload) {
      this.$emit('input', payload.formatInternational || '');
    },
  }
}
</script>

<style scoped>

</style>
