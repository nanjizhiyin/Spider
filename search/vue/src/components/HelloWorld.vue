<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <input id="wd" class="wd"/>
    <button id="searchBt" class="searchBt">搜索</button>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: '请输入搜索的内容'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
.wd {
  height: 40px;
  width: 400px;
}
.searchBt{
  height: 40px;
  width: 40px;
}
</style>
