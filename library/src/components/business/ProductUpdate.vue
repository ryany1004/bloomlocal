<template>
  <div v-loading.fullscreen="loading" class="product-update" >
    <form v-if="product.id">
      <div class="row">
        <div class="col-md-4 col-12">
          <el-upload
            class="product-uploader"
            action=""
            :show-file-list="false"
            :http-request="handleThumbnailUpload"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <div v-if="product.thumbnail" :style="{backgroundImage: `url(${mediaUrl}${product.thumbnail}`}" class="product-thumbnail"></div>
            <div class="" v-else>
              <i  class="el-icon-plus avatar-uploader-icon">
                <span class="uploader-circle"></span>
              </i>
            </div>
            <div class="progress" style="height: 1px;">
              <div class="progress-bar" role="progressbar" :style="{width: percent + '%'}" style="width: 0%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </el-upload>

          <div class="clearfix mt-4">
            <el-upload action="" list-type="picture-card" :file-list="product_imgs" class="product-images"
              :http-request="handleImgsUpload" :auto-upload="true"
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
          <div class="d-flex mt-2" v-if="edit.images">
            <button class="btn btn-primary btn-sm" type="button" :disabled="saving.description" @click="saveProductImages()"><i class="fas fa-upload"></i> Submit product</button>
            <button class="btn btn-secondary btn-sm ml-3" type="button" @click="hide_edit_images()"><i class="fas fa-times"></i></button>
          </div>
        </div>
        <div class="col-md-8 col-12">
          <div>
            <div class="form-group mb-4">
              <div v-if="edit.title" class="form-inline">
                <input  :class="{'is-invalid': errs.title}" type="text" maxlength="500" class="form-control w-75" id="product_tile" placeholder="" v-model="product.title">
                <button class="btn btn-primary btn-sm mx-3" type="button" :disabled="saving.title" @click="saveProduct('title')"><i class="fas fa-check"></i></button>
                <button class="btn btn-secondary btn-sm" type="button" @click="hide_edit('title')"><i class="fas fa-times"></i></button>
              </div>
              <h3 class="text-1 color-1" v-else><span>{{product.title}}</span> <a href="javascript:void(0)" @click="enable_edit('title')"><i class="fas fa-edit edit-icon"></i></a></h3>
            </div>
            <div class="mb-2">
              <el-rate v-model="product.rating" show-score disabled text-color="#000" score-template="({value})"></el-rate>
            </div>
            <div class="form-group mb-4">
              <div v-if="edit.price" class="form-inline">
                <ValidationProvider rules="positive" v-slot="{ errors }">
                <input type="number" min="0" :class="{'is-invalid': errors.length > 0 || errs.price}" class="form-control" id="product_price" placeholder="" v-model="product.price">
                </ValidationProvider>
                <button class="btn btn-primary btn-sm mx-3" type="button" :disabled="saving.price" @click="saveProduct('price')"><i class="fas fa-check"></i></button>
                <button class="btn btn-secondary btn-sm" type="button" @click="hide_edit('price')"><i class="fas fa-times"></i></button>
              </div>
              <h4 class="text-1 color-1" v-else><span>${{product.price}}</span> <a href="javascript:void(0)" @click="enable_edit('price')"><i class="fas fa-edit edit-icon"></i></a></h4>
            </div>
            <div class="form-group">
              <h5 class="text-2">Product Description <a href="javascript:void(0)" @click="enable_edit('description')"><i class="fas fa-edit edit-icon"></i></a></h5>
              <div v-if="edit.description">
                <textarea :class="{'is-invalid': errs.description}" class="form-control" id="product_description" v-model="product.description"></textarea>
                <div class="d-flex mt-2">
                  <button class="btn btn-primary btn-sm" type="button" :disabled="saving.description" @click="saveProduct('description')"><i class="fas fa-check"></i></button>
                  <button class="btn btn-secondary btn-sm ml-3" type="button" @click="hide_edit('description')"><i class="fas fa-times"></i></button>
                </div>
              </div>
              <div style="white-space: pre-line;" v-else>
                {{product.description}}
              </div>
            </div>
            <div class="form-group d-flex justify-content-between">
              <div class="d-flex align-items-center">
                <label class="mr-3 mb-0" :class="{disabled: !product.enable_color || active_colors.length == 0}">Color:</label>
                <div v-if="edit.color" class="form-inline">
                  <span :class="{disabled: !product.enable_color}">
                    <span class="c-circle" :style="{backgroundColor: color.value}" v-for="color in colors" :key="color.value"
                      :class="{ active: active_colors.indexOf(color.value) != -1}" @click="toggleColor(color)"></span>
                  </span>
                  <button class="btn btn-primary btn-sm mx-3" type="button" :disabled="saving.color" @click="saveProductVariants('color')"><i class="fas fa-check"></i></button>
                  <button class="btn btn-secondary btn-sm" type="button" @click="hide_edit('color')"><i class="fas fa-times"></i></button>
                </div>
                <span v-else class="d-flex align-items-center">
                  <span class="c-circle" :style="{backgroundColor: color.value}" v-show="active_colors.indexOf(color.value) != -1" v-for="color in colors" :key="color.value"></span>
                  <a class="ml-3" href="javascript:void(0)" @click="enable_edit('color')"><i class="fas fa-edit edit-icon"></i></a>
                </span>
              </div>
              <div>
                <el-switch v-if="edit.color" v-model="product.enable_color" @change="reset_attribute('color')"></el-switch>
              </div>
            </div>
            <div class="form-group d-flex align-items-center">
              <label class="mr-2 mb-0">Categories:</label>
              <div v-if="edit.categories" class="form-inline">
                <el-select v-model="product.categories" collapse-tags multiple placeholder="Categories" :class="{'is-invalid': errs.categories}">
                  <el-option
                    v-for="item in categories"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id">
                  </el-option>
                </el-select>
                <button class="btn btn-primary btn-sm mx-3" type="button" :disabled="saving.categories" @click="saveProduct('categories')"><i class="fas fa-check"></i></button>
                <button class="btn btn-secondary btn-sm" type="button" @click="hide_edit('categories')"><i class="fas fa-times"></i></button>
              </div>
              <div v-else><span>{{product.category_names.join(", ")}}</span> <a href="javascript:void(0)" @click="enable_edit('categories')"><i class="fas fa-edit edit-icon"></i></a></div>
            </div>
            <div class="form-group d-flex justify-content-between">
              <div class="d-flex align-items-center">
                <label class="mr-3 mb-0" :class="{disabled: !product.enable_size || active_sizes.length == 0}">Size:</label>
                <div v-if="edit.size">
                  <span :class="{disabled: !product.enable_size}">
                    <span @click="toggleSize(size)" :class="{'badge-secondary': active_sizes.indexOf(size.value) == -1, 'badge-primary': active_sizes.indexOf(size.value) != -1}" class="badge mr-1 product-size"
                                                                         v-for="size in sizes" :key="size.value">{{size.text}}</span>
                  </span>
                  <div class="mt-2">
                    <button class="btn btn-primary btn-sm mr-3" type="button" :disabled="saving.size" @click="saveProductVariants('size')"><i class="fas fa-check"></i></button>
                    <button class="btn btn-secondary btn-sm" type="button" @click="hide_edit('size')"><i class="fas fa-times"></i></button>
                  </div>
                </div>
                <span v-else class="d-flex align-items-center">
                  <span class="badge badge-primary mr-1 product-size white" v-show="active_sizes.indexOf(size.value) != -1" v-for="size in sizes" :key="size.value">{{size.text}}</span>
                  <a class="ml-3" href="javascript:void(0)" @click="enable_edit('size')"><i class="fas fa-edit edit-icon"></i></a>
                </span>
              </div>
              <div>
                <el-switch v-if="edit.size" v-model="product.enable_size"  @change="reset_attribute('size')"></el-switch>
              </div>
            </div>
            <div class="form-group d-flex align-items-center">
              <label class="mr-3 mb-0">Stock:</label>
              <div v-if="edit.stock" class="form-inline">
                <ValidationProvider rules="positive" v-slot="{ errors }">
                <input type="number" min="0" :class="{'is-invalid': errors.length > 0 || errs.stock }" v-model="product.stock" class="form-control form-control-sm input-w50"/>
                </ValidationProvider>
                <button class="btn btn-primary btn-sm mx-3" type="button" :disabled="saving.stock" @click="saveProduct('stock')"><i class="fas fa-check"></i></button>
                <button class="btn btn-secondary btn-sm" type="button" @click="hide_edit('stock')"><i class="fas fa-times"></i></button>
              </div>
              <div v-else><span class="white bg-1 p-stock">{{product.stock}}</span> <a href="javascript:void(0)" @click="enable_edit('stock')"><i class="fas fa-edit edit-icon"></i></a></div>
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
    </form>
  </div>
</template>

<script>
import {mapState} from 'vuex';
import $ from 'jquery'
import axios from "axios";
import _ from "lodash";
import { ValidationProvider, extend } from 'vee-validate';

extend('positive', value => {
  return value >= 0;
});

export default {
  name: "ProductUpdate",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    productId: {
      required: true
    }
  },
  components: {
    ValidationProvider
  },
  data: function () {
    return {
      backup_product: {},
      product: {},
      percent: 0,
      percent2: 0,
      product_imgs: [],
      delivery_types: [
        {value: 'pickup', text: "Pickup"},
        {value: 'delivery', text: "Delivery"},
        {value: 'both', text: "Both"},
      ],
      active_color: null,
      active_sizes: [],
      active_colors: [],
      variants: [],
      uploaded: false,
      errs: {},
      loading: false,
      saving: {},
      edit: {}
    }
  },
  created() {
    this.get_product();
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
    get_product() {
      let that = this;
      that.loading = true
      axios.get(`/api/shop/product/${this.productId}/`).then(function (res) {
        that.product = res.data;
        that.backup_product = JSON.parse(JSON.stringify(res.data));
        that.product_imgs = res.data.images
        that.variants = res.data.variants;
        that.set_active_sizes_and_color(res.data);
        that.loading = false;
      }).catch(function () {
        that.loading = false
      })
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
    reset_attribute(attr) {
      if (attr == 'color' && !this.product.enable_color) {
        this.active_colors = [];
      } else if (attr == 'size' && !this.product.enable_size) {
        this.active_sizes = [];
      }
    },
    enable_edit(field) {
      this.$set(this.edit, field, true);
    },
    hide_edit_images() {
      this.$set(this.edit, 'images', false);
      this.product.thumbnail = this.backup_product.thumbnail;
      this.product_imgs = JSON.parse(JSON.stringify(this.backup_product.images));
    },
    hide_edit(_field) {
      let field = _field;
      if (field == 'size' || field == 'color') {
        this.$set(this.edit, field, false);
        field = 'variants';
      } else {
        this.$set(this.edit, field, false);
      }

      let data = this.backup_product[field];
      if (typeof data != 'object') {
        this.product[field] = data;
      } else {
        this.product[field] = JSON.parse(JSON.stringify(data));
        if (field == 'variants') {
          this.product.enable_size = this.backup_product.enable_size;
          this.product.enable_color = this.backup_product.enable_color;
          this.set_active_sizes_and_color(this.product);
        }
      }
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
              that.$set(that.edit, 'images', true);
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
              that.$set(that.edit, 'images', true);
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
    beforeAvatarUpload: function () {

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
        this.$set(this.edit, 'images', true);
      }
    },
    saveProduct(field) {
      let data = {}, that=this;
      that.errs = {};
      if (field == 'categories') {
        data = new FormData();
        if (that.product.categories.length == 0) {
          that.$set(that.errs, field, true);
          return;
        }
        that.product.categories.forEach(function (item) {
          data.append('categories', item);
        })
      } else {
        data[field] = this.product[field];
      }
      that.$set(that.saving, field, true);
      axios.patch(`/api/shop/product/${this.product.uuid}/`, data).then(function (res) {
        that.errs = {}
        that.$set(that.saving, field, false);
        that.edit[field] = false;
        if (field == 'categories') {
          that.product.category_names = res.data.category_names;
        }
        that.backup_product[field] = res.data[field];
        that.uploaded = true
      }).catch(function (err) {
        that.$set(that.saving, field, false);
        if(err.response.data) {
          that.errs = err.response.data;
        }
        console.log(err);
      })
    },
    saveProductImages() {
      let that = this;
      let data = {
        thumbnail: this.product.thumbnail,
        images: this.product_imgs
      }
      that.$set(that.saving, 'images', true);
      axios.patch(`/api/shop/product/attribute/${this.product.uuid}/`, data).then(function (res) {
        that.$set(that.saving, 'images', false);
        that.$set(that.edit, 'images', false);
        that.backup_product.thumbnail = res.data.thumbnail;
        that.backup_product.images = res.data.images;
        that.product.images = res.data.images;
      }).catch(function (err) {
        that.$set(that.saving, 'images', false);
        if(err.response.data) {
          that.errs = err.response.data;
        }
        console.log(err);
      })
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
    saveProductVariants(attr) {
      let that = this;

      let data = {
        enable_color: this.product.enable_color,
        enable_size: this.product.enable_size,
        variants: this.getVariants()
      }
      that.$set(that.saving, attr, true);
      axios.patch(`/api/shop/product/attribute/${this.product.uuid}/`, data).then(function (res) {
        that.$set(that.saving, attr, false);
        that.$set(that.edit, attr, false);
        that.product.variants = res.data.variants;
        that.backup_product.variants = res.data.variants;
        that.backup_product.enable_color = res.data.enable_color;
        that.backup_product.enable_size = res.data.enable_size;
        that.set_active_sizes_and_color(this.product);
      }).catch(function (err) {
        that.$set(that.saving, attr, false);
        console.log(err);
      })
    },
    changeColor(color) {
      let that = this;
      if (this.product.enable_size && this.product.enable_color) {
        let active_color_variant_group = _.groupBy(this.variants, 'color')[color.value] || [];
        let active_sizes = [];
        active_color_variant_group.forEach(function (item) {
          active_sizes.push(item.size)
        })
        this.active_sizes = active_sizes
        this.active_color = color.value;
        this.active_colors = [];
      } else if (!this.product.enable_size && this.product.enable_color) {
        this.active_color = null;
        let index = this.active_colors.indexOf(color.value)
        if (index != -1) {
          this.$delete(this.active_colors, index);
        } else {
          this.active_colors.push(color.value)
        }
        this.variants = [];
        this.active_colors.forEach(function (color) {
          that.variants.push({color: color});
        })
      }
      console.log(this.variants)
    },
    toggleSize(size) {
      let index = this.active_sizes.indexOf(size.value);
      if ( index != -1) {
        this.$delete(this.active_sizes, index);
      } else {
        this.active_sizes.push(size.value);
      }
    },
    toggleColor(color) {
      let index = this.active_colors.indexOf(color.value);
      if ( index != -1) {
        this.$delete(this.active_colors, index);
      } else {
        this.active_colors.push(color.value);
      }
    }
  }
}
</script>

<style lang="scss">
  .disabled {
    pointer-events: none;
    opacity: 0.5;
  }
  .product-update {
    .edit-icon {
      font-size: 14px;
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
      margin-right: 14px;
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
      background-size: contain;
      background-repeat: no-repeat;
    }
    .product-images {
      .el-upload-list--picture-card .el-upload-list__item {
        width: 60px;
        height: 60px;
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
          font-size: 18px;
        }
        .content {
          font-size: 12px;
          color: #4F4F4F;
        }
      }
    }
    .el-select.is-invalid {
      border: 1px solid #dc3545;
      border-radius: 6px;
    }
  }
</style>
