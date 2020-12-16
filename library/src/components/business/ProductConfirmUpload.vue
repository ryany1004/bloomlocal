<template>
  <div class="d-flex justify-content-center align-items-center confirm-upload">
    <div class="text-center">
      <h5 class="mb-4" style="font-weight: normal;font-size: 90%">Product Upload</h5>
      <h3 class="mb-4">Confirmed</h3>
      <div class="mb-5 d-flex justify-content-center"><i class="fa fa-check-circle fa-3x color-1"></i></div>
      <a href="/business/inventory/" class="btn btn-primary white">
        <svg width="17" height="14" viewBox="0 0 17 17" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M8.62757 11.7218L7.21641 13.139L0.838745 6.7888L7.18897 0.411133L8.60623 1.82229L4.82971 5.61514L15.1353 5.59292C17.3445 5.58815 19.1392 7.37515 19.144 9.58428L19.1612 17.5843L17.1612 17.5886L17.144 9.5886C17.1416 8.48403 16.2442 7.59053 15.1396 7.59291L4.50391 7.61584L8.62757 11.7218Z" fill="#FEFEFE"/>
          </svg> Back to invetory
      </a>
    </div>
  </div>
</template>

<script>
export default {
name: "ProductConfirmUpload"
}
</script>

<style scoped>
  .confirm-upload {
    height: calc(100vh - 150px);
    background-color: #f2f2f2;
    border-radius: 10px;
  }
</style>
