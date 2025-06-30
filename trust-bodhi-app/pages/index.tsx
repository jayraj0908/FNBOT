import LandingNav from '../components/LandingNav';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <LandingNav />
      <main className="flex flex-1 flex-col items-center justify-center text-center px-4">
        <h1 className="text-4xl md:text-5xl font-bold mb-6">Welcome to Trust Bodhi – CPG Intelligence, Simplified</h1>
        <p className="mb-8 text-lg text-gray-700 max-w-xl">A multi-tenant SaaS platform for client-specific data tools and analytics.</p>
        <a href="/client-login" className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold shadow hover:bg-blue-700 transition">Client Login</a>
      </main>
    </div>
  );
} 