import Link from 'next/link';

export default function LandingNav() {
  return (
    <nav className="w-full flex items-center justify-between px-8 py-4 bg-white border-b shadow-sm">
      <div className="font-bold text-xl text-blue-700">Trust Bodhi</div>
      <div className="flex gap-6">
        <Link href="/" className="hover:underline">Home</Link>
        <Link href="#about" className="hover:underline">About</Link>
        <Link href="/client-login" className="hover:underline">Login</Link>
      </div>
    </nav>
  );
} 