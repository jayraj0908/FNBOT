import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { supabase } from '../src/lib/supabaseClient';

export default function Login() {
  const router = useRouter();
  const { org, email: queryEmail } = router.query;
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (typeof queryEmail === 'string') setEmail(queryEmail);
  }, [queryEmail]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    const { error, data } = await supabase.auth.signInWithPassword({ email, password });
    setLoading(false);
    if (error) {
      setError(error.message);
    } else {
      // Use org from query or user_metadata
      const organization = org || data.user?.user_metadata?.organization;
      router.push('/dashboard' + (organization ? `?org=${encodeURIComponent(organization)}` : ''));
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow p-8">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            className="border rounded px-4 py-2"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="border rounded px-4 py-2"
          />
          {error && <div className="text-red-500 text-sm">{error}</div>}
          <button type="submit" className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition" disabled={loading}>{loading ? 'Logging in...' : 'Login'}</button>
        </form>
      </div>
    </div>
  );
} 