import React from 'react'
import './navbar.css'

const Navbar = () => {
  return (
    <div className = "navbar">
      <div className='navbar-container'>
        <div className="navbar-logo"> 
          <a href=""> Writify </a>
        </div>
        <div className = "navbar-links">
          <div className="navbar-links_container">
            <a href="info">How it works</a>
            <a href="#About">About</a>
          </div>
        </div> 
      </div>
    </div>
  )
}

export default Navbar