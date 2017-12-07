<template>
  <div id="example-3">
    <h1>{{ msg }}</h1>
    <input id="wd" class="wd"/>
    <button id="searchBt" class="searchBt">搜索</button>
  </div>
</template>

<script src="./Search.js"></script>
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
