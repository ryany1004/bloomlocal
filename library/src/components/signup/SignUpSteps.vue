<template>
    <div>
        <section class="wraper">
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <div class="logo_inner"><img src="../../assets/images/logo.png" alt="" /></div>
                        <h1 class="welcome_head">Welcome to Bloom Local</h1>
                        <p class="main_para">Its time to build your store by adding store information, contact details & Products</p>
                    </div>
                </div>
            </div>
        </section>
        <section class="signup-step-container bg_body">
            <div class="container">
                <div class="row d-flex justify-content-center">
                    <div class="col-md-10">
                        <div class="wizard">
                            <div class="wizard-inner">
                                <ul class="nav nav-tabs" role="tablist">
                                    <li role="presentation" class="" v-bind:class="{active: steps == 1 }" @click="formSteps(1)">
                                        <a href="javascript:void(0)" data-href="#step1" data-toggle="tab" aria-controls="step1" role="tab" aria-expanded="true"><span class="round-tab">1 </span> <i>Store Information</i></a>
                                    </li>
                                    <li role="presentation" class="" v-bind:class="{active:steps == 2, disabled: steps < 2}" @click="formSteps(2)">
                                        <a href="javascript:void(0)" data-href="#step2" data-toggle="tab" aria-controls="step2" role="tab" aria-expanded="false"><span class="round-tab">2</span> <i>Contact Details</i></a>
                                    </li>
                                    <li role="presentation" class="" v-bind:class="{active:steps == 3, disabled: steps < 3}" @click="formSteps(3)">
                                        <a href="javascript:void(0)" data-href="#step3" data-toggle="tab" aria-controls="step3" role="tab"><span class="round-tab">3</span> <i>Import Products</i></a>
                                    </li>
                                    <li role="presentation" class="step4" v-bind:class="{active:steps == 4, disabled: steps < 4}" @click="formSteps(4)">
                                        <a href="javascript:void(0)" data-href="#step4" data-toggle="tab" aria-controls="step4" role="tab"><span class="round-tab">4</span> <i>Confirmation</i></a>
                                    </li>
                                </ul>
                            </div>
                            <form class="login-box" @submit.prevent="stepsFormSubmit" ref="stepsFormSubmit1">
                                <div class="tab-content" id="main_form">
                                    <div class="tab-pane active" role="tabpanel" id="step1" v-if="steps == 1" v-bind:class="{active:steps == 1}">
                                        <store-information></store-information>
                                    </div>
                                    <!-- Steps 2 -->
                                    <div class="tab-pane" role="tabpanel" id="step2" v-if="steps == 2" v-bind:class="{active:steps == 2}">
                                        <contact-detail :google-maps-api-key="googleMapsApiKey"></contact-detail>
                                    </div>
                                    <!-- Steps 3 -->
                                    <div class="tab-pane" role="tabpanel" id="step3" v-if="steps == 3" v-bind:class="{active:steps == 3}">
                                      <import-data :next-step="nextStep"></import-data>
                                    </div>
                                    <!-- Steps 4 -->
                                    <div class="tab-pane" role="tabpanel" id="step4" v-if="steps == 4" v-bind:class="{active:steps == 4}">
                                        <div class="row">
                                            <div class="col-md-6">
                                                <div class="confimation_div">
                                                    <h3>Congratulations</h3>
                                                    <h4>
                                                        Your Store is <br />
                                                        almost ready
                                                    </h4>
                                                    <p>
                                                        We are building your store and <br />
                                                        we will notify you once it is ready.
                                                    </p>
                                                    <button @click="goToLogin()" class="gotohomepage">Bloom Homepage</button>
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="confimation_img"><img src="../../assets/images/confirmation_banner.png" alt="" /></div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="clearfix"></div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
// import $ from 'jquery'
import StoreInfo from './StoreInfo.vue'
import ContactDetail from './ContactDetail.vue'
import ImportData from "@/components/signup/ImportData";
import axios from "axios";

export default {
    name: 'SignUpSteps',
    components: {
      ImportData,
        'store-information': StoreInfo,
        'contact-detail': ContactDetail
    },
    props: {
      googleMapsApiKey: {
        type: String
      }
    },
    computed: {
        steps() {
            return this.$store.getters.formSteps;
        }
    },
    mounted(){

    },
    methods: {
        goToLogin() {
          window.location.href = 'https://www.bloomlocal.ca/';
        },
        formSteps (step) {
            // let checkFormFiled = this.$store.getters.
            this.$store.dispatch('nextProcess', step)
        },
        nextStep() {
            let step = this.steps;
            // let step = this.$store.getters.formSteps;
            if( step >= 1 ||  step <= 4 ) {
                step +=1;
                if (step == 4) {
                  this.signUpComplete();
                }
                this.$store.dispatch('nextProcess', step)
            }
            // let form = this.$refs.stepsFormSubmit1;
        },
        signUpComplete() {
          axios.get("/api/accounts/vendor/signup-complete/")
        },
        stepsFormSubmit(event) {
            event.preventDefault();
            console.log(event.target)
        }
    }
}
</script>
