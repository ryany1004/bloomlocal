<template>
  <div class="variants" v-show="sizes.length > 0 || colors.length > 0">
    <el-table
      :data="variants" stripe
      style="width: 100%">
      <el-table-column
        label="Variant"
        width="180">
        <template slot-scope="scope">
          <span class="font-14">{{ show_variant(scope.row) }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="Price"
        width="100">
        <template slot-scope="scope">
          <vue-number-input v-model="scope.row.price" @change="emitVariants()"
            placeholder="0" :min="0" size="small"></vue-number-input>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import VueNumberInput from '@chenfengyuan/vue-number-input';

export default {
  name: "Variants",
  components: {
    VueNumberInput
  },
  props: {
    sizes: {
      type: Object,
      default: () => []
    },
    colors: {
      type: Object,
      default: () => []
    },
    value: {
      type: Object
    }
  },
  computed: {
    price_variants() {
      let data = {};
      this.value.forEach(variant => {
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
    variants() {
      let that = this, variants = [];
      if (that.colors.length > 0 && that.sizes.length == 0) {
        that.colors.forEach(function (color) {
          variants.push({color: color, price: that.price_variants[color] || null});
        })
      } else if (that.colors.length == 0 && that.sizes.length > 0) {
        that.sizes.forEach(function (size) {
          variants.push({size: size, price: that.price_variants[size] || null});
        })
      } else {
        that.colors.forEach(function (color) {
          that.sizes.forEach(function (size) {
            variants.push({size: size, color: color, price: that.price_variants[`${size}:${color}`] || null});
          })
        })
      }
      return variants;
    }
  },
  data() {
    return {
    }
  },
  methods: {
    show_variant(variant) {
      let v = [];
      if (variant.size) {
        v.push(variant.size)
      }
      if (variant.color) {
        v.push(variant.color)
      }
      return v.join(" / ");
    },
    emitVariants() {
      this.$emit("input", this.variants)
    }
  }
}
</script>

<style scoped>

</style>
