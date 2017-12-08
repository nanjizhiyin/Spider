import React, { Component } from 'react';
import logo from './logo.svg';
import $ from 'jquery'
import './App.css';

class App extends Component {
  render() {
    var event = {
      Click: function () {
        console.log("到后台搜索,并将结果显示在界面上")
        $.ajax({
          dataType: "json", 
          url: 'http://127.0.0.1:8890/s?wd=' + $("#wd").val(),
          success: function (data) {
            var tmpHtmp = '';
            for (var i = 0; i < data.length; i++) {
              var item = data[i];
              tmpHtmp += '<div>'
              tmpHtmp += '<a href="' + item['url']+'">' + item['url'] + '</a>'
              tmpHtmp += '<div>' + item['content'] + '</div>'
              tmpHtmp += '</div>'
            }
            $('#itemList').html(tmpHtmp);
          },
          error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
            $('#error').html('出错了');
          } 
        });
      }
    }
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <input id="wd" placeholder="搜索关键字" />
        <button id="searchBt" onClick={event.Click}>搜索</button>
        <div id='itemList'></div>
        <div id="error"></div>

      </div>
    );
  }
}

export default App;
