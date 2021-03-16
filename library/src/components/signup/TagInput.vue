<template>
  <div class='tag-input'>
    <div v-for='(tag, index) in tags' :key='tag' class='tag-input__tag'>
      {{ tag }}
      <span @click='removeTag(index)'>x</span>
    </div>
    <input
      type='text'
      placeholder="Type keyword and press enter"
      class='tag-input__text'
      @keydown.enter='addTag'
      @keydown.188='addTag'
      @keydown.delete='removeLastTag'
      :disabled="tags.length >= 8"
    />
  </div>
</template>
<script>
export default {
  props: ['inputTag'],
  data () {
    return {
      tags: this.inputTag
    }
  },
  methods: {
    addTag (event) {
        event.preventDefault()
        let val = event.target.value.trim()
        if (val.length > 0) {
            this.tags.push(val)
            event.target.value = ''
        }
        this.emitTags();
    },
    removeTag (index) {
      this.tags.splice(index, 1)
      this.emitTags();
    },
    removeLastTag(event) {
      if (event.target.value.length === 0) {
        this.removeTag(this.tags.length - 1)
      }
    },
    emitTags(){
        this.$emit('inputTags', this.tags);
    }
  }
}
</script>
<style scoped>
.tag-input {
  width: 100%;
  height: 100%;
  border: 1px solid #eee;
  font-size: 0.9em;
  /* height: 50px; */
  box-sizing: border-box;
  padding: 0 10px;
}

.tag-input__tag {
  height: 30px;
  float: left;
  margin-right: 10px;
  background-color: #eee;
  margin-top: 10px;
  line-height: 30px;
  padding: 0 5px;
  border-radius: 5px;
}

.tag-input__tag > span {
  cursor: pointer;
  opacity: 0.75;
}

.tag-input__text {
  border: none;
  outline: none;
  font-size: 0.9em;
  line-height: 50px;
  background: none;
  box-shadow: none;
  min-width: 220px;
}
.tag-input__tag {
  background: #00aeef;
  border: 0;
  font-size: 13px;
  padding: 6px 32px 6px 12px;
  border-radius: 50px;
  color: #fff;
  position: relative;
  line-height: 1.5;
}
.tag-input__tag > span {
  position: absolute;
  right: 5px;
  top: 6px;
  width: 18px;
  height: 18px;
  line-height: 18px;
  border-radius: 50%;
  border: 1px solid #fff;
  opacity: 1;
  text-align: center;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
}
.tag-input__tag > span:hover {
  color: #000;
}

</style>
