<template>
  <section class="store-product px-3">
    <a :href="`/business/product/${product.uuid}/update/`">
      <div class="card-image" :style="{backgroundImage: `url('${mediaUrl}${product.thumbnail}')`}">
<!--        <input v-if="selectable" type="checkbox" v-model="product.checked" :checked="product.checked" class="select-product"/>-->
      </div>
    </a>
    <div class="d-flex mt-5">
      <span class="s-price">${{ product.price | numFormat("0,000.00") }}</span>
      <span class="on-sale ml-auto">SALE</span>
    </div>
    <article class="mt-3">
      <h2 :title="product.title" class="mt-2"><a :href="`/business/product/${product.uuid}/update/`">{{product.title}}</a></h2>
    </article>
    <footer class="d-flex justify-content-between align-items-center">
      <div class="d-flex align-items-center">
        <i class="icon-16 icon-shop"></i> <span class="font-12 ml-2" style="color: #959EAD">{{ product.shop_data.name }}</span>
      </div>
      <div>
        <i class="fas fa-star"></i> <span class="font-14" style="color: #161D25">4,6</span>
      </div>
    </footer>
  </section>
</template>

<script>
export default {
  name: "StoreProductCard",
  props: {
    product: {
      type: Object,
      required: true
    },
    mediaUrl: {
      type: String,
      default: ""
    },
  }
}
</script>

<style lang="scss">
.store-product {
  .card-image {
    height: 180px;
    width: 100%;
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;
    .select-product {
      position: absolute;
      right: 10px;
      top: 10px;
    }
  }
  article {
    h2 {
      font-size: 18px;
      font-weight: 500;
      a {
        color: #161D25;
      }
    }
  }
  .s-price {
    color: #50B83C;
    font-size: 16px;
  }
  .on-sale {
    font-size: 12px;
    color: #DE3618;
    padding: 3px 10px;
    background: #fcebe8;
    border-radius: 4px;
    font-weight: 500;
  }
  .icon-shop {
    background: url("../../../assets/icons/icon-shop-16.png") no-repeat;
  }
  .fa-star {
    color: #EEC200;
  }
}
</style>
