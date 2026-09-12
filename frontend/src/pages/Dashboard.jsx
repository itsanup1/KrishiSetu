import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">
          Welcome, {user.name}!
        </h1>
        <p className="text-gray-600 mt-1">
          <span className="capitalize font-medium">{user.role}</span>
          {user.location && <span> · {user.location}</span>}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {user.role === 'farmer' && (
          <>
            <DashboardCard
              title="Marketplace"
              description="Browse and purchase seeds, fertilizers, pesticides, and other agricultural inputs from verified vendors."
            />
            <DashboardCard
              title="Equipment Rental"
              description="Rent tractors, harvesters, and other farming equipment from equipment owners near you."
            />
          </>
        )}
        {user.role === 'vendor' && (
          <DashboardCard
            title="My Products"
            description="Manage your product listings, track inventory, and view incoming orders."
          />
        )}
        {user.role === 'admin' && (
          <DashboardCard
            title="Admin Panel"
            description="Manage users, review listings, and monitor platform activity."
            link="/admin"
          />
        )}
      </div>

      <p className="text-sm text-gray-400 mt-10">
        More features coming soon.
      </p>
    </div>
  );
}

function DashboardCard({ title, description }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
      <h3 className="text-lg font-semibold text-green-700 mb-2">{title}</h3>
      <p className="text-gray-600 text-sm leading-relaxed">{description}</p>
      <span className="inline-block mt-4 text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">
        Coming soon
      </span>
    </div>
  );
}
