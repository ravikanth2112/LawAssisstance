// Sample data for the dashboard
export const clients = [
  {
    id: 1,
    name: 'Sarah Johnson',
    email: 'sarah.johnson@email.com',
    phone: '+1 (555) 123-4567',
    caseType: 'OPT Application',
    status: 'Active',
    priority: 'Medium',
    lastUpdate: '2025-08-22'
  },
  {
    id: 2,
    name: 'Michael Chen',
    email: 'michael.chen@email.com',
    phone: '+1 (555) 234-5678',
    caseType: 'H1B Visa',
    status: 'Pending',
    priority: 'High',
    lastUpdate: '2025-08-21'
  },
  {
    id: 3,
    name: 'Elena Rodriguez',
    email: 'elena.rodriguez@email.com',
    phone: '+1 (555) 345-6789',
    caseType: 'STEM Extension',
    status: 'Active',
    priority: 'Urgent',
    lastUpdate: '2025-08-24'
  },
  {
    id: 4,
    name: 'Anna Kowalski',
    email: 'anna.kowalski@email.com',
    phone: '+1 (555) 456-7890',
    caseType: 'H1B Filing',
    status: 'Active',
    priority: 'High',
    lastUpdate: '2025-08-23'
  }
];

export const deadlines = [
  {
    id: 1,
    clientName: 'Elena Rodriguez',
    caseType: 'STEM Application Deadline',
    dueDate: '2025-08-30',
    priority: 'urgent',
    status: 'pending'
  },
  {
    id: 2,
    clientName: 'Anna Kowalski',
    caseType: 'H1B Filing Deadline',
    dueDate: '2025-09-08',
    priority: 'high',
    status: 'pending'
  },
  {
    id: 3,
    clientName: 'Sarah Johnson',
    caseType: 'OPT Report Due',
    dueDate: '2025-09-15',
    priority: 'medium',
    status: 'pending'
  },
  {
    id: 4,
    clientName: 'Michael Chen',
    caseType: 'H1B Interview Preparation',
    dueDate: '2025-09-20',
    priority: 'medium',
    status: 'pending'
  }
];

export const recentActivities = [
  {
    id: 1,
    type: 'approved',
    title: "Sarah Johnson's OPT application approved",
    subtitle: 'Application processed successfully',
    time: '2 hours ago',
    status: 'success'
  },
  {
    id: 2,
    type: 'payment',
    title: 'Payment received: Michael Chen ($4,500)',
    subtitle: 'H1B visa processing fee',
    time: '4 hours ago',
    status: 'success'
  },
  {
    id: 3,
    type: 'new',
    title: 'New client onboarded: Elena Rodriguez',
    subtitle: 'STEM extension case',
    time: '1 day ago',
    status: 'info'
  },
  {
    id: 4,
    type: 'document',
    title: 'Documents uploaded: Anna Kowalski',
    subtitle: 'H1B supporting documents',
    time: '2 days ago',
    status: 'info'
  }
];

export const stats = {
  totalClients: {
    value: 247,
    active: 156,
    pending: 91,
    change: '+5% from last month'
  },
  deadlinesThisWeek: {
    value: 23,
    urgent: 5,
    normal: 18,
    change: '+2 from last week'
  },
  monthlyRevenue: {
    value: 48200,
    change: '+12% from last month',
    trend: 'up'
  },
  pendingPayments: {
    value: 12700,
    overdue: 3,
    change: '-8% from last month'
  }
};
