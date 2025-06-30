export const toolMap: Record<string, { name: string; route: string; description: string }[]> = {
  BBB: [
    {
      name: 'Data Normalizer Tool',
      route: '/tools/bbb-normalizer',
      description: 'Upload and normalize 60 Bev data for BBB.'
    }
  ],
  Nectar: [
    {
      name: 'Nielsen + VIP Fulfillment Tracker',
      route: '/tools/nectar-dashboard',
      description: 'Track Nielsen and VIP fulfillment for Nectar.'
    }
  ]
}; 