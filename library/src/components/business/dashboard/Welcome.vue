<template>
  <div class="wbox welcome">
    <p class="welcome-text">Welcome to your Bloom dashboard.</p>
    <div class="row pt-2">
      <div class="col-6 manage">
        <a href="/business/my-orders/" class=" btn-manage">
          <i class="m-icon m-orders"></i>
          <span class="m-btn-text">
            <span class="m-text">Manage Orders</span>
            <span class="m-sub-text">Update Dashboard</span>
          </span>
        </a>
      </div>
      <div class="col-6 manage">
        <a href="javascript:void(0)" class=" btn-manage">
          <i class="m-icon m-products"></i>
          <span class="m-btn-text">
            <span class="m-text">Manage Products</span>
            <span class="m-sub-text">An event date update again</span>
          </span>
        </a>
      </div>
      <div class="col-6 manage">
        <a href="javascript:void(0)" class=" btn-manage">
          <i class="m-icon m-store"></i>
          <span class="m-btn-text">
            <span class="m-text">Manage Store</span>
            <span class="m-sub-text">Update your profile</span>
          </span>
        </a>
      </div>
      <div class="col-6 manage">
        <a href="javascript:void(0)" class=" btn-manage">
          <i class="m-icon m-notification"></i>
          <span class="m-btn-text">
            <span class="m-text">Manage Notifications</span>
            <span class="m-sub-text">Check Your running application</span>
          </span>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
name: "Welcome"
}
</script>

<style scoped>

</style>
