<template>
  <div class="home">
    <SignUp v-if="isSignup"/>
    <!-- Store Information -->
    <SignUpSteps v-if="isSignUpSteps"/>
  </div>
</template>

<script>
import SignUp from "@/components/signup/SignUp";
import SignUpSteps from "@/components/signup/SignUpSteps";

export default {
  name: "SignUpContainer",
  components: {SignUpSteps, SignUp},
  computed: {
    isSignup(){
      return this.$store.getters.isSignupForm;
    },
    isSignUpSteps() {
      return this.$store.getters.isformSteps;
    }
  },
}
</script>

<style scoped>
@import url('../../assets/css/style.css');

</style>
