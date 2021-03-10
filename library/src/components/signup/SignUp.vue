<template>
  <div class="sign-up" v-loading="loading">
    <!-- Section SignUp -->
    <div class="d-lg-flex half">
      <div class="fixed_body left-side order-1 order-md-1 signup_image"><img src="../../assets/images/Left_Side.png" alt=""></div>
      <div class="contents order-2 order-md-2 right_side">
        <div class="container">
          <div class="row align-items-center justify-content-center signup_section">
            <div class="col-md-8">
              <div class="logo_div"><img src="../../assets/images/logo.png" alt=""></div>
              <h3>Create an account</h3>
              <p>Please create an account to continue using our service</p>
              <form @submit.prevent="submitForm" method="post" ref="signUpForm">
                <div class="form-group first">
                  <div class="row">
                    <div class="col-md-4">
                      <input type="radio" name="business_type" id="shopper" value="2" disabled="disabled"
                             class="form-input" v-model="businessType">
                      <span class="radio_label">Shopper</span>
                    </div>
                    <div class="col-md-4">
                      <input type="radio" name="business_type" id="localBusiness" class="form-input"
                             value="1" v-model="businessType">
                      <span class="radio_label">Local Business</span>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6">
                      <div class="social-login">
                        <a href="/accounts/apple/login/?process=login" class="twitter btn d-flex justify-content-center align-items-center">
                          <i class="fab fa-apple white"></i> Sign up with  Apple
                        </a>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="social-login">
                        <a href="/accounts/google/login/?process=login" class="twitter btn d-flex justify-content-center align-items-center">
                          <i class="fab fa-google white"></i> Sign up with  Google
                        </a>
                      </div>
                    </div>
                    <div class="col-md-10">
                      <span class="d-block text-center text-muted"> or </span>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-5">
                      <input type="text" :class="{'is-invalid': errors1.first_name}" class="form-control"
                             required v-model="business.first_name" id="first_name" placeholder="First name">
                      <div class="invalid-feedback" v-if="errors1.first_name">
                        {{ errors1.first_name }}
                      </div>
                    </div>
                    <div class="col-md-5">
                      <input type="text" :class="{'is-invalid': errors1.last_name}" class="form-control"
                             required v-model="business.last_name" id="last_name" placeholder="Last name">
                      <div class="invalid-feedback" v-if="errors1.last_name">
                        {{ errors1.last_name }}
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-10">
                      <input :class="{'is-invalid': errors1.username}" type="text" class="form-control"
                             required id="business_username" v-model="business.username"
                             name="username" placeholder="Username" @change="removeWhiteSpace">
                      <div class="invalid-feedback" v-if="errors1.username">
                        {{ errors1.username }}
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-10">
                      <input type="email" :class="{'is-invalid': errors1.email}" class="form-control" required id="email" name="email" v-model="business.email" placeholder="Email">
                      <div class="invalid-feedback" v-if="errors1.email">
                        {{ errors1.email }}
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-10">
                      <input type="text"
                        name="phone"
                        placeholder="Phone"
                        class="form-control"
                        maxlength="12"
                        v-model="business.phone_number"
                        :class="{'is-invalid': errors1.phone_number}"
                        required>
                      <div class="invalid-feedback" v-if="errors1.phone_number">
                        {{ errors1.phone_number }}
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-5">
                      <password-meter :class="{'is-invalid': errors1.password}" default-class="form-control" v-model="business.password" placeholder="Password" :badge="false"></password-meter>
                      <div class="invalid-feedback" v-if="errors1.password">
                        {{ errors1.password }}
                      </div>
                    </div>
                    <div class="col-md-5">
                      <input type="password" :class="{'is-invalid': errors1.confirm_password || business_password_invalid, 'is-valid': business_password_valid}" class="form-control" required id="confirm_password" v-model="business.confirm_password" name="confirm_password" placeholder="Confirm password">
                      <div class="invalid-feedback" v-if="errors1.confirm_password">
                        {{ errors1.confirm_password }}
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-10">
                      <select required :class="{'is-invalid': errors1.store_type}" class="form-control" v-model="business.category">
                        <option value="" disabled selected>Store Type</option>
                        <option v-for="c in categories" :value="c.id" :key="c.id">
                          {{ c.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-12">
                      <div class="form-check terms-checkbox">
                        <input class="form-check-input custom-input" type="checkbox" v-model="agree_terms" id="defaultCheck1">
                        <label class="form-check-label ml-2" for="defaultCheck1" style="display: inline-block !important;">
                          I have read and accepted Bloom Local <a href="https://www.bloomlocal.ca/terms-and-conditions/">terms and conditions.</a>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
                <input type="submit" value="Create an account" class="btn btn-block btn-primary submit signup-btn" :disabled="!agree_terms">
                <div class="d-flex mb-5 align-items-center">
                  <p class="signin-noti">Already have an account? <a href="/accounts/login/">Sign In</a></p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Section Store Information -->
    <!-- <StoreInformation v-if="isStoreInfo"/> -->
    <!-- Section Contact Details -->
    <!-- Section Import Products -->
    <!-- Confirmation -->
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'SignUp',
  data() {
    return {
      shopper: {
        username: "",
        first_name: "",
        last_name: "",
        phone_number: "",
        email: "",
        password: "",
        confirm_password: "",
      },
      business: {
        first_name: "",
        last_name: "",
        username: "",
        phone_number: "",
        email: "",
        password: "",
        confirm_password: "",
        business_address: "",
        apartment: "",
        business_phone: "",
        category: ""
      },
      businessType: "1",
      store_types: [
        {value: "food", text: "Food"},
        {value: "clothes", text: "Clothes"},
        {value: "electronics", text: "Electronics"},
      ],
      errors: {},
      errors1: {},
      loading: false,
      agree_terms: false
    }
  },
  created() {
    this.initRole(this.businessType);
    this.$store.dispatch('get_shop_categories');
  },
  computed: {
    categories() {
      return this.$store.getters.shopCategories;
    },
    business_password_valid() {
      return this.business.password === this.business.confirm_password && this.business.confirm_password !== '' && this.business.password !== '';
    },
    business_password_invalid() {
      return this.business.password !== this.business.confirm_password && this.business.confirm_password !== '' && this.business.password !== '';
    },
  },
  methods: {
    initRole: function (val) {
      axios.get(`/api/accounts/signup/initial/?role=${val}`)
    },
    removeWhiteSpace(){
      this.business.username = this.business.username.replace(/\s/g, '').toLowerCase();
    },
    submitForm(event) {
      event.preventDefault();
      let that = this;
      this.loading = true;
      event.preventDefault()
      this.errors1 = {};
      this.business.categories = [this.business.category];
      axios.post("/api/accounts/vendor/signup/", this.business).then(function (res) {
        that.loading = false;
        that.$store.dispatch('singUpFormField', res.data)
        that.$store.dispatch('nextStep', 'steps')
      }).catch((errors) => {
        that.loading = false;
        // eslint-disable-next-line no-debugger
        debugger
        let data = errors.response.data;
        if (data) {
          that.errors1 = {}
          Object.keys(data).forEach(key => {
            that.errors1[key] = data[key].join(", ");
          })
        }
      })
    }
  }
}
</script>
<style>
.parsley-errors-list {
  padding: 0;
  list-style: none;
  margin: 3px 2px;
  color: red;
}
.parsley-required{
  color: red;
}
</style>
