<template>
  <product-confirm-upload v-if="uploaded"></product-confirm-upload>
  <div v-else class="product-upload">
    <form>
      <div class="row">
        <div class="col-md-4 col-12">
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
            </div>
            <div class="progress" style="height: 1px;">
              <div class="progress-bar" role="progressbar" :style="{width: percent + '%'}" style="width: 0%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </el-upload>
          <p class="error" v-if="errs.thumbnail">Thumbnail is required</p>
          <p class="text-center">Upload Image</p>

          <div class="clearfix">
            <el-upload action="" list-type="picture-card" :file-list="product_imgs" class="product-images"
              :http-request="handleImgsUpload" :auto-upload="true" :before-upload="beforeUpload"
              :on-success="handleImgsSuccess">
                <i slot="default" class="el-icon-plus"></i>
                <div slot="file" slot-scope="{file}">
                  <div v-if="!file.url.startsWith('blob')" :style="{backgroundImage: `url('${file.url.startsWith('blob') ? file.url: mediaUrl + file.url}'`}" class="el-upload-list__item-thumbnail"></div>
                  <div v-else class="progress" style="height: 1px;">
                    <div class="progress-bar" role="progressbar" :style="{width: percent2 + '%'}" style="width: 0%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                  </div>
                  <span v-if="!file.url.startsWith('blob')" class="el-upload-list__item-actions">
                    <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleRemove(file)">
                      <i class="el-icon-delete"></i>
                    </span>
                  </span>
                </div>
            </el-upload>
            <p class="error" v-if="errs.images">Images are required</p>
          </div>
          <button type="button" class="btn btn-primary btn-block mt-3 mb-4" @click="uploadProduct"><i class="fas fa-upload"></i> Upload Product</button>
        </div>
        <div class="col-md-8 col-12">
          <div class="form-row">
            <div class="form-group col-md-8">
              <label for="product_tile">Product Title</label>
              <input :class="{'is-invalid': errs.title}" type="text" maxlength="500"
                     class="form-control w-75" id="product_tile" placeholder="" v-model="product.title">
            </div>
            <div class="form-group col-md-4">
              <label for="product_price">Set Price</label>
              <ValidationProvider rules="positive" v-slot="{ errors }">
              <input min="0" type="number" :class="{'is-invalid': errors.length > 0 || errs.price}" class="form-control" id="product_price" placeholder="" v-model="product.price">
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
                <label for="product_tile" class="mr-4">Color</label>
                <el-switch v-model="product.enable_color" @change="reset_attribute('color')"></el-switch>
              </div>
              <div :class="{disabled: !product.enable_color}">
                <span @click="toggleColor(color)" class="c-circle" :style="{backgroundColor: color.value}" v-for="color in colors" :key="color.value"
                      :class="{ active: active_colors.indexOf(color.value) != -1}"></span>
              </div>
            </div>
            <div class="form-group col-md-7">
              <div class="d-flex">
                <label for="product_tile" class="mr-4">Size</label>
                <el-switch v-model="product.enable_size" @change="reset_attribute('size')"></el-switch>
              </div>
              <div :class="{disabled: !product.enable_size}">
                <span @click="toggleSize(size)" :class="{'badge-secondary': active_sizes.indexOf(size.value) == -1, 'badge-primary': active_sizes.indexOf(size.value) != -1}" class="badge mr-1 product-size"
                      v-for="size in sizes" :key="size.value">{{size.text}}</span>
              </div>
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
  </div>
</template>

<script>
import {mapState} from 'vuex';
import $ from 'jquery'
import axios from "axios";
import { ValidationProvider, extend } from 'vee-validate';

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
        description: ""
      },
      percent: 0,
      percent2: 0,
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
      errs: {}
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
  },
  methods: {
    reset_variants() {
      this.variants = [];
      this.active_colors = [];
      this.active_color = [];
      this.active_sizes = [];
    },
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
    handleImgsUpload(data) {
      let that = this;
      let params = {
        filename: data.file.name,
        content_type: data.file.type,
        prefix: "product/imgs/"
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
                  myXhr.upload.addEventListener('progress', that.progressHandling2, false);
              }
              return myXhr;
            },
            success: function () {
              that.product_imgs.push({name: data.file.name, url: res.data.path});
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
    progressHandling2(event) {
      let percent = 0;
      let position = event.loaded || event.position;
      let total = event.total;
      if (event.lengthComputable) {
        percent = Math.ceil(position / total * 100);
        this.percent2 = percent;
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
    handleImgsSuccess(file) {
      this.percent2 = 0
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
            variants.push({color: color});
          })
        } else if (this.active_colors.length == 0 && that.active_sizes.length > 0) {
          this.active_sizes.forEach(function (size) {
            variants.push({size: size});
          })
        } else {
          this.active_colors.forEach(function (color) {
            that.active_sizes.forEach(function (size) {
              variants.push({size: size, color: color});
            })
          })
        }
      } else if (!this.product.enable_color && this.product.enable_size) {
        this.active_sizes.forEach(function (size) {
          variants.push({size: size});
        })

      } else if (this.product.enable_color && !this.product.enable_size) {
        this.active_colors.forEach(function (color) {
          variants.push({color: color});
        })
      }
      return variants;
    },
    toggleColor(color) {
      let index = this.active_colors.indexOf(color.value);
      if ( index != -1) {
        this.$delete(this.active_colors, index);
      } else {
        this.active_colors.push(color.value);
      }
    },
    toggleSize(size) {
      let index = this.active_sizes.indexOf(size.value);
      if ( index != -1) {
        this.$delete(this.active_sizes, index);
      } else {
        this.active_sizes.push(size.value);
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
    .product-thumbnail {
      width: 100%;
      height: 178px;
      display: block;
      background-position: center;
      background-size: cover;
      background-repeat: no-repeat;
    }
    .product-images {
      .el-upload-list--picture-card .el-upload-list__item {
        width: 60px;
        height: 60px;
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
  }
</style>
