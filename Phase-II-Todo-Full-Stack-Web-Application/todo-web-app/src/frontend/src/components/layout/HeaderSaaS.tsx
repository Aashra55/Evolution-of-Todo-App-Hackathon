'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { FiMenu, FiX } from 'react-icons/fi';
import { FaTasks, FaHome, FaChartBar, FaSignInAlt, FaUserPlus, FaUserCircle } from 'react-icons/fa';

const HeaderSaaS = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check for token in localStorage to determine if the user is authenticated
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  return (
    <>
      <header className="header-saas">
        <nav className="container mx-auto px-6 flex justify-between items-center">
          {/* Left: Logo */}
          <div className="flex items-center">
            <Link href="/" passHref>
              <div className="app-logo-saas flex items-center gap-3 cursor-pointer">
                <FaTasks className="icon text-2xl" />
                <span className="text text-xl">TodoApp</span>
              </div>
            </Link>
          </div>

          {/* Center: Desktop Navigation */}
          <div className="desktop-nav items-center gap-8">
            <Link href="/" passHref>
              <div className="nav-link-saas flex items-center gap-3">
                <FaHome className="mr-3 text-neon-pink neon-heading" style={{ marginRight: '10px', filter: 'drop-shadow(0 0 8px var(--neon-pink-glow-medium)) drop-shadow(0 0 15px var(--neon-pink-glow-strong)) drop-shadow(0 0 25px var(--neon-pink-glow-strong))' }} /> <span>Home</span>
              </div>
            </Link>
            <Link href="/dashboard" passHref>
              <div className="nav-link-saas flex items-center gap-3">
                <FaChartBar className="mr-3 text-neon-pink neon-heading" style={{ marginRight: '10px', filter: 'drop-shadow(0 0 8px var(--neon-pink-glow-medium)) drop-shadow(0 0 15px var(--neon-pink-glow-strong)) drop-shadow(0 0 25px var(--neon-pink-glow-strong))' }} /> <span>Dashboard</span>
              </div>
            </Link>
          </div>

          {/* Right: Actions & Mobile Menu Button */}
          <div className="flex items-center gap-4">
            <div className="desktop-actions items-center gap-4">
              {isAuthenticated ? (
                <Link href="/profile" passHref>
                  <div className="btn-primary-saas flex items-center gap-3">
                    <FaUserCircle className="mr-3 text-neon-pink" style={{ marginRight: '10px', filter: 'drop-shadow(0 0 5px var(--neon-pink-glow-medium)) drop-shadow(0 0 10px var(--neon-pink-glow-strong))' }}/> <span>Profile</span>
                  </div>
                </Link>
              ) : (
                <>
                  <Link href="/signin" passHref>
                    <div className="btn-secondary-saas flex items-center gap-3">
                      <FaSignInAlt className="mr-3 text-neon-pink neon-heading" style={{ marginRight: '10px', filter: 'drop-shadow(0 0 5px var(--neon-pink-glow-medium)) drop-shadow(0 0 10px var(--neon-pink-glow-strong))' }}/> <span>Sign In</span>
                    </div>
                  </Link>
                  <Link href="/signup" passHref>
                    <div className="btn-primary-saas flex items-center gap-3">
                      <FaUserPlus className="mr-3 text-neon-pink" style={{ marginRight: '10px', filter: 'drop-shadow(0 0 5px var(--neon-pink-glow-medium)) drop-shadow(0 0 10px var(--neon-pink-glow-strong))' }}/> <span>Sign Up</span>
                    </div>
                  </Link>
                </>
              )}
            </div>
            {/* Hamburger Menu Button */}
            <div className="mobile-menu-toggle">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="hamburger-icon-themed focus:outline-none"
                aria-label="Toggle menu"
              >
                {isMobileMenuOpen ? <FiX size={28} /> : <FiMenu size={28} />}
              </button>
            </div>
          </div>
        </nav>
      </header>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="mobile-menu">
          <nav style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', paddingTop: '2rem' }}>
            <Link href="/" passHref style={{ display: 'block', marginBottom: '1.5rem', textDecoration: 'none' }}>
              <div className="nav-link-saas text-xl flex items-center gap-3" onClick={() => setIsMobileMenuOpen(false)}>
                <FaHome className="mr-3 text-neon-pink" style={{ marginRight: '10px', filter: 'drop-shadow(0 0 8px var(--neon-pink-glow-medium)) drop-shadow(0 0 15px var(--neon-pink-glow-strong)) drop-shadow(0 0 25px var(--neon-pink-glow-strong))' }} /> <span>Home</span>
              </div>
            </Link>
            <Link href="/dashboard" passHref style={{ display: 'block', marginBottom: '1.5rem', textDecoration: 'none' }}>
              <div className="nav-link-saas text-xl flex items-center gap-3" onClick={() => setIsMobileMenuOpen(false)}>
                <FaChartBar className="mr-3 text-neon-pink" style={{ marginRight: '10px', filter: 'drop-shadow(0 0 8px var(--neon-pink-glow-medium)) drop-shadow(0 0 15px var(--neon-pink-glow-strong)) drop-shadow(0 0 25px var(--neon-pink-glow-strong))' }} /> <span>Dashboard</span>
              </div>
            </Link>
            <div className="border-t border-gray-700 w-3/4 my-4"></div>
            {isAuthenticated ? (
              <Link href="/profile" passHref style={{ display: 'block', margin: '1rem 0', textDecoration: 'none' }}>
                <div className="btn-primary-saas flex items-center gap-3" onClick={() => setIsMobileMenuOpen(false)}>
                  <FaUserCircle className="mr-3 text-neon-pink" style={{ filter: 'drop-shadow(0 0 5px var(--neon-pink-glow-medium)) drop-shadow(0 0 10px var(--neon-pink-glow-strong))' }} /> <span>Profile</span>
                </div>
              </Link>
            ) : (
              <>
                <Link href="/signin" passHref style={{ display: 'block', margin: '1rem 0', textDecoration: 'none' }}>
                  <div className="btn-secondary-saas flex items-center gap-3" onClick={() => setIsMobileMenuOpen(false)}>
                    <FaSignInAlt className="mr-3 text-neon-pink" style={{ filter: 'drop-shadow(0 0 5px var(--neon-pink-glow-medium)) drop-shadow(0 0 10px var(--neon-pink-glow-strong))' }} /> <span>Sign In</span>
                  </div>
                </Link>
                <Link href="/signup" passHref style={{ display: 'block', margin: '1rem 0', textDecoration: 'none' }}>
                  <div className="btn-primary-saas flex items-center gap-3" onClick={() => setIsMobileMenuOpen(false)}>
                    <FaUserPlus className="mr-3 text-neon-pink" style={{ filter: 'drop-shadow(0 0 5px var(--neon-pink-glow-medium)) drop-shadow(0 0 10px var(--neon-pink-glow-strong))' }} /> <span>Sign Up</span>
                  </div>
                </Link>
              </>
            )}
          </nav>
        </div>
      )}
    </>
  );
};

export default HeaderSaaS;
