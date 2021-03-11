<template>
    <div v-loading="loading">
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <input type="email"
                        name="business_email"
                        placeholder="Business Email"
                        class="form-control"
                        v-model="business_email"
                        @input="checkValidation"
                        v-bind:class="{'is-invalid': (errors ==true && (business_email == '' || errorMsg.business_email))}"
                        required />
                    <div class="invalid-feedback">{{ errorMsg.business_email }}</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <input type="text"
                        name="business_phone"
                        placeholder="Business Phone Number"
                        class="form-control"
                        v-model="business_phone"
                        @input="checkValidation"
                        v-bind:class="{'is-invalid': (errors ==true && (business_phone == '' || errorMsg.business_phone))}"
                        required
                        />
                    <div class="invalid-feedback">{{ errorMsg.business_phone }}</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <input type="url"
                        name="business_website"
                        placeholder="Business Website"
                        class="form-control"
                        v-model="business_website"
                        @input="checkValidation"
                        @blur="validSite()"
                        v-bind:class="{'is-invalid': (errors ==true && (business_website == '' || errorMsg.business_website))}"
                        required/>
                    <div class="invalid-feedback">{{ errorMsg.business_website }}</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
<!--                    <input type="text"-->
<!--                        name="business_address"-->
<!--                        placeholder="Business address"-->
<!--                        class="form-control"-->
<!--                        v-model="business_address"-->
<!--                        @input="checkValidation"-->
<!--                        v-bind:class="{'is-invalid': (errors ==true && (business_address == '' || errorMsg.business_address))}"-->
<!--                        required/>-->
                    <place-autocomplete-field
                      v-model="business_address" placeholder="Business address" class=""
                      @change="checkValidation()"
                      :class="{'is-invalid': (errors ==true && (business_address == '' || errorMsg.business_address))}"
                      name="business_address" :api-key="googleMapsApiKey"
                      v-place-autofill:street="business_address"
                      v-place-autofill:state="state"
                      v-place-autofill:zipcode="zipcode"></place-autocomplete-field>
                    <div class="invalid-feedback">{{ errorMsg.business_address }}</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="form-group">
                    <input type="text"
                        name="state"
                        placeholder="Province"
                        class="form-control"
                        v-model="state"
                        @input="checkValidation"
                        v-bind:class="{'is-invalid': (errors ==true && (state == '' || errorMsg.state))}"
                        required/>
                    <div class="invalid-feedback">{{ errorMsg.state }}</div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-group">
                    <input type="text"
                    name="zipcode"
                    placeholder="Postal code"
                    class="form-control"
                    v-model="zipcode"
                    @input="checkValidation"
                    v-bind:class="{'is-invalid': (errors ==true && (zipcode == '' || errorMsg.zipcode))}"
                    required/>
                    <div class="invalid-feedback">{{ errorMsg.zipcode }}</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <ul class="list-inline next_btn_div">
                    <li><button type="button" class="default-btn next-step" v-on:click="nextStep">Next: Import Products</button></li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'ContactDetail',
    props: {
      googleMapsApiKey: {
        type: String
      }
    },
    data(){
        return {
            business_email: '',
            business_phone: '',
            business_website: '',
            business_address: '',
            state: '',
            zipcode: '',
            errors: false,
            errorMsg: {business_email: '', business_phone: '', business_website: '', business_address: '', state: '', zipcode: ''},
            loading: false
        }
    },
    mounted() {
        let formFields = this.$store.getters.getContactDetail;
        if(formFields) {
            this.business_email = (formFields && formFields.business_email) ? formFields.business_email : ''
            this.business_phone = (formFields && formFields.business_phone) ? formFields.business_phone : ''
            this.business_website = (formFields && formFields.business_website) ? formFields.business_website : ''
            this.business_address = (formFields && formFields.business_address) ? formFields.business_address : ''
            this.state = (formFields && formFields.state) ? formFields.state : ''
            this.zipcode = (formFields && formFields.zipcode) ? formFields.zipcode : ''
        }
    },
    methods: {
        validSite() {
          if (!this.business_website.startsWith("http")) {
            this.business_website = 'http://' + this.business_website;
          }
        },
        checkValidation() {
            this.validate()
        },
        validate() {
            let errors = [];
            if(this.business_email == '') {
                this.errors = true
                this.errorMsg.business_email = "Email is required"
                errors.push('business_email')
            } else if(/^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$/.test(this.business_email) == false) {
                this.errors = true;
                this.errorMsg.business_email = "Enter valid Email"
                errors.push('business_email')
            } else {
                this.errorMsg.business_email = ''
            }
            if(this.business_phone == '') {
                this.errors = true
                this.errorMsg.business_phone = "Phone is required"
                errors.push('business_email')
            } else if(/^\d{10}$/.test(this.business_phone) == false) {
                this.errors = true;
                this.errorMsg.business_phone = "Enter valid Phone"
                errors.push('phone')
            } else {
                this.errorMsg.business_phone = '';
            }
            // Website Validate
            let regex = /^((http(s)?):\/\/)([wW]{3}\.)?[a-zA-Z0-9\-.]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?\/?$/g
            if(this.business_website == '') {
                this.errors = true;
                this.errorMsg.business_website = "Website is required.";
                errors.push('website')
            }else if(!this.business_website.match(regex)) {
                this.errors = true;
                this.errorMsg.business_website = "Enter valid website"
                errors.push('website')
            } else {
                this.errorMsg.business_website = ''
            }
            // business_address
            if(this.business_address == '') {
                this.errors = true;
                this.errorMsg.business_address = "Business address is required."
                errors.push('business_address')
            } else {
                this.errorMsg.business_address = ''
            }
            // State String empty Validate
            if(this.state == '') {
                this.errors = true;
                this.errorMsg.state = "Province is required."
                errors.push('state')
            } else {
                this.errorMsg.state = ''
            }
            // Zipcode Validate
            if(this.zipcode == '') {
                this.errors = true;
                this.errorMsg.zipcode = "Postal code is required."
                errors.push('zipcode')
            } else {
                this.errorMsg.zipcode = ''
            }
            // Check the input fields is not empty
            if (errors.length) {
                return false
            } else {
                return true
            }
        },
        nextStep() {
            // Check validation before next steps
            if(this.validate()) {
                let formFileds = {
                    business_email: this.business_email,
                    business_phone: this.business_phone,
                    business_website: this.business_website,
                    business_address: this.business_address,
                    state: this.state,
                    zipcode: this.zipcode
                };
                // Proceed Next Form
                let step = this.$store.getters.formSteps;
                if( step >= 1 ||  step <= 4 ) {
                    step +=1;
                    let storeInfo = this.$store.getters.getStoreInfo;
                    let data = {
                      business_email: this.business_email,
                      business_phone: this.business_phone,
                      business_website: this.business_website,
                      business_address: this.business_address,
                      state: this.state,
                      zipcode: this.zipcode,
                      name: storeInfo.name,
                      description: storeInfo.description,
                      tags: storeInfo.tags,
                      delivery_type: storeInfo.delivery_type
                    }
                    let that = this;
                    this.loading = true;
                    axios.patch("/api/business/shop/update/", data).then(() => {
                      that.loading = false;
                      that.$store.dispatch('nextProcess', step)
                      that.$store.dispatch('contactDetail', formFileds)
                    }).catch(errors => {
                      that.loading = false;
                      let data = errors.response.data
                      if (data) {
                        that.errorMsg = {}
                        that.errors = true;
                        Object.keys(data).forEach(key => {
                          that.errorMsg[key] = data[key].join(", ");
                        })
                      }
                    })
                }
            }
        }
    }
}
</script>
