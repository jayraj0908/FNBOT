import React from 'react';
import Link from 'next/link';
import { useUser } from '../context/UserContext';

const NavBar = () => {
  const { user } = useUser();
  const company = user?.user_metadata?.company || 'Client';

  return (
    <nav className="w-full flex items-center justify-between px-6 py-4 bg-gray-100 border-b">
      <div className="flex items-center gap-4">
        <span className="font-bold text-lg text-blue-700">Trust Bodhi</span>
        <span className="text-gray-600">{company}</span>
      </div>
      <div className="flex items-center gap-4">
        <Link href="/dashboard" className="hover:underline">Dashboard</Link>
        <Link href="/admin" className="hover:underline">Admin</Link>
        <button
          className="ml-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          onClick={async () => {
            const { supabase } = await import('../lib/supabaseClient');
            await supabase.auth.signOut();
            window.location.href = '/auth/login';
          }}
        >
          Logout
        </button>
      </div>
    </nav>
  );
};

export default NavBar; 