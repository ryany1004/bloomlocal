<template>
  <product-confirm-upload v-if="uploaded"></product-confirm-upload>
  <div v-else class="product-upload">
    <h3 class="business-title">Add New Product</h3>
    <form class="mt-5">
      <div class="row">
        <div class="col-md-5 col-12">
          <el-upload
            class="product-uploader"
            action=""
            :show-file-list="false"
            :http-request="handleThumbnailUpload"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeUpload">
            <div v-if="product.thumbnail" :style="{backgroundImage: `url('${mediaUrl}${product.thumbnail}'`}" class="product-thumbnail"></div>
            <div class="" v-else>
              <i  class="el-icon-plus avatar-uploader-icon">
                <span class="uploader-circle"></span>
              </i>
              <p class="el-uploader-text">Add Product Image</p>
            </div>
            <div class="progress" style="height: 1px;">
              <div class="progress-bar" role="progressbar" :style="{width: percent + '%'}" style="width: 0%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </el-upload>
          <p class="error" v-if="errs.thumbnail">Product Image is required</p>

          <div class="clearfix">
            <div class="product-images d-flex justify-content-between">
              <image-uploader v-model="img.url" v-for="(img, index) in product_imgs" :key="index"
                :media-url="mediaUrl"></image-uploader>
            </div>
<!--            <el-upload action="" list-type="picture-card" :file-list="product_imgs" class="product-images"-->
<!--              :http-request="handleImgsUpload" :auto-upload="true" :before-upload="beforeUpload"-->
<!--              :on-success="handleImgsSuccess">-->
<!--                <i slot="default" class="el-icon-plus"></i>-->
<!--                <div slot="file" slot-scope="{file}">-->
<!--                  <div v-if="!file.url.startsWith('blob')" :style="{backgroundImage: `url('${file.url.startsWith('blob') ? file.url: mediaUrl + file.url}'`}" class="el-upload-list__item-thumbnail"></div>-->
<!--                  <div v-else class="progress" style="height: 1px;">-->
<!--                    <div class="progress-bar" role="progressbar" :style="{width: percent2 + '%'}" style="width: 0%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>-->
<!--                  </div>-->
<!--                  <span v-if="!file.url.startsWith('blob')" class="el-upload-list__item-actions">-->
<!--                    <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleRemove(file)">-->
<!--                      <i class="el-icon-delete"></i>-->
<!--                    </span>-->
<!--                  </span>-->
<!--                </div>-->
<!--            </el-upload>-->
            <p class="error" v-if="errs.images">Images are required</p>
          </div>
        </div>
        <div class="col-md-7 col-12">
          <div class="row">
            <div class="form-group col-md-8">
              <input :class="{'is-invalid': errs.title}" type="text" maxlength="500"
                     class="form-control" id="product_tile" placeholder="Product Title" v-model="product.title">
            </div>
            <div class="form-group col-md-4">
              <ValidationProvider rules="positive" v-slot="{ errors }">
              <input min="0" type="number" :class="{'is-invalid': errors.length > 0 || errs.price}"
                     class="form-control" id="product_price" placeholder="Price" v-model="product.price">
              </ValidationProvider>
            </div>
          </div>
          <div class="row">
            <div class="form-group col-8">
              <textarea :class="{'is-invalid': errs.description}" class="form-control" id="product_description"
                        v-model="product.description" placeholder="Description"></textarea>
            </div>
            <div class="form-group col-4">
              <ValidationProvider rules="positive" v-slot="{ errors }">
              <input min="0" type="number" :class="{'is-invalid': errors.length > 0 || errs.stock}" v-model="product.stock" class="form-control" placeholder="Stock"/>
              </ValidationProvider>
            </div>
          </div>

          <div class="form-row">
            <div class="col-12 product-section">Product Specs</div>
            <div class="form-group col-4">
              <el-select collapse-tags v-model="active_colors" multiple placeholder="Color">
                <el-option
                  v-for="value in colors"
                  :key="value"
                  :label="value"
                  :value="value">
                </el-option>
              </el-select>
            </div>
            <div class="form-group col-4">
              <el-select collapse-tags v-model="active_sizes" multiple placeholder="Size">
                <el-option
                  v-for="value in sizes"
                  :key="value"
                  :label="value"
                  :value="value">
                </el-option>
              </el-select>
            </div>
            <div class="form-group col-3">
              <el-select v-model="product.status" clearable placeholder="Availability"  :class="{'is-invalid': errs.status}">
                <el-option label="Yes" :value="0"></el-option>
                <el-option label="No" :value="1"></el-option>
              </el-select>
            </div>
          </div>
          <div class="row">
            <div class="form-group col-8">
              <el-select class="display-block" collapse-tags v-model="product.categories" multiple placeholder="Category">
                <el-option
                  v-for="c in categories"
                  :key="c.id"
                  :label="c.name"
                  :value="c.id">
                </el-option>
              </el-select>
            </div>
          </div>
          <div class="form-row">
            <div class="col-12 font-14 product-section">Product Dimensions</div>
            <div class="form-group col-2">
              <ValidationProvider rules="positive" v-slot="{ errors }">
              <input min="0" :class="{'is-invalid': errors.length > 0 || errs.length}" type="number" class="form-control" v-model="product.length" placeholder="Length"/>
              </ValidationProvider>
            </div>
            <div class="form-group col-2">
              <ValidationProvider rules="positive" v-slot="{ errors }">
              <input min="0" :class="{'is-invalid': errors.length > 0 || errs.width}" type="number" class="form-control" v-model="product.width" placeholder="Width"/>
              </ValidationProvider>
            </div>
            <div class="form-group col-2">
              <ValidationProvider rules="positive" v-slot="{ errors }">
              <input min="0" :class="{'is-invalid': errors.length > 0 || errs.height}" type="number" class="form-control" v-model="product.height" placeholder="Height"/>
              </ValidationProvider>
            </div>
            <div class="form-group col-2">
              <ValidationProvider rules="positive" v-slot="{ errors }">
              <input min="0" :class="{'is-invalid': errors.length > 0 || errs.weight}" type="number" class="form-control" v-model="product.weight" placeholder="Weight"/>
              </ValidationProvider>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-12">
              <button type="button" class="btn btn-primary mt-3 mb-4 white" @click="uploadProduct"><i class="fas fa-plus-circle"></i> Publish Product</button>
            </div>
          </div>


<!--          <div class="form-row">-->
<!--            <div class="form-group col-md-5">-->
<!--              <div class="d-flex">-->
<!--                <label for="product_tile" class="mr-4" :class="{disabled: !product.enable_color}">Color</label>-->
<!--                <el-switch v-model="product.enable_color" @change="reset_attribute('color')"></el-switch>-->
<!--              </div>-->
<!--              <div :class="{disabled: !product.enable_color}">-->
<!--                <span @click="toggleColor(color)" class="c-circle" :style="{backgroundColor: color}" v-for="color in colors" :key="color"-->
<!--                      :class="{ active: active_colors.indexOf(color) != -1}"></span>-->
<!--              </div>-->
<!--            </div>-->
<!--            <div class="form-group col-md-7">-->
<!--              <div class="d-flex">-->
<!--                <label for="product_tile" class="mr-4" :class="{disabled: !product.enable_size}">Size</label>-->
<!--                <el-switch v-model="product.enable_size" @change="reset_attribute('size')"></el-switch>-->
<!--              </div>-->
<!--              <div :class="{disabled: !product.enable_size}">-->
<!--                <span @click="toggleSize(size)" :class="{'badge-secondary': active_sizes.indexOf(size) == -1, 'badge-primary': active_sizes.indexOf(size) != -1}" class="badge mr-1 product-size"-->
<!--                      v-for="size in sizes" :key="size">{{size}}</span>-->
<!--              </div>-->
<!--            </div>-->
<!--            <div class="mb-3" v-if="active_colors.length > 0 || active_sizes.length > 0">-->
<!--              <a href="javascript:void(0)" class="font-14" @click="dialogVisible = true">Set price for variants</a>-->
<!--            </div>-->
<!--          </div>-->

<!--          <div class="form-row">-->
<!--            <div class="form-group col-md-5">-->
<!--              <label for="product_category">Category</label>-->
<!--              <select class="form-control form-control-sm w-50" id="product_category" v-model="product.category">-->
<!--                <option disabled value="">&#45;&#45;</option>-->
<!--                <option v-for="category in categories" :value="category.id" :key="category.id">{{category.name}}</option>-->
<!--              </select>-->
<!--            </div>-->
<!--            <div class="form-group col-md-7">-->
<!--              <div class="form-check" v-for="option in delivery_types" :key="option.value">-->
<!--                <input class="form-check-input" v-model="product.delivery_type" type="radio" name="delivery_type" :id="option.value" :value="option.value">-->
<!--                <label class="form-check-label" :for="option.value">-->
<!--                  {{ option.text }}-->
<!--                </label>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
<!--          <div class="form-row">-->
<!--            <div class="form-group col-12">-->
<!--              <label for="product_category">Product Dimensions</label>-->
<!--              <div class="form-inline">-->
<!--                <select class="form-control form-control-sm input-w50" v-model="product.dimension_unit">-->
<!--                  <option value="cm">cm</option>-->
<!--                  <option value="in">inch</option>-->
<!--                </select>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
<!--          <div class="form-row">-->
<!--            <div class="form-group col-5">-->
<!--              <label for="product_category">Product Weight</label>-->
<!--              <div class="form-inline">-->

<!--                <select class="form-control form-control-sm input-w50" v-model="product.weight_unit">-->
<!--                  <option value="lb">lb</option>-->
<!--                  <option value="kg">kg</option>-->
<!--                </select>-->
<!--              </div>-->
<!--            </div>-->
<!--            <div class="form-group col-3">-->
<!--              <label for="product_category">Stock</label>-->

<!--            </div>-->
<!--          </div>-->
        </div>
      </div>
    </form>

    <el-dialog
      title="Set price for variants"
      :visible.sync="dialogVisible"
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
import $ from 'jquery'
import axios from "axios";
import { ValidationProvider, extend } from 'vee-validate';
import Variants from "@/components/variants/Variants";
import ImageUploader from "@/components/business/products/ImageUploader";

extend('positive', value => {
  return value >= 0;
});

export default {
  name: "ProductAdd",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    shop: {
      required: true
    }
  },
  components: {
    ImageUploader,
    Variants,
    ValidationProvider
  },
  data: function () {
    return {
      product: {
        title:"",
        price: "",
        enable_color: true,
        enable_size: true,
        thumbnail: null,
        delivery_type: 'pickup',
        category: "",
        dimension_unit: 'cm',
        length: null,
        width: null,
        height: null,
        weight_unit: 'lb',
        weight: null,
        stock: null,
        description: "",
        status: null
      },
      percent: 0,
      percent2: 0,
      product_imgs: [
          {url: ""},
          {url: ""},
          {url: ""},
          {url: ""},
      ],
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
    this.$store.dispatch('get_colors');
    this.$store.dispatch('get_sizes');
    this.$store.dispatch('get_categories');
  },
  computed: {
    ...mapState(
        ['colors', 'sizes', 'categories']
    ),
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
  methods: {
    handleThumbnailUpload(data) {
      let that = this;
      let params = {
        filename: data.file.name,
        content_type: data.file.type,
        prefix: "product/thumb/"
      }
      this.axios.post('/api/shop/upload/generate-url/',params, ).then(function (res) {
        $.ajax({
            url: res.data.url,
            type: 'PUT',
            data: data.file,
            contentType: data.file.type,
            xhr: function () {
              let myXhr = $.ajaxSettings.xhr();
              if (myXhr.upload) {
                  myXhr.upload.addEventListener('progress', that.progressHandling, false);
              }
              return myXhr;
            },
            success: function () {
              that.product.thumbnail = res.data.path;
              data.onSuccess(res.data.path)
            },
            error: function (result) {
                console.log(result);
                alert("Error while uploading.");
            },
            processData: false
        });
      });
    },

    progressHandling(event) {
      let percent = 0;
      let position = event.loaded || event.position;
      let total = event.total;
      if (event.lengthComputable) {
        percent = Math.ceil(position / total * 100);
        this.percent = percent;
      }
    },

    beforeUpload: function (file) {
      const isJPG = ['image/jpeg', "image/png", "image/webp"].indexOf(file.type) != -1;
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('Image must be JPG, PNG format!');
      }
      if (!isLt2M) {
        this.$message.error('Image size can not exceed 2MB!');
      }
      return isJPG && isLt2M;
    },
    handleAvatarSuccess: function (file) {
      this.percent = 0
      console.log(file)
    },
    handleRemove: function(file) {
      let index = this.product_imgs.indexOf(file);
      if (index != -1) {
        this.$delete(this.product_imgs, index);
      }
    },
    uploadProduct() {
      console.log(this.getVariants());
      if (confirm("Are you sure?")) {
        let data = this.product, that=this;
        data.shop = this.shop;
        data.variants = this.getVariants();
        data.enable_color = this.active_colors.length > 0;
        data.enable_size = this.active_sizes.length > 0;
        data.images = this.product_imgs.filter((img) => img.url != '');
        console.log(data.images);
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
    .el-uploader-text {
      position: absolute;
      top: 60%;
      left: 0;
      right: 0;
      font-size: 16px;
      color: #919EAB;
    }
    #product_description {
      height: 155px;
    }
    .product-section {
      font-weight: 500;
      font-size: 14px;
      color: #212B36;
      margin-bottom: 0.5rem !important;
    }
    .el-input__inner::placeholder {
      color: #47484B;
    }
    .el-select .el-input .el-select__caret {
      color: #495057;
    }
    .el-input__suffix {
      margin-right: 0;
    }
    .el-select__tags-text {
      max-width: 65px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      display: inline-block;
      vertical-align: middle;
      color: #495057;
    }
    .el-upload-list__item-thumbnail {
      height: 80px;
      width: 80px;
      background-position: center;
      background-size: contain;
      background-repeat: no-repeat;
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
      border-radius: 8px;
      cursor: pointer;
      background-color: #F4F6F8;
      position: relative;
      overflow: hidden;
      width: 100%;
      height: 100%;
    }
    .product-uploader .el-upload:hover {
      border-color: #409EFF;
    }
    .avatar-uploader-icon {
      font-size: 39px;
      color: #00AEEF;
      width: 100%;
      height: 100%;
      line-height: 350px;
      justify-content: center;
      display: flex;
    }
    .avatar-uploader-icon .uploader-circle {
      width: 65px;
      height: 65px;
      position: absolute;
      background-color: #ccc;
      z-index: -1;
      top: 40.5%;
      border-radius: 50%;
    }
    .product-thumbnail {
      width: 100%;
      height: 350px;
      display: block;
      background-position: center;
      background-size: contain;
      background-repeat: no-repeat;
    }
    .product-images {
      .el-upload-list--picture-card .el-upload-list__item {
        width: 80px;
        height: 80px;
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

    .is-invalid {
      .el-input__inner {
        border-color: #b94a48;
        padding-right: calc(1.5em + 0.75rem);
        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='%23b94a48' viewBox='-2 -2 7 7'%3e%3cpath stroke='%23b94a48' d='M0 0l3 3m0-3L0 3'/%3e%3ccircle r='.5'/%3e%3ccircle cx='3' r='.5'/%3e%3ccircle cy='3' r='.5'/%3e%3ccircle cx='3' cy='3' r='.5'/%3e%3c/svg%3E");
        background-repeat: no-repeat;
        background-position: center right calc(0.375em + 0.1875rem);
        background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
      }
    }
  }
</style>
