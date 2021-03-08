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
                                    <li role="presentation" class="" v-bind:class="{active:steps == 1}" @click="formSteps(1)">
                                        <a href="javascript:void(0)" data-href="#step1" data-toggle="tab" aria-controls="step1" role="tab" aria-expanded="true"><span class="round-tab">1 </span> <i>Store Information</i></a>
                                    </li>
                                    <li role="presentation" class="disabled" v-bind:class="{active:steps == 2}" @click="formSteps(2)">
                                        <a href="javascript:void(0)" data-href="#step2" data-toggle="tab" aria-controls="step2" role="tab" aria-expanded="false"><span class="round-tab">2</span> <i>Contact Details</i></a>
                                    </li>
                                    <li role="presentation" class="disabled" v-bind:class="{active:steps == 3}" @click="formSteps(3)">
                                        <a href="javascript:void(0)" data-href="#step3" data-toggle="tab" aria-controls="step3" role="tab"><span class="round-tab">3</span> <i>Import Products</i></a>
                                    </li>
                                    <li role="presentation" class="disabled step4" v-bind:class="{active:steps == 4}" @click="formSteps(4)">
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
                                        <contact-detail></contact-detail>
                                    </div>
                                    <!-- Steps 3 -->
                                    <div class="tab-pane" role="tabpanel" id="step3" v-if="steps == 3" v-bind:class="{active:steps == 3}">
                                        <div class="step_3">
                                            <h3>
                                                Import your products from <br />
                                                Shopify, WooCommerce Or Big Commerce
                                            </h3>
                                            <h4>Select Your Platform</h4>
                                            <div class="clearfix"></div>
                                            <div class="d-flex align-items-center justify-content-center">
                                                <div class="p-2 bd-highlight col-example box_div">
                                                    <a href="#"><img src="../../assets/images/shopify.png" alt="" /></a>
                                                </div>
                                                <div class="p-2 bd-highlight col-example box_div">
                                                    <a href="#"><img src="../../assets/images/bigcommorce.png" alt="" /></a>
                                                </div>
                                                <div class="p-2 bd-highlight col-example box_div">
                                                    <a href="#"><img src="../../assets/images/woocommerce.png" alt="" /></a>
                                                </div>
                                                <div class="p-2 bd-highlight col-example box_div">
                                                    <a href="#"><img src="../../assets/images/csv.png" alt="" /></a>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <ul class="list-inline next_btn_div">
                                                    <li><button type="button" class="default-btn import_btn" v-on:click="nextStep">Import Now</button></li>
                                                </ul>
                                            </div>
                                            <div class="col-md-12">
                                                <ul class="list-inline next_btn_div">
                                                    <li><a href="#" class="default-btn next-step skip_btn" v-on:click="nextStep">Skip for now and create my e-commerce store</a></li>
                                                </ul>
                                            </div>
                                        </div>
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
                                                    <button class="gotohomepage">Bloom Homepage</button>
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

export default {
    name: 'SignUpSteps',
    components: {
        'store-information': StoreInfo,
        'contact-detail': ContactDetail
    },
    computed: {
        steps() {
            return this.$store.getters.formSteps;
        }
    },
    mounted(){

    },
    methods: {
        formSteps (step) {
            // let checkFormFiled = this.$store.getters.
            this.$store.dispatch('nextProcess', step)
        },
        nextStep() {
            let step = this.steps;
            // let step = this.$store.getters.formSteps;
            if( step >= 1 ||  step <= 4 ) {
                step +=1;
                this.$store.dispatch('nextProcess', step)
            }
            // let form = this.$refs.stepsFormSubmit1;
        },
        stepsFormSubmit(event) {
            event.preventDefault();
            console.log(event.target)
        }
    }
}
</script>
