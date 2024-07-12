import React from 'react';
import './Header.css';

const Header = () => (
  <header>
    <div className="header-container">
      <div className="logo">
        <img src="/logo.png" alt="Mother's Compass Logo" />
        <h1>Mother's Compass</h1>
      </div>
      <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/chat">Group Chat</a>
      </nav>
    </div>
  </header>
);

export default Header;
