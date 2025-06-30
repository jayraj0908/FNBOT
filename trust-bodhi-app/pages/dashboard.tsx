import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

const toolMap: Record<string, { name: string; description: string; route: string }[]> = {
  bbb: [
    { name: 'Data Normalizer', description: 'Upload and normalize 60 Bev data for BBB.', route: '/tools/bbb-normalizer' }
  ],
  nectar: [
    { name: 'Fulfillment Tracker', description: 'Track Nielsen and VIP fulfillment for Nectar.', route: '/tools/nectar-dashboard' }
  ]
};

export default function Dashboard() {
  const router = useRouter();
  const { org } = router.query;
  const [organization, setOrganization] = useState('');
  const [tools, setTools] = useState<typeof toolMap['bbb']>([]);

  useEffect(() => {
    if (typeof org === 'string') {
      setOrganization(org.toLowerCase());
      setTools(toolMap[org.toLowerCase()] || []);
    }
  }, [org]);

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-50 px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl">
        {tools.length === 0 && <div className="text-gray-500">No tools available for this organization.</div>}
        {tools.map(tool => (
          <a key={tool.route} href={tool.route} className="block bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
            <h2 className="text-xl font-semibold mb-2">{tool.name}</h2>
            <p className="text-gray-700 mb-2">{tool.description}</p>
            <span className="text-blue-600 font-medium">Open Tool →</span>
          </a>
        ))}
      </div>
    </div>
  );
} 