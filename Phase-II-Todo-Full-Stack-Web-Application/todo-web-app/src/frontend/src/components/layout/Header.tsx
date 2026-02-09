'use client';

import Link from 'next/link';
import { FaTasks, FaHome, FaChartBar, FaSignInAlt, FaUserPlus } from 'react-icons/fa';

const Header = () => {
  return (
    <header className="header-modern sticky top-0 z-50">
      <nav className="container mx-auto px-6 py-3 flex justify-between items-center">
        <div className="flex items-center">
          <Link href="/" passHref>
            <div className="flex items-center gap-3 cursor-pointer">
              <FaTasks className="text-3xl text-neon-pink" />
              <span className="text-2xl font-bold app-title">TodoApp</span>
            </div>
          </Link>
        </div>
        <div className="hidden md:flex items-center gap-8">
          <Link href="/" passHref>
            <div className="nav-link flex items-center gap-2">
              <FaHome /> <span>Home</span>
            </div>
          </Link>
          <Link href="/dashboard" passHref>
            <div className="nav-link flex items-center gap-2">
              <FaChartBar /> <span>Dashboard</span>
            </div>
          </Link>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/signin" passHref>
            <div className="btn-secondary flex items-center gap-2">
              <FaSignInAlt /> <span>Sign In</span>
            </div>
          </Link>
          <Link href="/signup" passHref>
            <div className="btn-primary flex items-center gap-2">
              <FaUserPlus /> <span>Sign Up</span>
            </div>
          </Link>
        </div>
      </nav>
    </header>
  );
};

export default Header;
