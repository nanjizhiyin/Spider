<template>
  <div id="example-3">
    <h1>{{ msg }}</h1>
    <input id="wd" class="wd" ref="wd" placeholder="搜索关键字"/>
    <button id="searchBt" class="searchBt" v-on:click="greet">搜索</button>
    <!-- 循环显示返回的数据 -->
    <div class='itemList'>
      <div class="item" v-for = "item in itemList" :key="item.id">
        <a class="url" :href="item.url"> {{ item.url }} </a>
        <div v-if="item.content.length==0">没有抓取到网页数据</div>
        <div v-else class="content">{{ item.content}}</div>
      </div>
    </div>
    <!-- 返回错误时显示 -->
    <div class="error">{{error}}</div>
  </div>
</template>

<script>
import Vue from 'vue'
import VueResource from 'vue-resource'
Vue.use(VueResource)

export default {
  name: 'Search',
  data () {
    return {
      msg: '请输入搜索的内容',
      itemList: [
        { url: 'https://www.baidu.com/', content: '百度' },
        { url: 'Fhttps://www.baidu.com/o', content: '百度1' }
      ],
      error: '没有发现错误'
    }
  },
  methods: {
    // 绑定点击事件
    greet: function (event) {
      this.$http.get('http://127.0.0.1:8890/s?wd=' + this.$refs.wd.value).then(response => {
        // 返回数据赋值给变量
        this.itemList = response.body
      }, response => {
        // error callback
        this.error = response.body
      })
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
/* 搜索结果样式 */
.itemList{ margin-left: 10px; margin-top: 20px}
.item{margin-top: 20px} 
.url{color: blue; margin-top: 20px} 
.content{margin-top: 20px} 
</style>