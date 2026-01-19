'use client';

import { useEffect, useState } from 'react';
import { TaskList } from '../../components/TaskList';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Button } from '../../components/ui/Button';
import { LogOut, Home } from 'lucide-react';

export default function TasksPage() {
  const router = useRouter();

  const [userEmail, setUserEmail] = useState<string | null>(null);

  useEffect(() => {
    const email = localStorage.getItem('userEmail');
    setUserEmail(email);
  }, []);

  const firstLetter = userEmail ? userEmail.charAt(0).toUpperCase() : 'U';

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <motion.div className="bg-black/20 backdrop-blur-lg border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Button
            onClick={() => router.push('/')}
            variant="ghost"
            className="text-white"
            icon={Home}
          >
            Home
          </Button>

          <h1 className="text-2xl font-bold text-white">📋 My Tasks</h1>

          <div className="flex items-center space-x-4">
            <div
              className="w-10 h-10 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-full flex items-center justify-center"
              title={userEmail ? `Logged in as ${userEmail}` : 'Logged in'}
            >
              <span className="text-white font-bold text-lg">{firstLetter}</span>
            </div>

            <Button
              onClick={handleLogout}
              variant="ghost"
              className="text-white"
            >
              Logout
            </Button>
          </div>
        </div>
      </motion.div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <TaskList />
      </div>
    </div>
  );
}
