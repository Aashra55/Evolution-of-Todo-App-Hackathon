'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { signin } from '@/services/api';
import { FaSignInAlt } from 'react-icons/fa'; // Import the icon

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const data = await signin(email, password);
      localStorage.setItem('token', data.access_token);
      router.push('/dashboard');
    } catch (err) {
      setError('Signin failed. Please check your credentials.');
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full modern-card"> {/* Applied modern-card class, removed space-y-8 from here */}
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold neon-heading">
            Sign in to your account
          </h2>
        </div>
        <form className="mt-8 px-8" onSubmit={handleSubmit}> {/* Increased horizontal padding */}
          {error && <p className="text-red-500 text-center">{error}</p>}
          <div style={{ marginBottom: '1.5rem' }}> {/* Email input div with inline margin */}
            <div>
              <label htmlFor="email-address" className="sr-only">
                Email address
              </label>
              <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="input-field-modern" /* Removed w-full */
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={{ width: 'calc(100% - 3.6%)', margin: '0 auto' }} /* Explicitly set width and center */
              />
            </div>
          </div>
          <div style={{ marginBottom: '1.5rem' }}> {/* Password input div with inline margin */}
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="input-field-modern" /* Removed w-full */
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ width: 'calc(100% - 3.6%)', margin: '0 auto' }} /* Explicitly set width and center */
              />
            </div>
          </div>

          <div style={{ marginTop: '1.5rem' }} className="flex justify-center"> {/* Button div with inline margin and flex centering */}
            <button
              type="submit"
              className="neon-button"
            >
              <FaSignInAlt className="mr-2" /> Sign in
            </button>
          </div>
          <div className="text-sm text-center mt-6 pt-0">
            <p className="text-gray-400">
              Don't have an account?{' '}
              <Link href="/signup" className="font-medium text-neon-pink hover:text-neon-pink-light">
                Sign up
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}