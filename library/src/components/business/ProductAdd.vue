<template>
  <div class="product-upload">
    <form>
      <div class="row">
        <div class="col-4">
          <el-upload
            class="product-uploader"
            action="https://jsonplaceholder.typicode.com/posts/"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <img v-if="product.thumbnail" :src="product.thumbnail" class="product-thumbnail">
            <div class="" v-else>
              <i  class="el-icon-plus avatar-uploader-icon">
                <span class="uploader-circle"></span>
              </i>
            </div>

          </el-upload>
          <p class="text-center">Upload Image</p>

          <div class="clearfix">
            <el-upload action="#" list-type="picture-card" :auto-upload="false" class="product-images">
                <i slot="default" class="el-icon-plus"></i>
                <div slot="file" slot-scope="{file}">
                  <img
                    class="el-upload-list__item-thumbnail"
                    :src="file.url" alt=""
                  >
                  <span class="el-upload-list__item-actions">
                    <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleRemove(file)">
                      <i class="el-icon-delete"></i>
                    </span>
                  </span>
                </div>
            </el-upload>
          </div>
          <button class="btn btn-primary btn-block mt-3"><i class="fas fa-upload"></i> Upload Product</button>
        </div>
        <div class="col-8">
          <div class="form-row">
            <div class="form-group col-md-8">
              <label for="product_tile">Product Title</label>
              <input type="text" maxlength="500" class="form-control w-75" id="product_tile" placeholder="">
            </div>
            <div class="form-group col-md-4">
              <label for="product_price">Set Price</label>
              <input type="number" class="form-control" id="product_price" placeholder="">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col">
              <label for="product_description">Description</label>
              <textarea class="form-control" id="product_description"></textarea>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-5">
              <div class="d-flex">
                <label for="product_tile" class="mr-4">Color</label>
                <el-switch v-model="product.enable_color"></el-switch>
              </div>
              <div>
                <span class="c-circle" :style="{backgroundColor: color.value}" v-for="color in colors" :key="color.value"
                      :class="{ active: color.value == active_color}" @click="set_active_color(color)"></span>
              </div>
            </div>
            <div class="form-group col-md-7">
              <div class="d-flex">
                <label for="product_tile" class="mr-4">Size</label>
                <el-switch v-model="product.enable_size"></el-switch>
              </div>
              <div>
                <span class="badge badge-primary mr-1" v-for="size in sizes" :key="size.value">{{size.text}}</span>
              </div>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-5">
              <label for="product_category">Category</label>
              <select class="form-control form-control-sm w-50" id="product_category" v-model="product.category">
                <option>1</option>
                <option>2</option>
                <option>3</option>
                <option>4</option>
                <option>5</option>
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
            <div class="form-group col">
              <label for="product_category">Product Dimensions</label>
              <div class="form-inline">
                <input type="number" class="form-control form-control-sm input-w50" v-model="product.length" placeholder="length"/> x
                <input type="number" class="form-control form-control-sm input-w50" v-model="product.width" placeholder="width"/> x
                <input type="number" class="form-control form-control-sm input-w50" v-model="product.height" placeholder="height"/>
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
                <input type="number" class="form-control input-w50 form-control-sm mr-1" v-model="product.weight"/>
                <select class="form-control form-control-sm input-w50" v-model="product.weight_unit">
                  <option value="lb">lb</option>
                </select>
              </div>
            </div>
            <div class="form-group col-3">
              <label for="product_category">Stock</label>
              <input type="number" v-model="product.stock" class="form-control form-control-sm input-w50"/>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import {mapState} from 'vuex';

export default {
  name: "ProductAdd",
  data: function () {
    return {
      product: {
        enable_color: true,
        enable_size: true,
        thumbnail: null,
        delivery_type: 'pickup',
        category: null,
        dimension_unit: 'cm',
        length: null,
        width: null,
        height: null,
        weight_unit: 'lb',
        weight: null,
        stock: null
      },
      delivery_types: [
        {value: 'pickup', text: "Pickup"},
        {value: 'delivery', text: "Delivery"},
        {value: 'both', text: "Both"},
      ],
      active_color: null
    }
  },
  created() {
    this.$store.dispatch('get_colors');
    this.$store.dispatch('get_sizes');
  },
  computed: {
    ...mapState(
            ['colors', 'sizes']
        ),
  },
  methods: {
    set_active_color(color) {
      this.active_color = color.value;
    },
    beforeAvatarUpload: function () {

    },
    handleAvatarSuccess: function () {

    },
    handleRemove: function(file) {
      console.log(file);
    },

  }
}
</script>

<style lang="scss">
  .product-upload {
    .form-inline .form-control.input-w50 {
      width: 80px;
    }
    .c-circle {
      width: 25px;
      height: 25px;
      display: inline-block;
      border-radius: 50%;
      border: 1px solid #00d1b2;
      margin-right: 2px;
      cursor: pointer;
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
      font-size: 28px;
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
      width: 178px;
      height: 178px;
      display: block;
    }
    .product-images .el-upload-list--picture-card .el-upload-list__item {
      width: 60px;
      height: 60px;
    }
    .product-images .el-upload--picture-card {
      width: 60px;
      height: 60px;
      line-height: 60px;
      float: left;
    }
  }
</style>
