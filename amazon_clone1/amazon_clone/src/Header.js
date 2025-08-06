import React from 'react';
import './Header.css';

function Header() {
  return (
    <div className='header'>
      <img 
        className='header_logo' 
        src="https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg" 
        alt="Amazon Logo" 
      />

      <div className='header_search'>
        <input className='header_searchInput' type='text' />
        {/* You can add a search icon here */} 
        
      </div>

      <div className='header_nav'>

        <div className='header_option'>
          <span className='header_optionLine1'>Hello, Varad</span>
          <span className='header_optionLine2'>Sign In</span>
        </div>

        <div className='header_option'>
          <span className='header_optionLine1'>Returns</span>
          <span className='header_optionLine2'>& Orders</span>
        </div>

        <div className='header_option'>
          <span className='header_optionLine1'>Your</span>
          <span className='header_optionLine2'>Prime</span>
        </div>

      </div>
    </div>
  );
}

export default Header;
