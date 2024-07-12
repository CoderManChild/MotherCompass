import React from 'react';
import Header from './components/Header';
import ChatContainer from './components/ChatContainer';
import Sidebar from './components/Sidebar';
import './App.css';

const App = () => {
  return (
    <div className="App">
      <Header />
      <div className="container">
        <ChatContainer />
        <Sidebar />
      </div>
    </div>
  );
};

export default App;
