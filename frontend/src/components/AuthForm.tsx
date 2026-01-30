'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Input } from './ui/Input';
import { Button } from './ui/Button';
import { apiClient } from '../lib/api';
import { useToast } from './ui/Toast';

interface AuthFormProps {
  mode: 'signin' | 'signup';
}

export function AuthForm({ mode }: AuthFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const router = useRouter();
  const isSignup = mode === 'signup';
  const { addToast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isSignup) {
        console.log('Attempting signup for email:', email);
        if (password !== confirmPassword) {
          console.log('Signup failed: passwords do not match');
          addToast('Passwords do not match', 'error');
          setLoading(false);
          return;
        }

        // Call signup API
        console.log('Calling signup API');
        const signupResponse = await apiClient.post('/auth/signup', { email, password });
        console.log('Signup API response:', signupResponse);
        addToast('Account created successfully!', 'success');

        // Auto-login after successful signup
        console.log('Auto-logging in after signup');
        const signinResponse = await apiClient.post('/auth/signin', { email, password });
        const { access_token, user } = signinResponse.data;

        // Store token, user email, and user ID in localStorage
        localStorage.setItem('token', access_token);
        localStorage.setItem('userEmail', email);
        if (user && user.id) {
          localStorage.setItem('userId', user.id);
        }
        console.log('Auto-login successful, token stored');
      } else {
        // Call signin API
        console.log('Calling signin API');
        const response = await apiClient.post('/auth/signin', { email, password });
        const { access_token, user } = response.data;

        // Store token, user email, and user ID in localStorage
        localStorage.setItem('token', access_token);
        localStorage.setItem('userEmail', email);
        if (user && user.id) {
          localStorage.setItem('userId', user.id);
        }
        addToast('Signed in successfully!', 'success');
      }

      // Redirect to tasks page after successful auth
      router.push('/tasks');
      router.refresh();
    } catch (err: any) {
      console.error('Auth error:', err);
      console.log('Error details:', err.response?.data, err.response?.status);

      // Better error handling with more specific messages
      let errorMessage = 'An error occurred during authentication';
      
      if (err.code === 'ECONNREFUSED' || err.message?.includes('Network Error')) {
        errorMessage = 'Cannot connect to the server. Please make sure the backend is running and accessible.';
      } else if (err.response?.status === 401) {
        errorMessage = err.response?.data?.detail || 'Invalid email or password';
      } else if (err.response?.status === 400) {
        errorMessage = err.response?.data?.detail || 'Invalid request. Please check your input';
      } else if (err.response?.status === 409) {
        errorMessage = err.response?.data?.detail || 'User already exists';
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      addToast(errorMessage, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-foreground mb-1">
          Email
        </label>
        <Input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full"
          placeholder="your@email.com"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-foreground mb-1">
          Password
        </label>
        <Input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full"
          placeholder="••••••••"
        />
      </div>

      {isSignup && (
        <div>
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-foreground mb-1">
            Confirm Password
          </label>
          <Input
            id="confirmPassword"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            className="w-full"
            placeholder="••••••••"
          />
        </div>
      )}

      <Button type="submit" disabled={loading} className="w-full">
        {loading ? 'Processing...' : isSignup ? 'Sign Up' : 'Sign In'}
      </Button>

      <div className="text-center text-sm text-muted-foreground mt-4">
        {isSignup ? (
          <span>
            Already have an account?{' '}
            <a href="/signin" className="text-primary hover:underline">
              Sign In
            </a>
          </span>
        ) : (
          <span>
            Don't have an account?{' '}
            <a href="/signup" className="text-primary hover:underline">
              Sign Up
            </a>
          </span>
        )}
      </div>
    </form>
  );
}