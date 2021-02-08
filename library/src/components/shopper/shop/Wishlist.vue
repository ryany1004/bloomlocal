<template>
  <div>
    <a v-if="isLoggedIn" href="javascript:void(0)" @click="dialogVisible = true">
      <i class="fa-heart box-shadow" :class="{'fas': user.wishlist_products.indexOf(product.id) != -1,
        'far': user.wishlist_products.indexOf(product.id) == -1}"></i>
    </a>
    <el-dialog
      title="Add or remove the product to your Collections"
      :visible.sync="dialogVisible"
      width="30%" :close-on-click-modal="false" append-to-body>
      <div v-loading="loading">
        <ul class="collection-list">
          <li class="d-flex justify-content-between align-items-center">
            <div>
              <input type="text" :class="{'is-invalid': errors.collection_name}" placeholder="New Collection" class="form-control form-control-sm" v-model="new_collection.collection_name" maxlength="200"/>
            </div>
            <div>
              <button type="button" class="btn btn-primary btn-sm white font-12"  :disabled="new_collection.loading" @click="addProduct(new_collection)">Add</button>
            </div>
          </li>
          <li class="d-flex justify-content-between align-items-center" v-for="collection in collections" :key="collection.id">
            <div>
              <span>{{ collection.collection_name }} <span v-if="collection.products.length > 0">({{ countProduct(collection) }})</span></span>
            </div>
            <div>
              <button v-if="collection.products.indexOf(product.id) == -1" :disabled="collection.loading" type="button" class="btn btn-primary btn-sm white font-12" @click="addProduct(collection)">Add</button>
              <button v-else type="button" class="btn btn-danger btn-sm white font-12" :disabled="collection.loading" @click="addProduct(collection)">Remove</button>
            </div>
          </li>
        </ul>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false" class="el-button--small">Close</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {mapState} from "vuex";
import axios from "axios";

export default {
  name: "Wishlist",
  props: {
    product: {
      required: true,
      type: Object
    }
  },
  data() {
    return {
      dialogVisible: false,
      collections: [],
      loading: false,
      new_collection: {collection_name: ""},
      errors: {}
    }
  },
  computed: {
    ...mapState([
        'isLoggedIn', 'user'
    ]),
  },
  watch: {
    dialogVisible: {
      immediate: true,
      handler(val) {
        if (val) {
          this.loadCollections();
        }
      }
    }
  },
  methods: {
    loadCollections() {
      let that = this;
      that.loading = true;
      axios.get('/api/user/collections/?simple=1').then(res => {
        that.collections = res.data;
        that.loading = false
      }).catch(() => {
        that.loading = false
      })
    },
    addProduct(collection) {
      if (!collection.id) {
        if (collection.collection_name.trim() == "") {
          this.errors = {collection_name: true}
          return;
        }
      }
      let that = this;
      that.errors = {};
      let data = {
        collection: collection
      }
      collection.loading = true;
      axios.post(`/api/user/product/${this.product.id}/collection/`, data).then(res => {
        collection.loading = false;
        if (collection.id) {
          collection.collection_name = res.data.collection.collection_name;
          collection.products = res.data.collection.products;
        } else {
          that.collections.push(res.data.collection);
          that.new_collection = {collection_name: ""};
        }
        that.$store.dispatch('set_user', res.data.user);
        that.collection_name = "";
      }).catch(() => {
        collection.loading = false;
        alert("Error");
      })
    },
    countProduct(collection) {
      if (collection.products.length == 1) {
        return "1 product";
      }
      return collection.products.length + " products";
    }
  }
}
</script>

<style lang="scss">
.collection-list {
  list-style: none;
  padding-left: 0;
  li {
    padding: 5px 0;
  }
}
</style>
<style scoped>
.fa-heart.fas {
  color: #ED6B5E;
}
.box-shadow {
  -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
  -moz-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
}
</style>
