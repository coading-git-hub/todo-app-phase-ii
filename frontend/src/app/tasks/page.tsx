'use client';

import { TaskList } from '../../components/TaskList';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Button } from '../../components/ui/Button';
import { LogOut, Home, User } from 'lucide-react';

export default function TasksPage() {
  const router = useRouter();

  // Get user email from localStorage
  const userEmail = typeof window !== 'undefined' ? localStorage.getItem('userEmail') : null;
  const firstLetter = userEmail ? userEmail.charAt(0).toUpperCase() : 'U';

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-black/20 backdrop-blur-lg border-b border-white/10"
      >
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex items-center space-x-4"
            >
              <Button
                onClick={() => router.push('/')}
                variant="ghost"
                className="text-white hover:bg-black/20 hover:text-cyan-300"
                icon={Home}
              >
                Home
              </Button>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="text-2xl md:text-3xl font-bold text-white"
            >
              📋 <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">My Tasks</span>
            </motion.h1>

            <div className="flex items-center space-x-4">
              {/* User Avatar */}
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.4 }}
                className="w-10 h-10 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-full flex items-center justify-center shadow-lg cursor-pointer hover:scale-110 transition-transform duration-200"
                title={`Logged in as ${userEmail || 'User'}`}
              >
                <span className="text-white font-bold text-lg">{firstLetter}</span>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.5 }}
              >
                <Button
                  onClick={handleLogout}
                  variant="ghost"
                  className="text-white hover:bg-red-500/20 hover:text-red-400"
                  icon={LogOut}
                >
                  Logout
                </Button>
              </motion.div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.5 }}
        className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8"
      >
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.7 }}
          className="bg-white/5 backdrop-blur-lg rounded-3xl border border-white/10 p-8 shadow-2xl"
        >
          <TaskList />
        </motion.div>
      </motion.div>
    </div>
  );
}