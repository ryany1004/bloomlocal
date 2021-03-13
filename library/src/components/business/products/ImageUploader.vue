<template>
  <div class="p-image-uploader">
    <el-upload action="" class="" :show-file-list="false"
      :http-request="handleImgsUpload" :auto-upload="true" :before-upload="beforeUpload"
      :on-success="handleImgsSuccess">
        <div v-if="value" :style="{backgroundImage: `url('${mediaUrl + value}'`}" class="el-upload-img"></div>
        <i v-else class="el-icon-plus img-uploader-icon">
          <span class="uploader-circle"></span>
        </i>

        <div v-if="percent > 0" class="progress" style="height: 1px;">
          <div class="progress-bar" role="progressbar" :style="{width: percent + '%'}" style="width: 0%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
    </el-upload>
    <span v-if="value" class="el-upload-list__item-actions">
      <span class="el-upload-list__item-delete" @click="handleRemove">
        <i class="el-icon-delete"></i>
      </span>
    </span>
  </div>
</template>

<script>
import $ from "jquery";

export default {
  name: "ImageUploader",
  props: {
    value: {
      type: Object,
      required: true
    },
    mediaUrl: {
      type: String,
      default: ""
    },
  },
  data() {
    return {
      percent: 0
    }
  },
  methods: {
    handleImgsUpload(data) {
      let that = this;
      let params = {
        filename: data.file.name,
        content_type: data.file.type,
        prefix: "product/imgs/"
      }
      this.axios.post('/api/shop/upload/generate-url/',params, ).then(function (res) {
        $.ajax({
            url: res.data.url,
            type: 'PUT',
            data: data.file,
            contentType: data.file.type,
            xhr: function () {
              let myXhr = $.ajaxSettings.xhr();
              if (myXhr.upload) {
                  myXhr.upload.addEventListener('progress', that.progressHandling2, false);
              }
              return myXhr;
            },
            success: function () {
              that.$emit('input', res.data.path);
              data.onSuccess(res.data.path)
            },
            error: function (result) {
                console.log(result);
                alert("Error while uploading.");
            },
            processData: false
        });
      });
    },
    handleImgsSuccess(file) {
      this.percent = 0
      console.log(file)
    },
    beforeUpload: function (file) {
      const isJPG = ['image/jpeg', "image/png", "image/webp"].indexOf(file.type) != -1;
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('Image must be JPG, PNG format!');
      }
      if (!isLt2M) {
        this.$message.error('Image size can not exceed 2MB!');
      }
      return isJPG && isLt2M;
    },
    handleRemove: function(e) {
      e.preventDefault();
      this.$emit('input', "");

    },
    progressHandling2(event) {
      let percent = 0;
      let position = event.loaded || event.position;
      let total = event.total;
      if (event.lengthComputable) {
        percent = Math.ceil(position / total * 100);
        this.percent = percent;
      }
    },
  }
}
</script>

<style lang="scss">
.p-image-uploader {
  position: relative;
  .el-upload {
    position: relative;
  }
  .img-uploader-icon {
    width: 100px;
    height: 80px;
    background: #F4F6F8;
    border-radius: 8px;
    line-height: 80px;
    color: #00AEEF;
  }
  .el-upload-img {
    width: 100px;
    height: 80px;
    border-radius: 8px;
    background-position: center;
    background-size: contain;
    background-repeat: no-repeat;
    border: 1px solid #e4e4e4;
  }
  .el-upload-list__item-actions {
    position: absolute;
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    cursor: default;
    text-align: center;
    color: #fff;
    opacity: 0;
    font-size: 20px;
    background-color: rgba(0,0,0,.5);
    transition: opacity .3s;
    border-radius: 8px;
    z-index: 99;
  }
}
.p-image-uploader:hover {
  .el-upload-list__item-actions:hover {
    opacity: 1;
  }
  .el-upload-list__item-delete {
    position: static !important;
    line-height: 80px;
    font-size: inherit;
    color: inherit;
    display: inline-block;
  }
}
</style>
