<template>
  <div class="d-flex justify-content-center align-items-center confirm-upload">
    <div class="text-center">
      <h5 class="mb-4" style="font-weight: normal">Product Upload</h5>
      <h3 class="mb-4">Confirmed</h3>
      <div class="mb-5 d-flex justify-content-center"><i class="fa fa-check-circle fa-3x"></i></div>
      <a href="/business/inventory/" class="btn btn-primary"><i class="fa fa-arrow-circle-left"></i> Back to invetory</a>
      </div>
  </div>
</template>

<script>
export default {
name: "ProductCofirmUpload"
}
</script>

<style scoped>
  .confirm-upload {
    height: calc(100vh - 150px);
    background-color: #f2f2f2;
    border-radius: 10px;
  }
</style>
