import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/login');
  }

  return (
    <nav className="bg-green-700 text-white shadow-md">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold tracking-tight">
          🌾 Krishisetu
        </Link>

        <div className="flex items-center gap-4 text-sm">
          {user ? (
            <>
              <Link to="/dashboard" className="hover:text-green-200 transition-colors">
                Dashboard
              </Link>
              {user.role === 'admin' && (
                <Link to="/admin" className="hover:text-green-200 transition-colors">
                  Admin
                </Link>
              )}
              <span className="text-green-200">Hi, {user.name}</span>
              <button
                onClick={handleLogout}
                className="bg-green-800 px-3 py-1.5 rounded hover:bg-green-900 transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-green-200 transition-colors">
                Login
              </Link>
              <Link
                to="/register"
                className="bg-white text-green-700 px-3 py-1.5 rounded font-medium hover:bg-green-50 transition-colors"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
