import React from 'react'
import { NavLink } from 'react-router-dom'

export const Navbar: React.FC = () => (
  <nav>
    <div className="nav-wrapper cyan darken-1 px1">
      <NavLink to="/" className="brand-logo"></NavLink>
      <ul className="right hide-on-med-and-down">
        <li cy-data="home-nav-link"></li>
        <li></li>
      </ul>
    </div>
  </nav>
)
