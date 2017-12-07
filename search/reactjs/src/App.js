import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
  
        <input id="wd" class="wd" ref="wd" placeholder="搜索关键字" />
        <button id="searchBt" class="searchBt">搜索</button>
        <div class='itemList'>
          <div class="item" v-for="item in itemList">
            <a class="url"> "url" </a>
            <div class="content">"content"</div>
          </div>
        </div>
        <div class="error">"error"</div>

      </div>
    );
  }
}

export default App;
