<template>
  <div v-loading="loading">
    <a class="btn btn-primary btn-sm white font-12" @click="dialogVisible = true"><i class="fas fa-plus"></i> Add a address</a>
    <el-table
        :data="addresses" row-class-name="font-12"
        style="width: 100%">
      <el-table-column
          prop="country"
          width="90"
          label="Country">
      </el-table-column>
      <el-table-column
          label="Full Name">
        <template slot-scope="scope">
          <a href="javascript:void(0)" @click="handleSelect(scope.row)">{{ scope.row.first_name }}
            {{ scope.row.last_name }}</a>
        </template>
      </el-table-column>
      <el-table-column
          prop="street_address"
          width="130"
          label="Street Address">
      </el-table-column>
      <el-table-column
          prop="city"
          label="City">
      </el-table-column>
      <el-table-column
          prop="state"
          label="State">
      </el-table-column>
      <el-table-column
          prop="zip_code"
          label="Zip Code">
      </el-table-column>
      <el-table-column
          prop="email"
          label="Email">
      </el-table-column>
      <el-table-column
          prop="phone_number"
          label="Phone">
      </el-table-column>
      <el-table-column width="50">
        <template slot-scope="scope">
          <a href="javascript:void(0)" @click="delete_address(scope.row)"><i class="fas fa-trash-alt"></i></a>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      title="Add a Address"
      :visible.sync="dialogVisible" width="40%" append-to-body :close-on-click-modal="false">
      <div v-loading="saving">
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="country">Country or Region</label>
            <country-select id="country" v-model="shipping_address.country" :country="shipping_address.country" topCountry="US" className="form-control" :class="{'is-invalid': errors.country}"/>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="first_name">First name</label>
            <input type="text" class="form-control" id="first_name" name="first_name" v-model="shipping_address.first_name" :class="{'is-invalid': errors.first_name}">
          </div>
          <div class="form-group col-md-6">
            <label for="last_name">Last name</label>
            <input type="text" class="form-control" id="last_name" name="last_name" v-model="shipping_address.last_name" :class="{'is-invalid': errors.last_name}">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="first_name">Street Address</label>
            <input type="text" class="form-control" id="street_address" name="street_address" v-model="shipping_address.street_address" :class="{'is-invalid': errors.street_address}">
          </div>
          <div class="form-group col-md-6">
            <label for="last_name">Street Address 2 (Optional)</label>
            <input type="text" class="form-control" id="street_address_2" name="street_address_2" v-model="shipping_address.street_address_2" :class="{'is-invalid': errors.street_address_2}">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-3">
            <label for="city">City</label>
            <input type="text" class="form-control" id="city" name="city" v-model="shipping_address.city" :class="{'is-invalid': errors.city}">
          </div>
          <div class="form-group col-md-6">
            <label for="state">State/Province/Region</label>
            <input type="text" class="form-control" id="state" name="state" v-model="shipping_address.state" :class="{'is-invalid': errors.state}">
          </div>
          <div class="form-group col-md-3">
            <label for="zip_code">Zip Code</label>
            <input type="text" class="form-control" id="zip_code" name="zip_code" v-model="shipping_address.zip_code" :class="{'is-invalid': errors.zip_code}">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="email">Email</label>
            <input type="text" class="form-control" id="email" name="email" v-model="shipping_address.email" :class="{'is-invalid': errors.email}">
          </div>
          <div class="form-group col-md-6">
            <label for="confirm_email">Confirm Email</label>
            <input type="text" class="form-control" id="confirm_email" name="confirm_email" v-model="shipping_address.confirm_email" :class="{'is-invalid': errors.confirm_email}">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-12">
            <label for="phone">Phone</label>
            <vue-phone-number-input ref="phone_input" id="phone" @update="onUpdate" v-model="shipping_address.phone" name="phone_number" :required="true" :class="{'is-invalid': errors.phone_number}"/>
          </div>
        </div>

        <button class="btn btn-primary btn-block white" @click="addAddress()"> Add</button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SavedAddresses",
  props: {
    selectAddress: {
      type: Function,
      required: true
    },
  },
  data() {
    return {
      loading: false,
      addresses: [],
      dialogVisible: false,
      shipping_address: {
        country: "",
        first_name: "",
        last_name: "",
        street_address: "",
        street_address_2: "",
        city: "",
        state: "",
        zip_code: "",
        email: "",
        confirm_email: "",
        phone_number: "",
        phone: ""
      },
      errors: {},
      saving: false
    }
  },
  created() {
    this.get_saved_address();
  },
  methods: {
    onUpdate(payload) {
      this.shipping_address.phone_number = payload.formatInternational || '';
    },
    get_saved_address() {
      let that = this;
      that.loading = true;
      axios.get("/api/user/saved-addresses/").then(res => {
        that.loading = false;
        that.addresses = res.data;
      })
    },
    handleSelect(address) {
      this.selectAddress(address);
    },
    addAddress() {
      let data = this.shipping_address, that = this;
      that.saving = true;
      axios.post("/api/user/saved-addresses/", data).then((res) => {
        that.errors = {};
        that.addresses.push(res.data);
        that.dialogVisible = false;
        that.saving = false;
      }).catch((err) => {
        that.saving = false;
        if (err.response.data) {
          that.errors = err.response.data;
        }
      })
    },
    delete_address(address) {
      let that = this;
      if (confirm("Are you sure?")) {
        that.loading = true;
        axios.delete(`/api/user/saved-address/${address.id}/`).then(() => {
          let index = that.addresses.indexOf(address);
          if (index != -1) {
            that.$delete(that.addresses, index);
          }
          that.loading = false;
        }).catch(() => {
          that.loading = false;
          alert("Unable to delete this address!")
        })
      }
    }
  }
}
</script>

<style scoped>

</style>
