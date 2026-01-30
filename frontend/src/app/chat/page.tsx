'use client';

import { useEffect, useState } from 'react';
import ChatInterface from '../../components/ChatInterface';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Button } from '../../components/ui/Button';
import { LogOut, Home, MessageSquare } from 'lucide-react';

export default function ChatPage() {
  const router = useRouter();

  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    const email = localStorage.getItem('userEmail');
    const storedUserId = localStorage.getItem('userId');
    setUserEmail(email);
    setUserId(storedUserId);
  }, []);

  const firstLetter = userEmail ? userEmail.charAt(0).toUpperCase() : 'U';

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userId');
    router.push('/');
  };

  // Show an error if user is not logged in
  if (!userId) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="bg-black/20 backdrop-blur-lg border border-white/10 rounded-xl p-8 max-w-md w-full mx-4 text-center">
          <h2 className="text-2xl font-bold text-white mb-4">🔒 Access Denied</h2>
          <p className="text-gray-300 mb-6">
            Please log in to access the AI Chat Assistant.
          </p>
          <Button
            onClick={() => router.push('/signin')}
            className="bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-600 hover:to-purple-700 text-white"
          >
            Go to Login
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col">
      {/* Header */}
      <motion.header
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="bg-black/20 backdrop-blur-lg border-b border-white/10 py-4"
      >
        <div className="max-w-7xl mx-auto px-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <Button
              onClick={() => router.push('/')}
              variant="ghost"
              className="text-white hover:bg-white/10 transition-colors"
              icon={Home}
            >
              Home
            </Button>
            <Button
              onClick={() => router.push('/tasks/')}
              variant="ghost"
              className="text-white hover:bg-white/10 transition-colors"
              icon={MessageSquare}
            >
              Tasks
            </Button>
          </div>

          <h1 className="text-2xl font-bold text-white flex items-center">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
              className="mr-3"
            >
              <MessageSquare className="text-cyan-400" />
            </motion.div>
            AI Todo Assistant
          </h1>

          <div className="flex items-center space-x-4">
            <div
              className="w-10 h-10 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-full flex items-center justify-center transition-transform hover:scale-110"
              title={userEmail ? `Logged in as ${userEmail}` : 'Logged in'}
            >
              <span className="text-white font-bold text-lg">{firstLetter}</span>
            </div>

            <Button
              onClick={handleLogout}
              variant="ghost"
              className="text-white hover:bg-white/10 transition-colors"
            >
              Logout
            </Button>
          </div>
        </div>
      </motion.header>

      {/* Main Content with Sidebar Layout */}
      <div className="flex flex-1 overflow-hidden max-w-7xl mx-auto w-full px-4 py-4">
        {/* Left Sidebar - Chat Interface */}
        <motion.aside
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="w-full md:w-1/2 lg:w-2/5 xl:w-1/3 flex flex-col mr-0 md:mr-4 mb-4 md:mb-0"
        >
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 shadow-2xl h-full flex flex-col overflow-hidden">
            <div className="p-4 border-b border-white/10">
              <h2 className="text-lg font-semibold text-white flex items-center">
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.4, type: "spring", stiffness: 300 }}
                  className="mr-2"
                >
                  💬
                </motion.span>
                Your AI Assistant
              </h2>
              <p className="text-sm text-gray-300 mt-1">
                Manage tasks with natural language
              </p>
            </div>
            <div className="flex-1 overflow-hidden p-4">
              <ChatInterface userId={userId} />
            </div>
          </div>
        </motion.aside>

        {/* Right Side - Task Preview or Information */}
        <motion.section
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="hidden md:block w-1/2 lg:w-3/5 xl:w-2/3"
        >
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 shadow-2xl h-full p-6">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center">
              <motion.div
                initial={{ rotate: -90 }}
                animate={{ rotate: 0 }}
                transition={{ delay: 0.6, duration: 0.4 }}
                className="mr-3"
              >
                📋
              </motion.div>
              Your Tasks Overview
            </h2>
            <div className="space-y-4">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7, duration: 0.4 }}
                className="bg-white/5 rounded-xl p-4 border border-white/10"
              >
                <h3 className="font-medium text-cyan-300">Interactive Assistant</h3>
                <p className="text-gray-300 text-sm mt-1">
                  Communicate with your AI assistant using natural language.
                  Try commands like "Add a task to buy groceries" or "Show me my tasks".
                </p>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8, duration: 0.4 }}
                className="bg-white/5 rounded-xl p-4 border border-white/10"
              >
                <h3 className="font-medium text-purple-300">Smart Task Management</h3>
                <p className="text-gray-300 text-sm mt-1">
                  The AI understands context and can manage your tasks efficiently.
                  It remembers previous conversations and maintains task state.
                </p>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.9, duration: 0.4 }}
                className="bg-white/5 rounded-xl p-4 border border-white/10"
              >
                <h3 className="font-medium text-green-300">Natural Language Processing</h3>
                <p className="text-gray-300 text-sm mt-1">
                  Simply tell the assistant what you want to do. It will parse your
                  requests and perform the appropriate task operations automatically.
                </p>
              </motion.div>
            </div>
          </div>
        </motion.section>
      </div>
    </div>
  );
}