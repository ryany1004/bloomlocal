<template>
  <div class="sign-up">
    <!-- Section SignUp -->
    <div class="d-lg-flex half">
      <div class="fixed_body left-side order-1 order-md-1 signup_image"><img src="../../assets/images/Left_Side.png" alt=""></div>
      <div class="contents order-2 order-md-2 right_side">
        <div class="container">
          <div class="row align-items-center justify-content-center signup_section">
            <div class="col-md-8">
              <div class="logo_div"><img src="../../assets/images/logo.png" alt=""></div>
              <h3>Create an account</h3>
              <p>Plese create an account to continue using our service</p>
              <form @submit.prevent="submitForm" method="post" ref="signUpForm" data-parsley-validate>
                <div class="form-group first">
                  <div class="row">
                    <div class="col-md-6">
                      <input type="radio" name="business_type" id="shopper" value="shopper" class="form-input" v-bind:checked="businessType" v-model="businessType">
                      <span class="radio_label">Shopper</span>
                    </div>
                    <div class="col-md-6">
                      <input type="radio" name="business_type" id="localBusiness" class="form-input" value="localBusiness" v-model="businessType">
                      <span class="radio_label">Local Business</span>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6">
                      <div class="social-login">
                        <a href="javascript:void(0)" class="twitter btn d-flex justify-content-center align-items-center">
                          <span class="icon-apple mr-3"></span> Login with  Apple
                        </a>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="social-login">
                        <a href="javascript:void(0)" class="twitter btn d-flex justify-content-center align-items-center">
                          <span class="icon-google mr-3"></span> Login with  Google
                        </a>
                      </div>
                    </div>
                    <span class="d-block text-center text-muted"> or </span>
                  </div>
                  <div class="row">
                    <div class="col-md-6">
                      <input type="text" name="fname" placeholder="First Name" class="form-control"
                        v-model="fname"
                        v-bind:class="{'is-invalid': (errors ==true && (fname == '' || errorMsg.fname))}"
                        data-parsley-required-message="First name is required."
                        required
                       >
                    </div>
                    <div class="col-md-6">
                      <input type="text"
                        name="lname"
                        placeholder="Last Name"
                        class="form-control"
                        v-model="lname"
                        v-bind:class="{'is-invalid': (errors ==true && lname == '')}"
                        data-parsley-required-message="Last name is required."
                        required>
                    </div>
                  </div>
                  <div class="row">
                      <div class="col-md-12">
                      <input type="text"
                        name="uname"
                        placeholder="Username"
                        class="form-control"
                        v-model="uname"
                        @change="removeWhiteSpace"
                        v-bind:class="{'is-invalid': (errors ==true && uname == '')}"
                        data-parsley-required-message="username is required."
                        required>
                    </div>
                  </div>
                  <div class="row">
                      <div class="col-md-12">
                      <input type="email"
                        name="email"
                        placeholder="Email"
                        class="form-control"
                        v-model="email"
                        v-bind:class="{'is-invalid': (errors ==true && email == '')}"
                        data-parsley-required-message="Email is required."
                        required >
                    </div>
                  </div>
                  <div class="row">
                      <div class="col-md-12">
                      <input type="text"
                        name="phone"
                        placeholder="Phone"
                        class="form-control"
                        maxlength="12"
                        v-model="phone"
                        v-bind:class="{'is-invalid': (errors ==true && phone == '')}"
                        data-parsley-required-message="Phone number is required."
                        required>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6">
                      <input type="password"
                        name="password"
                        id="formpassword"
                        placeholder="Password"
                        class="form-control"
                        v-model="password"
                        v-bind:class="{'is-invalid': (errors ==true && password == '')}"
                        data-parsley-required-message="Password is required."
                        required>
                    </div>
                    <div class="col-md-6">
                      <input type="password"
                        name="cpassword"
                        placeholder="Confirm Password"
                        class="form-control"
                        v-model="cpassword"
                        v-bind:class="{'is-invalid': (errors ==true && cpassword == '')}"
                        data-parsley-equalto="#formpassword"
                        required>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-12">
                      <select class="form-control" required data-parsley-required-message="Store Type is required." v-model="storeType">
                        <option value="">Store Type</option>
                        <option v-for="(store, index) in storeTpes" :value="store.id" :key="index">{{ store.name }}</option>
                      </select>
                    </div>
                  </div>
                </div>
                <input type="submit" value="Create an Account" class="btn btn-block btn-primary submit">
                <span class="d-block text-center my-4 text-muted">or</span>
                <div class="d-flex mb-5 align-items-center">
                  <span class="already_account">Already have an account? <a href="javascript:void(0)">Sign In</a></span>
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
// Import All the four Component
import $ from 'jquery'
export default {
  name: 'SignUp',
  components: {

  },
  data() {
    return {
      businessType: '',
      fname: '',
      lname: '',
      uname: '',
      email: '',
      phone: '',
      password: '',
      cpassword: '',
      storeType: '',
      errors: false
    }
  },
  mounted(){
    let form = this.$refs.signUpForm
    // $(form).parsley().destroy()
    $(form).parsley().reset()
    // Get Form Field Values
    let formFields = this.$store.getters.signUpFormFields;
    this.businessType = (formFields.businessType) ? formFields.businessType : 'shopper'
    this.fname = (formFields.fname) ? formFields.fname : ''
    this.lname = (formFields.lname) ? formFields.lname : ''
    this.uname = (formFields.uname) ? formFields.uname : ''
    this.email = (formFields.email) ? formFields.email : ''
    this.phone = (formFields.phone) ? formFields.phone : ''
    this.password = (formFields.password) ? formFields.password : ''
    this.cpassword = (formFields.cpassword) ? formFields.cpassword : ''
    this.storeType = (formFields.storeType) ? formFields.storeType : ''
  },
  computed: {
    storeTpes() {
      return this.$store.state.storeType
    }
  },
  methods: {
    removeWhiteSpace(){
      this.uname = this.uname.replace(/\s/g, '').toLowerCase();
    },
    submitForm(event){
      event.preventDefault();

      let form = this.$refs.signUpForm

      let fields = {
        businessType: this.businessType,
        fname: this.fname,
        lname: this.lname,
        uname: this.uname,
        email: this.email,
        phone: this.phone,
        password: this.password,
        cpassword: this.cpassword,
        storeType: this.storeType,
      }
      this.$store.dispatch('singUpFormField', fields)
      this.$store.dispatch('nextStep', 'steps')

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
