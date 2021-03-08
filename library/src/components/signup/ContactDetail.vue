<template>
    <div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <input type="email" 
                        name="businessEmail" 
                        placeholder="Business Email" 
                        class="form-control"
                        v-model="businessEmail"
                        @input="checkValidation"
                        v-bind:class="{'is-invalid': (errors ==true && (businessEmail == '' || errorMsg.businessEmail))}"
                        required />
                    <div class="invalid-feedback">{{ errorMsg.businessEmail }}</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <input type="text" 
                        name="businessphone" 
                        placeholder="Business Phone Number" 
                        class="form-control" 
                        v-model="businessphone"
                        @input="checkValidation"
                        v-bind:class="{'is-invalid': (errors ==true && (businessphone == '' || errorMsg.businessphone))}"
                        required
                        />
                    <div class="invalid-feedback">{{ errorMsg.businessphone }}</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <input type="text" 
                        name="businesswebsite" 
                        placeholder="Business Website" 
                        class="form-control" 
                        v-model="businesswebsite"
                        @input="checkValidation"
                        v-bind:class="{'is-invalid': (errors ==true && (businesswebsite == '' || errorMsg.businesswebsite))}"
                        required/>
                    <div class="invalid-feedback">{{ errorMsg.businesswebsite }}</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <input type="text" 
                        name="address" 
                        placeholder="Address"
                        class="form-control" 
                        v-model="address"
                        @input="checkValidation"
                        v-bind:class="{'is-invalid': (errors ==true && (address == '' || errorMsg.address))}"
                        required/>
                    <div class="invalid-feedback">{{ errorMsg.address }}</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="form-group">
                    <input type="text" 
                        name="state" 
                        placeholder="State" 
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
                    placeholder="Zipcode" 
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
export default {
    name: 'ContactDetail',
    data(){
        return {
            businessEmail: '',
            businessphone: '',
            businesswebsite: '',
            address: '',
            state: '',
            zipcode: '',
            errors: false,
            errorMsg: {businessEmail: '', businessphone: '', businesswebsite: '', address: '', state: '', zipcode: ''}
        }
    },
    mounted() {
        let formFields = this.$store.getters.getContactDetail;
        if(formFields) {
            this.businessEmail = (formFields && formFields.businessEmail) ? formFields.businessEmail : ''
            this.businessphone = (formFields && formFields.businessphone) ? formFields.businessphone : ''
            this.businesswebsite = (formFields && formFields.businesswebsite) ? formFields.businesswebsite : ''
            this.address = (formFields && formFields.address) ? formFields.address : ''
            this.state = (formFields && formFields.state) ? formFields.state : ''
            this.zipcode = (formFields && formFields.zipcode) ? formFields.zipcode : ''
        }
    },
    methods: {
        checkValidation() {
            this.validate()
        },
        validate() {
            let errors = [];
            if(this.businessEmail == '') {
                this.errors = true
                this.errorMsg.businessEmail = "Email is required"
                errors.push('bemail')
            } else if(/^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$/.test(this.businessEmail) == false) {
                this.errors = true;
                this.errorMsg.businessEmail = "Enter valid Email"
                errors.push('bemail')
            } else {
                this.errorMsg.businessEmail = ''
            }
            if(this.businessphone == '') {
                this.errors = true
                this.errorMsg.businessphone = "Phone is required"
                errors.push('phone')
            } else if(/^\d{10}$/.test(this.businessphone) == false) {
                this.errors = true;
                this.errorMsg.businessphone = "Enter valid Phone"
                errors.push('phone')
            } else {
                this.errorMsg.businessphone = '';
            }
            // Website Validate
            let regex = /^((http(s?)?):\/\/)?([wW]{3}\.)?[a-zA-Z0-9\-.]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?$/g
            if(this.businesswebsite == '') {
                this.errors = true;
                this.errorMsg.businesswebsite = "Website is required.";
                errors.push('website')
            }else if(regex.test(this.businesswebsite) == false) {
                this.errors = true;
                this.errorMsg.businesswebsite = "Enter valide website"
                errors.push('website')
            } else {
                this.errorMsg.businesswebsite = ''
            }
            // Address
            if(this.address == '') {
                this.errors = true;
                this.errorMsg.address = "Address is required."
                errors.push('Address')
            } else {
                this.errorMsg.address = ''
            }
            // State String empty Validate
            if(this.state == '') {
                this.errors = true;
                this.errorMsg.state = "State is required."
                errors.push('state')
            } else {
                this.errorMsg.state = ''
            }
            // Zipcode Validate
            let zipcodeRegex = /^(\s*\d{6}\s*)(,\s*\d{6}\s*)*,?\s*$/;
            if(this.zipcode == '') {
                this.errors = true;
                this.errorMsg.zipcode = "Zipcode is required."
                errors.push('zipcode')
            } else if(zipcodeRegex.test(this.zipcode) == false) {
                this.errors = true
                this.errorMsg.zipcode = 'Enter valid 6 digit zipcode.'
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
                    businessEmail: this.businessEmail, 
                    businessphone: this.businessphone, 
                    businesswebsite: this.businesswebsite, 
                    address: this.address, 
                    state: this.state,
                    zipcode: this.zipcode
                };
                // Proceed Next Form 
                let step = this.$store.getters.formSteps;
                if( step >= 1 ||  step <= 4 ) {
                    step +=1;
                    this.$store.dispatch('nextProcess', step)
                    this.$store.dispatch('contactDetail', formFileds)
                } 
            }
        }
    }
}
</script>