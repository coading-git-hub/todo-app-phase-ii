'use client';

import React, { useState } from 'react';
import { Input } from './ui/Input';
import { Button } from './ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Task } from '../lib/types';
import { apiClient } from '../lib/api';
import { useToast } from './ui/Toast';

interface TaskFormProps {
  task?: Task | null;
  onTaskCreated: (task: Task) => void;
  onTaskUpdated: (task: Task) => void;
  onCancel: () => void;
}

export function TaskForm({ task, onTaskCreated, onTaskUpdated, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [completed, setCompleted] = useState(task?.completed || false);
  const [loading, setLoading] = useState(false);

  const isEditing = !!task;
  const { addToast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      addToast('Title is required', 'error');
      return;
    }

    setLoading(true);

    try {
      if (isEditing && task) {
        // Update existing task
        const response = await apiClient.put(`/tasks/${task.id}`, {
          title,
          description,
          completed
        });
        onTaskUpdated(response.data);
        addToast('Task updated successfully!', 'success');
      } else {
        // Create new task
        const response = await apiClient.post('/tasks/', {
          title,
          description,
          completed
        });
        onTaskCreated(response.data);
        addToast('Task created successfully!', 'success');
      }
    } catch (err: any) {
      console.error('Error saving task:', err);
      const errorMessage = err.response?.data?.detail || 'An error occurred while saving the task';
      addToast(errorMessage, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="mb-6 animate-fade-in">
      <CardHeader>
        <CardTitle>{isEditing ? 'Edit Task' : 'Create New Task'}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-foreground mb-1">
              Title *
            </label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Task title"
              maxLength={200}
              required
            />
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-foreground mb-1">
              Description
            </label>
            <Input
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Task description (optional)"
              maxLength={2000}
            />
          </div>

          {/* Completion status checkbox */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="completed"
              checked={completed}
              onChange={(e) => setCompleted(e.target.checked)}
              className="h-4 w-4 text-primary rounded border-input focus:ring-ring"
            />
            <label htmlFor="completed" className="ml-2 block text-sm text-foreground">
              Mark as completed
            </label>
          </div>

          <div className="flex justify-end space-x-2">
            <Button type="button" variant="outline" onClick={onCancel} disabled={loading}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? (isEditing ? 'Updating...' : 'Creating...') : (isEditing ? 'Update Task' : 'Create Task')}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}