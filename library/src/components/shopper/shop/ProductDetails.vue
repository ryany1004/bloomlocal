<template>
  <div v-loading.fullscreen="loading" class="product-details" >
    <div v-if="product.id">
      <div class="row">
        <div class="col-md-6 col-12">
          <div>
            <div class=" ml-3">
              <img :src="`${mediaUrl}${thumbnail}`" style="width: 100%">
            </div>

            <div class="product-images mt-4">
              <ul class="el-upload-list el-upload-list--picture-card">
                <li class="el-upload-list__item is-success" v-for="img in product_imgs" :key="img.uid">
                  <div>
                    <a href="javascript:void(0)" @click="thumbnail = img.url"><div class="el-upload-list__item-thumbnail" :style="{backgroundImage: `url('${mediaUrl}${img.url}')`}"></div></a>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-12">
          <div>
            <div class="form-group mb-4">
              <h3 class="text-1 color-1 bolder"><span>{{product.title}}</span></h3>
            </div>
            <div class="mb-2">
              <el-rate v-model="product.rating" show-score disabled text-color="#000" score-template="({value})"></el-rate>
            </div>
            <div class="form-group mb-4">
              <h4 class="text-1 color-1 bolder"><span>${{product_price}}</span></h4>
            </div>
            <div class="form-group">
              <h5 class="text-2">Product Description</h5>
              <div class=" text-2" style="white-space: pre-line;" v-readMore:300="product.description">
              </div>
            </div>
            <div class="form-group" v-if="active_colors.length > 0">
              <div class="d-flex align-items-center">
                <label class="mr-3 mb-0 text-2">Color:</label>
                <span class="d-flex align-items-center">
                  <span class="c-circle" :class="{active: color == active_color}" :style="{backgroundColor: color}" @click="active_color = color" v-show="active_colors.indexOf(color) != -1" v-for="color in colors" :key="color"></span>
                </span>
              </div>
            </div>
            <div class="form-group d-flex align-items-center">
              <label class="mr-2 mb-0 text-2">Categories:</label>
              <div class="text-2"><span>{{product.category_names.join(", ")}}</span></div>
            </div>
            <div class="form-group" v-if="active_sizes.length > 0">
              <div class="d-flex align-items-center">
                <label class="mr-3 mb-0 text-2">Size:</label>
                <span class="d-flex align-items-center">
                  <span class="badge mr-1 product-size white"
                        @click="active_size = size" v-show="active_sizes.indexOf(size) != -1" v-for="size in sizes"
                        :class="{'badge-success': size == active_size, 'badge-primary': size!= active_size}"
                        :key="size">{{size}}</span>
                </span>
              </div>
            </div>
            <div class="form-group d-flex align-items-center">
              <div class="form-row">
                <div class="col-1 d-flex align-items-center">
                  <a href="javascript:void(0)" @click="quantity = quantity > 1 ? quantity - 1: 1"><i class="fal fa-minus color4f"></i></a>
                </div>
                <div class="col-2 d-flex align-items-center">
                  <ValidationProvider rules="positive" v-slot="{ errors }">
                  <input class="form-control quantity form-control-lg" @blur="check_quantity()" v-model="quantity" type="number" step="1" min="1" :class="{'is-invalid': errors.length > 0}">
                  </ValidationProvider>
                </div>
                <div class="col-1 d-flex align-items-center">
                  <a href="javascript:void(0)" @click="quantity += 1"><i class="fal fa-plus color4f"></i></a>
                </div>
                <div class="col-8">
                  <button :disabled="product.status !=0 || product.archived" @click="add_to_cart()" class="btn btn-primary btn-lg white" type="button"><i class="fal fa-shopping-cart mr-3"></i> Add to cart</button>
                </div>
              </div>
            </div>
          </div>
          <h3 class="color-1 text-2 mt-5">Customer's Feedback (0)</h3>
          <ul class="feedbacks">
            <li class="mb-3">
              <h4 class="customer">Elias Mnaik</h4>
              <div class="content">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Euismod eu nisi, a, id enim. Nibh tincidunt venenatis at cursus
              </div>
            </li>
            <li class="mb-3">
              <h4 class="customer">Istiaq Zisan</h4>
              <div class="content">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Euismod eu nisi, a, id enim. Nibh tincidunt venenatis at cursus
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ValidationProvider, extend } from 'vee-validate';
import {mapState} from "vuex";
import axios from "axios";
import _ from "lodash";

extend('positive', value => {
  return value >= 1;
});

export default {
  name: "ProductDetails",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    productId: {
      required: true
    },
    uuid: {
      type: String,
      required: true
    }
  },
  components: {
    ValidationProvider
  },
  data: function () {
    return {
      product: {},
      product_imgs: [],
      delivery_types: [
        {value: 'pickup', text: "Pickup"},
        {value: 'delivery', text: "Delivery"},
        {value: 'both', text: "Both"},
      ],
      variants: [],
      loading: false,
      active_colors: [],
      active_sizes: [],
      active_size: null,
      active_color: null,
      thumbnail: "",
      quantity: 1,
    }
  },
  created() {
    this.get_product();
    this.$store.dispatch('get_colors');
    this.$store.dispatch('get_sizes');
    this.$store.dispatch('get_categories');

    axios.post(`/api/analytics/product/${this.uuid}/`, {'channel': 'website'})
  },
  computed: {
    ...mapState(
        ['colors', 'sizes', 'categories']
    ),
    product_price() {
      let price = this.product.price;
      let variant = {};
      if (this.product.enable_size) {
        variant['size'] =  this.active_size;
      }
      if (this.product.enable_color) {
        variant['color'] =  this.active_color;
      }
      let price_variant = _.find(this.variants, variant);
      if (price_variant && price_variant.price > 0) {
        price = price_variant.price;
      }
      return price
    }
  },
  methods: {
    get_product() {
      let that = this;
      that.loading = true
      axios.get(`/api/shop/product/${this.productId}/`).then(function (res) {
        that.product = res.data;
        that.thumbnail = res.data.thumbnail;
        that.product_imgs = res.data.images
        that.variants = res.data.variants;
        that.set_active_sizes_and_color(res.data);
        that.loading = false;
      }).catch(function () {
        that.loading = false
      })
    },
    set_active_sizes_and_color(product) {
      let group = _.groupBy(product.variants, 'size');
      delete group[undefined];
      this.active_sizes = Object.keys(group) || [];
      group = _.groupBy(product.variants, 'color');
      delete group[undefined];
      this.active_colors = Object.keys(group) || [];
    },
    valid_input() {
      if (this.active_colors.length > 0 && this.active_color == null) {
        return "Please choose a color";
      }

      if (this.active_sizes.length > 0 && this.active_size == null) {
        return "Please choose a size";
      }
      this.quantity = parseInt(this.quantity)
      if (this.quantity < 1) {
        return "The quantity must greater than or equal to 1"
      }
      return null;
    },
    check_quantity() {
      this.quantity = parseInt(this.quantity);
    },
    add_to_cart() {
      let msg = this.valid_input(), that = this;
      if (msg) {
        alert(msg);
        return;
      }
      let payload = {
        product_id: this.product.id,
        quantity: this.quantity,
        size: this.active_size,
        color: this.active_color
      }
      this.$store.dispatch("add_to_cart", payload).then(() => {
        that.$notify({
          title: 'Success',
          message: `${that.product.title} was added to your shopping cart.`,
          type: 'success'
        });
      });
    }
  }
}
</script>

<style lang="scss">
  .disabled {
    pointer-events: none;
    opacity: 0.5;
  }
  .product-details {
    .color4f{
      color: #4F4F4F
    }
    .form-control.is-invalid {
      padding-right: 0.75rem;
    }
    .quantity, .quantity:focus {
      background-color: #B6E1F1;
      text-align: center;
    }
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        /* display: none; <- Crashes Chrome on hover */
        -webkit-appearance: none;
        margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
    }

    input[type=number] {
        -moz-appearance:textfield; /* Firefox */
    }
    .form-inline .form-control.input-w50 {
      width: 60px;
      padding: 0.25rem 0.1rem;
    }
    .c-circle {
      width: 24px;
      height: 24px;
      display: inline-block;
      border-radius: 50%;
      border: 1px solid #00d1b2;
      margin-right: 10px;
      cursor: pointer;
    }
    .c-circle:last-child {
      margin-right: 0;
    }
    .c-circle.active, .c-circle:hover {
      border: 2px solid yellowgreen;
      -webkit-box-shadow: 1px 5px 5px 0px #CCCCCC;
      -moz-box-shadow: 1px 5px 5px 0px #CCCCCC;
      -o-box-shadow: 1px 5px 5px 0px #CCCCCC;
      box-shadow: 1px 5px 5px 0px #CCCCCC;
      transform: scale(1.2);
      transition: transform .3s;
    }
    .product-uploader .el-upload {
      border: 1px dashed #d9d9d9;
      border-radius: 6px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      width: 100%;
      height: 100%;
    }
    .product-uploader .el-upload:hover {
      border-color: #409EFF;
    }
    .avatar-uploader-icon {
      font-size: 16px;
      color: #8c939d;
      width: 100%;
      height: 100%;
      line-height: 178px;
      justify-content: center;
      display: flex;
    }

    .product-thumbnail {
      width: 100%;
      height: 571px;
      display: block;
      background-position: center;
      background-size: contain;
      background-repeat: no-repeat;
      background-color: transparent;
      -webkit-transition: all 1s ease-in-out;
      -moz-transition: all 1s ease-in-out;
      -o-transition: all 1s ease-in-out;
      transition: all 1s ease-in-out;
    }
    .product-images {
      .el-upload-list--picture-card .el-upload-list__item {
        width: 80px;
        height: 80px;
        border: 1px solid #f9f9f9;
        background-color: transparent;
      }
      .el-upload-list__item-thumbnail {
        height: 80px;
        width: 80px;
        background-position: center;
        background-size: contain;
        background-repeat: no-repeat;
      }
      .el-upload--picture-card {
        width: 80px;
        height: 80px;
        line-height: 80px;
        float: left;
        margin-right: 15px;
        i {
          font-size: 16px;
        }
      }
      .el-upload-list__item {
        transition: none;
        margin: 0 15px 15px 0;
      }
    }
    .product-size {
      cursor: pointer;
      padding: 0.4em 0.5em;
    }
    .error {
      font-size: 11px;
      color: red;
    }
    .p-stock {
      padding: 9px 40px;
      border-radius: 5px;
    }
    .feedbacks {
      list-style: none;
      padding-left: 0;
      li {
        .customer {
          font-size: 14px;
        }
        .content {
          font-size: 12px;
          color: #4F4F4F;
        }
      }
    }
  }
</style>
