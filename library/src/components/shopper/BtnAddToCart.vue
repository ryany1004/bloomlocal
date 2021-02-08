<template>
  <el-popover placement="bottom"
    :title="popup_title" width="300" trigger="manual"
    v-model="visible">
    <div class="form-add-to-cart">
      <div class="form-group" v-if="active_colors.length > 0">
        <div class="d-flex align-items-center">
          <label class="mr-3 mb-0">Color:</label>
          <span class="d-flex align-items-center">
            <span class="c-circle" :class="{active: color == active_color}" :style="{backgroundColor: color}"
                  v-show="active_colors.indexOf(color) != -1"
                  @click="active_color = color" v-for="color in colors" :key="color"></span>
          </span>
        </div>
        <p class="error" v-if="errors.color">Please choose color</p>
      </div>

      <div class="form-group" v-if="active_sizes.length > 0">
        <div class="d-flex align-items-center">
          <label class="mr-3 mb-0" style="width: 40px;flex: 0 0 40px;">Size:</label>
          <span class="flex-grow-1">
            <span class="badge mr-1 product-size white"
                  @click="active_size = size" v-for="size in sizes" v-show="active_sizes.indexOf(size) != -1"
                  :class="{'badge-success': size == active_size, 'badge-primary': size != active_size}"
                  :key="size">{{size}}</span>
          </span>
        </div>
        <p class="error" v-if="errors.size">Please choose size</p>
      </div>
      <div class="mt-3" style="text-align: right;">
        <el-button size="mini" type="text" @click="visible = false">cancel</el-button>
        <el-button type="primary" size="mini" @click="add_to_cart()">confirm</el-button>
      </div>
    </div>
    <a slot="reference" href="javascript:void(0)" @click="handleClick()" class="btn btn-primary btn-sm white"><i class="fas fa-plus"></i> Add to cart</a>
  </el-popover>
</template>

<script>
import _ from "lodash";
import {mapState} from "vuex";

export default {
  name: "BtnAddToCart",
  props: {
    product: {
      type: Object,
      required: true,
    }
  },
  data: function () {
    return {
      visible: false,
      active_size: null,
      active_color: null,
      errors: {}
    }
  },
  computed: {
    ...mapState(
        ['colors', 'sizes',]
    ),
    active_sizes() {
      let group = _.groupBy(this.product.variants, 'size');
      delete group[undefined];
      return Object.keys(group) || [];
    },
    active_colors() {
      let group = _.groupBy(this.product.variants, 'color');
      delete group[undefined];
      return Object.keys(group) || [];
    },
    popup_title()  {
      if (this.active_sizes.length > 0 && this.active_colors.length > 0) {
        return "Choose color and size";
      }
      return this.active_sizes.length > 0 ? "Choose size": "Choose color"
    }
  },
  methods: {
    valid_input() {
      let is_invalid = false;
      if (this.active_colors.length > 0 && this.active_color == null) {
        is_invalid = true
        this.$set(this.errors, 'color', true);
      }

      if (this.active_sizes.length > 0 && this.active_size == null) {
        this.$set(this.errors, 'size', true);
        is_invalid = true
      }

      return is_invalid;
    },
    add_to_cart() {
      this.errors = {};
      let is_invalid = this.valid_input(), that = this;
      if (is_invalid) {
        return;
      }
      let payload = {
        product_id: this.product.id,
        quantity: 1,
        size: this.active_size,
        color: this.active_color
      }
      this.$store.dispatch("add_to_cart", payload).then(() => {
        that.visible = false;
        that.active_size = null;
        that.active_color = null;
        that.$notify({
          title: 'Success',
          message: `${that.product.title} was added to your shopping cart.`,
          type: 'success',
          duration: 2000
        });
      });
    },
    handleClick() {
      if (this.active_colors.length == 0 && this.active_sizes == 0) {
        this.add_to_cart();
      } else {
        this.visible = true;
      }
    }
  }
}
</script>

<style lang="scss">
.form-add-to-cart {
  .error {
    color: red;
    font-size: 12px;
    margin-top: 8px;
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
  .product-size {
    cursor: pointer;
    padding: 0.5em;
  }
}
.el-notification__content {
  text-align: left;
}
.el-button--mini {
  outline: none !important;
}
</style>
