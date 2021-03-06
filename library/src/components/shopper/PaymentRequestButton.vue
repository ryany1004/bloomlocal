<template>
  <div class="sr-root">
    <div class="sr-main">
      <h3 class="font-16">Payment Method</h3>
      <form id="payment-form" class="sr-payment-form mt-3" @submit="handleSubmit">
        <div class="sr-combo-inputs-row">
          <div class="sr-input sr-card-element" id="card-element"></div>
        </div>
        <div class="sr-field-error" id="card-errors" role="alert"></div>
        <button class="btn btn-primary white btn-block my-3" id="submit" :disabled="loading">
          <b-spinner v-if="loading" small label="Spinning"></b-spinner>
          <span id="button-text">Pay </span><span id="order-amount">${{ totalPrice | numFormat("0.00") }}</span>
        </button>
      </form>
      <div class="sr-result hidden">
        <p>Payment completed<br /></p>
      </div>
    </div>
  </div>
</template>

<script>
let stripe;

export default {
  name: "PaymentRequestButton",
  props: {
    publishableKey: {
      type: String,
      required: true
    },
    clientSecret: {
      type: String,
      required: true
    },
    totalPrice: {
      type: Number,
      default: 0
    },
    successUrl: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      disabled: true,
      payment_info: {},
      loading: false,
      errorMsgText: ""
    }
  },
  mounted() {
    this.setupElements();
  },
  methods: {
    handleSubmit(evt) {
      evt.preventDefault();
      let {stripe, card, clientSecret} = this.payment_info;
      this.loading = true;
      let that = this;
      // Initiate the payment.
      // If authentication is required, confirmCardPayment will automatically display a modal
      stripe.confirmCardPayment(clientSecret, {
          payment_method: {
            card: card
          }
        }).then(function(result) {
          that.loading = false;
          if (result.error) {
            // Show error to your customer
            that.showError(result.error.message);
          } else {
            // The payment has been processed!
            location.href = that.successUrl;
            that.orderComplete(clientSecret);
          }
        });
    },
    orderComplete(clientSecret) {
      // Just for the purpose of the sample, show the PaymentIntent response object
      stripe.retrievePaymentIntent(clientSecret).then(function(result) {
        let paymentIntent = result.paymentIntent;
        let paymentIntentJson = JSON.stringify(paymentIntent, null, 2);
        console.log(paymentIntentJson);
        document.querySelector(".sr-payment-form").classList.add("hidden");
        document.querySelector(".sr-result").classList.remove("hidden");
        this.loading = false;
      });
    },
    showError(errorMsgText) {
      let errorMsg = document.querySelector(".sr-field-error");
      errorMsg.textContent = errorMsgText;
    },
    setupElements() {
      stripe = window.Stripe(this.publishableKey);
      let elements = stripe.elements();
      let style = {
        base: {
          color: "#32325d",
          fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
          fontSmoothing: "antialiased",
          fontSize: "16px",
          "::placeholder": {
            color: "#aab7c4"
          }
        },
        invalid: {
          color: "#fa755a",
          iconColor: "#fa755a"
        }
      };

      let card = elements.create("card", { style: style, hidePostalCode: true });
      card.mount("#card-element");

      this.payment_info = {
        stripe: stripe,
        card: card,
        clientSecret: this.clientSecret
      };
    }
  }
}
</script>

<style scoped>
:root {
  --accent-color: #0a721b;
}
.sr-combo-inputs-row {
  margin-bottom: 20px;
  background: #fff;
  box-shadow: 0 1px 3px 0 rgb(50 50 93 / 15%), 0 4px 6px 0 rgb(112 157 199 / 15%);
  border-radius: 4px;
  border: none;
  padding: 10px;
}
.sr-field-error {
  color: red;
}
#button-text {
  margin-left: 10px;
}
</style>
