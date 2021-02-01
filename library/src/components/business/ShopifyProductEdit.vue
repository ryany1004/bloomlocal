<template>
  <div class="product-upload">
    <form>
      <div class="row">
        <div class="col-md-4 col-12">
          <div>
            <div class="product-thumbnail" :style="{backgroundImage: `url('${product_thumbnail}')`}">
            </div>

            <div class="product-images mt-4">
              <ul class="el-upload-list el-upload-list--picture-card">
                <li class="el-upload-list__item is-success" v-for="(img, index) in product_imgs" :key="index">
                  <div>
                    <a href="javascript:void(0)" @click="thumbnail = img.src"><div class="el-upload-list__item-thumbnail" :style="{backgroundImage: `url('${img.src}')`}"></div></a>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-8 col-12">
          <div class="form-row">
            <div class="form-group col-md-8">
              <label for="product_tile">Product Title</label>
              <input :class="{'is-invalid': errs.title}" type="text" maxlength="500"
                     class="form-control w-75" id="product_tile" placeholder="" v-model="product.title">
            </div>
            <div class="form-group col-md-4">
              <label for="product_price">Price</label>
              <ValidationProvider rules="positive" v-slot="{ errors }">
              <input min="0" type="number" :class="{'is-invalid': errors.length > 0 || errs.price}"
                     class="form-control" id="product_price" placeholder="" v-model="product.price">
              </ValidationProvider>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col">
              <label for="product_description">Description</label>
              <textarea :class="{'is-invalid': errs.description}" class="form-control" id="product_description" v-model="product.description"></textarea>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-5">
              <div class="d-flex">
                <label for="product_tile" class="mr-4" :class="{disabled: !product.enable_color}">Color</label>
                <el-switch v-model="product.enable_color" @change="reset_attribute('color')"></el-switch>
              </div>
              <div :class="{disabled: !product.enable_color}">
                <span @click="toggleColor(color)" class="c-circle" :style="{backgroundColor: color}" v-for="color in colors" :key="color"
                      :class="{ active: active_colors.indexOf(color) != -1}"></span>
              </div>
            </div>
            <div class="form-group col-md-7">
              <div class="d-flex">
                <label for="product_tile" class="mr-4" :class="{disabled: !product.enable_size}">Size</label>
                <el-switch v-model="product.enable_size" @change="reset_attribute('size')"></el-switch>
              </div>
              <div :class="{disabled: !product.enable_size}">
                <span @click="toggleSize(size)" :class="{'badge-secondary': active_sizes.indexOf(size) == -1, 'badge-primary': active_sizes.indexOf(size) != -1}" class="badge mr-1 product-size"
                      v-for="size in sizes" :key="size">{{size}}</span>
              </div>
            </div>
            <div class="mb-3" v-if="active_colors.length > 0 || active_sizes.length > 0">
              <a href="javascript:void(0)" class="font-14" @click="dialogVisible = true">Set price for variants</a>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-5">
              <label for="product_category">Category</label>
              <select class="form-control form-control-sm w-50" id="product_category" v-model="product.category">
                <option disabled value="">--</option>
                <option v-for="category in categories" :value="category.id" :key="category.id">{{category.name}}</option>
              </select>
            </div>
            <div class="form-group col-md-7">
              <div class="form-check" v-for="option in delivery_types" :key="option.value">
                <input class="form-check-input" v-model="product.delivery_type" type="radio" name="delivery_type" :id="option.value" :value="option.value">
                <label class="form-check-label" :for="option.value">
                  {{ option.text }}
                </label>
              </div>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-12">
              <label for="product_category">Product Dimensions</label>
              <div class="form-inline">
                <ValidationProvider rules="positive" v-slot="{ errors }">
                <input min="0" :class="{'is-invalid': errors.length > 0 || errs.length}" type="number" class="form-control form-control-sm input-w50" v-model="product.length" placeholder="length"/><span class="px-1" style="font-size: 80%">x</span>
                </ValidationProvider>
                <ValidationProvider rules="positive" v-slot="{ errors }">
                <input min="0" :class="{'is-invalid': errors.length > 0 || errs.width}" type="number" class="form-control form-control-sm input-w50" v-model="product.width" placeholder="width"/><span class="px-1" style="font-size: 80%">x</span>
                </ValidationProvider>
                <ValidationProvider rules="positive" v-slot="{ errors }">
                <input min="0" :class="{'is-invalid': errors.length > 0 || errs.height}" type="number" class="form-control form-control-sm input-w50 mr-1" v-model="product.height" placeholder="height"/>
                </ValidationProvider>
                <select class="form-control form-control-sm input-w50" v-model="product.dimension_unit">
                  <option value="cm">cm</option>
                  <option value="in">inch</option>
                </select>
              </div>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-5">
              <label for="product_category">Product Weight</label>
              <div class="form-inline">
                <ValidationProvider rules="positive" v-slot="{ errors }">
                <input min="0" :class="{'is-invalid': errors.length > 0 || errs.weight}" type="number" class="form-control input-w50 form-control-sm mr-1" v-model="product.weight"/>
                </ValidationProvider>
                <select class="form-control form-control-sm input-w50" v-model="product.weight_unit">
                  <option value="lb">lb</option>
                </select>
              </div>
            </div>
            <div class="form-group col-3">
              <label for="product_category">Stock</label>
              <ValidationProvider rules="positive" v-slot="{ errors }">
              <input min="0" type="number" :class="{'is-invalid': errors.length > 0 || errs.stock}" v-model="product.stock" class="form-control form-control-sm input-w50"/>
              </ValidationProvider>
            </div>
          </div>
        </div>
      </div>
    </form>

    <el-dialog
      title="Set price for variants"
      :visible.sync="dialogVisible"
      :append-to-body="true"
      width="50%">
      <variants :sizes="active_sizes" :colors="active_colors" v-model="variants"/>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Close</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {mapState} from 'vuex';
import axios from "axios";
import { ValidationProvider, extend } from 'vee-validate';
import _ from "lodash";
import Variants from "@/components/variants/Variants";

extend('positive', value => {
  return value >= 0;
});

export default {
  name: "ShopifyProductEdit",
  props: {
    product: {
      type: Object,
      required: true
    }
  },
  components: {
    ValidationProvider,
    Variants
  },
  data: function () {
    return {
      product_imgs: [],
      delivery_types: [
        {value: 'pickup', text: "Pickup"},
        {value: 'delivery', text: "Delivery"},
        {value: 'both', text: "Both"},
      ],
      active_sizes: [],
      active_colors: [],
      variants: [],
      uploaded: false,
      errs: {},
      dialogVisible: false
    }
  },
  created() {

  },
  computed: {
    ...mapState(
            ['colors', 'sizes', 'categories']
        ),
    product_thumbnail() {
      if (this.product.thumbnail) {
        return this.product.thumbnail;
      }
      return require("../../assets/sample-image.jpg");
    },
    price_variants() {
      let data = {};
      this.variants.forEach(variant => {
        if (variant.size && variant.color) {
          data[`${variant.size}:${variant.color}`] = variant.price || null;
        } else if (variant.size) {
          data[`${variant.size}`] = variant.price || null;
        } else if (variant.color) {
          data[`${variant.color}`] = variant.price || null;
        }
      })
      return data;
    },
  },
  watch: {
    product: {
      immediate: true,
      handler(val) {
        this.product_imgs = val.images;
        this.variants = val.variants;
        this.set_active_sizes_and_color(val);
      }
    },
    variants: {
      immediate: true,
      handler(val) {
        this.product.variants = val;
      }
    }
  },
  methods: {
    reset_variants() {
      this.variants = [];
      this.active_colors = [];
      this.active_color = [];
      this.active_sizes = [];
    },
    set_active_sizes_and_color(product) {
      // eslint-disable-next-line no-debugger
      let group = _.groupBy(product.variants, 'size');
      delete group[undefined];
      this.active_sizes = Object.keys(group) || [];
      group = _.groupBy(product.variants, 'color');
      delete group[undefined];
      this.active_colors = Object.keys(group) || [];
    },
    uploadProduct() {
      console.log(this.getVariants());
      if (confirm("Are you sure?")) {
        let data = this.product, that=this;
        data.shop = this.shop;
        data.variants = this.getVariants();
        data.images = this.product_imgs;
        if (data.category) {
          data.categories = [data.category];
        }
        that.errs = {};
        axios.post('/api/shop/product/upload/', data).then(function () {
          that.errs = {}
          that.uploaded = true
        }).catch(function (err) {
          if(err.response.data) {
            that.errs = err.response.data;
          }
          console.log(err);
        })
      }
    },
    getVariants() {
      let that = this, variants = [];
      if (this.product.enable_color && this.product.enable_size) {
        if (this.active_colors.length > 0 && that.active_sizes.length == 0) {
          this.active_colors.forEach(function (color) {
            variants.push({color: color, price: that.price_variants[color] || null});
          })
        } else if (this.active_colors.length == 0 && that.active_sizes.length > 0) {
          this.active_sizes.forEach(function (size) {
            variants.push({size: size, price: that.price_variants[size] || null});
          })
        } else {
          this.active_colors.forEach(function (color) {
            that.active_sizes.forEach(function (size) {
              variants.push({size: size, color: color, price: that.price_variants[`${size}:${color}`] || null});
            })
          })
        }
      } else if (!this.product.enable_color && this.product.enable_size) {
        this.active_sizes.forEach(function (size) {
          variants.push({size: size, price: that.price_variants[size] || null});
        })

      } else if (this.product.enable_color && !this.product.enable_size) {
        this.active_colors.forEach(function (color) {
          variants.push({color: color, price: that.price_variants[color] || null});
        })
      }

      return variants;
    },
    toggleColor(color) {
      let index = this.active_colors.indexOf(color);
      if ( index != -1) {
        this.$delete(this.active_colors, index);
      } else {
        this.active_colors.push(color);
      }
    },
    toggleSize(size) {
      let index = this.active_sizes.indexOf(size);
      if ( index != -1) {
        this.$delete(this.active_sizes, index);
      } else {
        this.active_sizes.push(size);
      }
    },
    reset_attribute(attr) {
      if (attr == 'color' && !this.product.enable_color) {
        this.active_colors = [];
      } else if (attr == 'size' && !this.product.enable_size) {
        this.active_sizes = [];
      }
    },
  }
}
</script>

<style lang="scss">
  .disabled {
    pointer-events: none;
    opacity: 0.5;
  }
  .product-upload {
    .el-upload-list__item-thumbnail {
      height: 60px;
      width: 60px;
      background-position: center;
      background-size: cover;
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
      margin-right: 8px;
      cursor: pointer;
    }
    .c-circle:last-child {
      margin-right: 0;
    }
    .c-circle.active, .c-circle:hover {
      border: 2px solid yellowgreen;
      -webkit-box-shadow: 1px 5px 5px 0px #CCCCCC;
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
    .avatar-uploader-icon .uploader-circle {
      width: 65px;
      height: 65px;
      position: absolute;
      background-color: #ccc;
      z-index: -1;
      top: 31%;
      border-radius: 50%;
    }

    .form-inline > span {
      display: flex;
      align-items: center;
    }
    .product-size {
      cursor: pointer;
      padding: 0.4em 0.5em;
    }
    .error {
      font-size: 11px;
      color: red;
    }
    .product-thumbnail {
      width: 100%;
      height: 200px;
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
        width: 64px;
        height: 64px;
        border: 1px solid #f9f9f9;
        background-color: transparent;
      }
      .el-upload-list__item-thumbnail {
        height: 60px;
        width: 60px;
        background-position: center;
        background-size: cover;
      }
      .el-upload--picture-card {
        width: 60px;
        height: 60px;
        line-height: 60px;
        float: left;
        margin-right: 5px;
        i {
          font-size: 16px;
        }
      }
      .el-upload-list__item {
        transition: none;
      }
    }
  }
</style>
