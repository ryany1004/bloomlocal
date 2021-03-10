<template>
    <div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <input type="text"
                        name="uname"
                        placeholder="Business Official Name"
                        class="form-control"
                        v-bind:class="{'is-invalid': (errors ==true && (name == ''))}"
                        v-model="name"
                        required/>
                    <div class="invalid-feedback">Business Official Name is required</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <textarea name="description"
                        placeholder="About the Business"
                        class="form-control"
                        v-bind:class="{'is-invalid': (errors ==true && (description == ''))}"
                        v-model="description"
                        required></textarea>
                    <div class="invalid-feedback">About the Business is required</div>
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
                    <label class="Delivery_label">Delivery Type </label>
                    <label class="Delivery_label"> <input class="mr-2" type="checkbox" name="Delivery" value="delivery" v-model="delivery_type" /> Delivery </label>
<!--                    <label class="Delivery_label"> <input class="mr-2" type="checkbox" name="Takeout" value="takeout" v-model="delivery_type" /> Takeout </label>-->
                    <label class="Delivery_label"> <input class="mr-2" type="checkbox" name="Pickup" value="pickup" v-model="delivery_type"/>Pickup </label>
                </div>
            </div>
            <div class="col-md-12">
                <div class="invalid-feedback" v-if="( errors && delivery_type.length < 1)" style="display:block">Delivery type is required</div>
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
import TagInput from './TagInput.vue';

export default {
    name: 'StoreInfo',
    data(){
        return {
            errors: {},
            name: '',
            description:'',
            tags: [],
            delivery_type: []
        }
    },
    components: {
        TagInput
    },
    created() {
      // Get Store Values
      let formFields = this.$store.getters.getStoreInfo;

      this.name = (formFields.name) ? formFields.name : ''
      this.description = (formFields.description) ? formFields.description : ''
      this.tags = (formFields.tags) ? formFields.tags : []
      this.delivery_type = (formFields.delivery_type) ? formFields.delivery_type : []
    },
    methods: {
        validate() {
            if(this.name == '') {
                this.errors = true;
            }
            if(this.description == '') {
                this.errors = true;
            }
            if(this.tags.length < 1) {
                this.errors = true
            }
            if(this.delivery_type.length < 1) {
                this.errors = true
            }
            if(this.name && this.description && this.tags.length && this.delivery_type.length) {
                this.errors = false;
            }
        },
        nextStep() {
            this.validate();
            if(this.errors == false) {
                 let fields = {
                    name: this.name,
                    description: this.description,
                    tags: this.tags,
                    delivery_type: this.delivery_type
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
