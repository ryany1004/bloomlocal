<template>
    <div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <input type="text" 
                        name="uname" 
                        placeholder="Username" 
                        class="form-control"  
                        v-bind:class="{'is-invalid': (errors ==true && (username == ''))}"
                        v-model="username"
                        @change="removeWhiteSpace"
                        required/>
                    <div class="invalid-feedback">username is required</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <textarea name="aboutBusiness" 
                        placeholder="About the Business" 
                        class="form-control"
                        v-bind:class="{'is-invalid': (errors ==true && (aboutBusiness == ''))}" 
                        v-model="aboutBusiness"
                        required></textarea>
                    <div class="invalid-feedback">username is required</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <label>Add up to 8 tags that relates to your business</label>
                    <TagInput @inputTags="updateInputTags" :inputTag="tags"/>
                    <div class="invalid-feedback" v-if="( errors && tags.length < 1)" style="display:block">Tags is required</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <label class="Delivery_label">Delivery Type </label> <label class="Delivery_label"> <input type="checkbox" name="Delivery" value="delivery" v-model="deliveryType" /> Delivery </label>
                    <label class="Delivery_label"> <input type="checkbox" name="Takeout" value="takeout" v-model="deliveryType" /> Takeout </label> 
                    <label class="Delivery_label"> <input type="checkbox" name="Instore pickup" value="instorePickup" v-model="deliveryType"/>Instore pickup </label>
                </div>
            </div>
            <div class="col-md-12">
                <div class="invalid-feedback" v-if="( errors && deliveryType.length < 1)" style="display:block">Delivery type is required</div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <ul class="list-inline next_btn_div">
                    <li><button type="button" class="default-btn next-step" v-on:click="nextStep">Next: Contact Details</button></li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import $ from 'jquery' 
// import select2 from 'select2'
// window.select2 =select2;
import TagInput from './TagInput.vue';

export default {
    name: 'StoreInfo',
    data(){
        return {
            errors: false,
            username: '',
            aboutBusiness:'',
            tags: [],
            deliveryType: []
        }
    },
    components: {
        TagInput
    },
    created() {
        // Get Store Values
        let formFields = this.$store.getters.getStoreInfo;
        
        this.username = (formFields.username) ? formFields.username : ''
        this.aboutBusiness = (formFields.aboutBusiness) ? formFields.aboutBusiness : ''
        this.tags = (formFields.tags) ? formFields.tags : []
        this.deliveryType = (formFields.deliveryType) ? formFields.deliveryType : []
    }, 
    methods: {
        removeWhiteSpace(){
            this.username = this.username.replace(/\s/g, '');
        },
        validate() {
            if(this.username == '') {
                this.errors = true;
            }
            if(this.aboutBusiness == '') {
                this.errors = true;
            }
            if(this.tags.length < 1) {
                this.errors = true
            }
            if(this.deliveryType.length < 1) {
                this.errors = true
            }
            if(this.username && this.aboutBusiness && this.tags.length && this.deliveryType.length) {
                this.errors = false;
            }
        },
        nextStep() {
            this.validate();
            if(this.errors == false) {
                 let fields = {
                    "username": this.username,
                    "aboutBusiness": this.aboutBusiness,
                    "tags": this.tags,
                    "deliveryType": this.deliveryType
                }
                // Process next Step
                let step = this.$store.getters.formSteps;
                if( step >= 1 ||  step <= 4 ) {
                    step +=1;
                    this.$store.dispatch('nextProcess', step)
                    this.$store.dispatch('storeInfoFields', fields)
                } 
            }
        },
        tagChanged(event) {
            this.tags = $(event.target).val();
        },
        updateInputTags(tags){
            this.tags = tags;
        }
    }
}
</script>