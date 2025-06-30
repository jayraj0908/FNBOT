import { useState } from 'react';
import { useRouter } from 'next/router';

export default function ClientLogin() {
  const [organization, setOrganization] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!organization || !email) {
      setError('Please enter both organization and email.');
      return;
    }
    // Simulate org/email validation (replace with Supabase check later)
    router.push(`/login?org=${encodeURIComponent(organization)}&email=${encodeURIComponent(email)}`);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow p-8">
        <h2 className="text-2xl font-bold mb-6 text-center">Client Login</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Organization"
            value={organization}
            onChange={e => setOrganization(e.target.value)}
            className="border rounded px-4 py-2"
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            className="border rounded px-4 py-2"
          />
          {error && <div className="text-red-500 text-sm">{error}</div>}
          <button type="submit" className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">Continue</button>
        </form>
      </div>
    </div>
  );
} 