'use client';

import { useEffect, useState } from 'react';
import { FaFacebookF, FaTwitter, FaInstagram, FaExternalLinkAlt } from 'react-icons/fa';

// Placeholder for user data
interface UserProfile {
  name: string;
  role: string;
  email: string;
  phone: string;
  recentProject: string;
  mostViewedProject: string;
  // Add other user details here as needed
}

const ProfilePage = () => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // In a real application, you would fetch user data from an API
    // For now, we'll use placeholder data and simulate a fetch
    const fetchUserProfile = async () => {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Placeholder data - replace with actual API call
        const mockUser: UserProfile = {
          name: 'Hacker', // Placeholder name
          role: 'Web Developer', // Placeholder role
          email: 'user@example.com',
          phone: '987-654-3210', // Placeholder phone
          recentProject: 'Todo App', // Placeholder project
          mostViewedProject: 'Portfolio Website', // Placeholder project
        };

        // You might get the user's email from a token or a user info endpoint
        // For demonstration, we're hardcoding it.
        const token = localStorage.getItem('token');
        if (!token) {
          setError('You must be logged in to view this page.');
          setLoading(false);
          return;
        }
        
        // Example of how you might decode a JWT to get user info (client-side)
        // This is for illustration. In a real app, you might have a dedicated API endpoint for user info.
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            mockUser.email = payload.sub; // Assuming 'sub' is the email in the JWT payload
            mockUser.name = payload.sub.split('@')[0]; // Simple name from email
        } catch (e) {
            console.error("Failed to decode token", e);
        }

        setUser(mockUser);
      } catch (err) {
        setError('Failed to fetch user profile.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, []);

  if (loading) {
    return <div className="text-center py-10">Loading profile...</div>;
  }

  if (error) {
    return <div className="text-center py-10 text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto px-6 py-12 pt-[10vh]">
      <div className="modern-card max-w-4xl mx-auto shadow-lg rounded-xl overflow-hidden">
        <div className="flex flex-col md:flex-row">
          {/* Left Column */}
          <div className="w-full md:w-1/3 bg-gray-900/50 p-8 flex flex-col items-center justify-center">
            <div style={{
              width: '6rem', 
              height: '6rem', 
              borderRadius: '50%', 
              border: '4px solid var(--neon-pink)', 
              boxShadow: '0 0 15px var(--neon-pink-glow-strong)',
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              marginBottom: '1rem'
            }}>
              <span style={{
                fontSize: '3.5rem',
                fontWeight: 'bold',
                color: 'var(--neon-pink)',
                textShadow: '0 0 10px var(--neon-pink-glow-medium)'
              }}>{user?.name[0].toUpperCase()}</span>
            </div>
            <h2 className="text-3xl font-light uppercase text-white mb-4 text-center">{user?.name}</h2>

          </div>

          {/* Right Column */}
          <div className="w-full md:w-2/3 p-8">
            <div className="mb-6">
              <h3 className="text-xl font-bold neon-heading mb-4">Information</h3>
              <div className="flex">
                <div className="w-1/2">
                  <strong className="text-gray-300">Email</strong>
                  <p className="text-gray-400">{user?.email}</p>
                </div>

              </div>
            </div>


            

          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
