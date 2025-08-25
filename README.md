<<<<<<< HEAD
# Immigration Law Dashboard

A comprehensive React.js dashboard for immigration law practice management.

## Features

- **Dashboard Overview**: Real-time statistics and key metrics
- **Client Management**: Track and manage client information
- **Deadline Tracking**: Monitor important case deadlines
- **Document Management**: Organize case documents
- **Billing & Invoices**: Handle billing and payment tracking
- **Analytics**: Practice performance insights
- **Firm Branding**: Customize firm appearance

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Sidebar.js      # Navigation sidebar
│   ├── DashboardStats.js   # Statistics cards
│   ├── RecentActivity.js   # Activity feed
│   └── UpcomingDeadlines.js # Deadline tracker
├── pages/              # Main page components
│   ├── Dashboard.js    # Main dashboard
│   ├── Clients.js      # Client management
│   ├── Documents.js    # Document management
│   ├── Deadlines.js    # Deadline management
│   ├── Billing.js      # Billing & invoices
│   ├── Analytics.js    # Analytics & reports
│   └── FirmBranding.js # Firm customization
├── data/               # Sample data and API calls
│   └── sampleData.js   # Mock data
├── styles/             # CSS stylesheets
│   └── App.css         # Main styles
├── App.js              # Main app component
└── index.js            # Entry point
```

## Key Modules

### 1. App.js
Main application component with routing setup using React Router.

### 2. Sidebar.js
Navigation component with:
- Logo and branding
- Navigation menu items
- User role tabs (Lawyer/Client)
- AI Assistant integration

### 3. Dashboard.js
Main dashboard page featuring:
- Header with notifications and settings
- Statistics overview cards
- Recent activity feed
- Upcoming deadlines

### 4. DashboardStats.js
Statistics cards showing:
- Total clients (active/pending)
- Weekly deadlines
- Monthly revenue
- Pending payments

### 5. RecentActivity.js
Activity feed displaying:
- Application approvals
- Payment notifications
- New client onboarding
- Document uploads

### 6. UpcomingDeadlines.js
Deadline tracker with:
- Client names and case types
- Due dates
- Priority levels (urgent, high, medium)

## Getting Started

1. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

2. Start the development server:
   \`\`\`bash
   npm start
   \`\`\`

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Available Scripts

- \`npm start\` - Runs the app in development mode
- \`npm build\` - Builds the app for production
- \`npm test\` - Launches the test runner
- \`npm eject\` - Ejects from Create React App (one-way operation)

## Dependencies

- React 18.2.0
- React Router DOM 6.3.0
- Lucide React (for icons)
- Create React App

## Customization

The dashboard is designed to be easily customizable:

1. **Colors & Themes**: Modify CSS variables in `App.css`
2. **Components**: Add new components in the `components/` directory
3. **Pages**: Create new pages in the `pages/` directory
4. **Data**: Update sample data in `data/sampleData.js`
5. **Navigation**: Modify sidebar menu in `Sidebar.js`

## Future Enhancements

- Database integration
- Real-time notifications
- Advanced analytics
- Document upload functionality
- Calendar integration
- Email automation
- Client portal
- Mobile responsiveness
- Multi-language support

## License

This project is licensed under the MIT License.
=======
# LawAssisstance
>>>>>>> d5f7e98fb9b48170fe7fba97c93317b819290df2
