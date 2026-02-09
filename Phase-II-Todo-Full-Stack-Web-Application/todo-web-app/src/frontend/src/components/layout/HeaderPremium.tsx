'use client';

import Link from 'next/link';
import { FaTasks } from 'react-icons/fa';

const HeaderPremium = () => {
  return (
    <header className="header-premium sticky top-0 z-50">
      <nav className="container mx-auto px-6 flex justify-between items-center">
        {/* Left: Logo */}
        <div className="flex items-center">
          <Link href="/" passHref>
            <div className="app-logo-premium flex items-center gap-3 cursor-pointer">
              <FaTasks className="icon text-3xl" />
              <span className="text text-2xl">TodoApp</span>
            </div>
          </Link>
        </div>

        {/* Center: Navigation */}
        <div className="hidden md:flex items-center gap-10">
          <Link href="/" passHref>
            <span className="nav-link-premium">Home</span>
          </Link>
          <Link href="/dashboard" passHref>
            <span className="nav-link-premium">Dashboard</span>
          </Link>
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-2">
          <Link href="/signin" passHref>
            <span className="btn-secondary-premium">Sign In</span>
          </Link>
          <Link href="/signup" passHref>
            <span className="btn-primary-premium">Sign Up</span>
          </Link>
        </div>
      </nav>
    </header>
  );
};

export default HeaderPremium;
