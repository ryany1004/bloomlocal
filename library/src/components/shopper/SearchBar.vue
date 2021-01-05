<template>
  <div class="input-group search-bar">
    <input type="text" v-model="query" class="form-control" v-on:keyup.enter="handleClick()" placeholder="Search" aria-label="Search" aria-describedby="button-addon2">
    <select class="custom-select" v-model="type" @change="handleChange()">
      <option selected value="all">All</option>
      <option value="shop">Shop</option>
      <option value="product">Product</option>
    </select>
    <div class="input-group-append">
      <button class="btn btn-primary btn-sm" type="button" id="button-addon2" @click="handleClick()"><i class="far fa-search white"></i></button>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchBar",
  data: function () {
    return {
      type: 'all',
      query: ''
    }
  },
  created() {
    let types = ['all', 'shop', 'product'], type;
    let uri = window.location.search.substring(1);
    let params = new URLSearchParams(uri);
    this.query = params.get('query') || '';
    if (params.get("search_type") && types.indexOf(params.get("search_type")) != -1) {
      type = params.get("search_type")
    } else {
      type = localStorage.getItem("search_type") || "all";
    }
    if (['all', 'shop', 'product'].indexOf(type) != -1) {
      this.type = type;
    }
  },
  methods: {
    handleClick() {
      window.location = `/search/?type=${this.type}&query=${this.query}`;
    },
    handleChange() {
      localStorage.setItem('search_type', this.type);
    }
  }
}
</script>

<style lang="scss">
.search-bar {
  input {
    font-size: 14px;
  }
  .custom-select {
    flex: 0 0 110px !important;
    font-size: 14px
  }
}
</style>
