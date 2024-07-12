import React from 'react';
import './HamburgerMenu.css';

const HamburgerMenu = () => {
  const toggleSidebar = () => {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
  };

  return (
    <div className="hamburger-menu" id="hamburger-menu" onClick={toggleSidebar}>
      <span></span>
      <span></span>
      <span></span>
    </div>
  );
};

export default HamburgerMenu;
