'use client';

import React, { useState } from 'react';
import { Card, CardContent } from './ui/Card';
import { Button } from './ui/Button';
import { Task } from '../lib/types';
import { apiClient } from '../lib/api';
import { CheckCircle, Circle, Edit, Trash2 } from 'lucide-react';

interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

export function TaskItem({ task, onEdit, onDelete }: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  const handleToggleComplete = async () => {
    if (isUpdating) return;

    setIsUpdating(true);
    try {
      const response = await apiClient.put(`/tasks/${task.id}`, {
        completed: !task.completed
      });
      onEdit(response.data);
    } catch (error) {
      console.error('Error updating task:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (isDeleting) return;

    setIsDeleting(true);
    try {
      await apiClient.delete(`/tasks/${task.id}`);
      onDelete(task.id);
    } catch (error) {
      console.error('Error deleting task:', error);
      setIsDeleting(false);
    }
  };

  return (
    <div className={`group relative bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-6 transition-all duration-300 hover:bg-white/15 hover:border-white/30 hover:shadow-2xl hover:shadow-purple-500/10 ${
      task.completed ? 'bg-green-500/10 border-green-500/30' : ''
    }`}>
      {/* Status indicator */}
      <div className={`absolute top-4 right-4 w-3 h-3 rounded-full ${
        task.completed ? 'bg-green-400' : 'bg-yellow-400'
      }`} />

      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0 pr-4">
          <h3 className={`font-semibold text-lg truncate mb-2 ${
            task.completed ? 'line-through text-gray-400' : 'text-white'
          }`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`text-sm leading-relaxed ${
              task.completed ? 'text-gray-500' : 'text-gray-300'
            }`}>
              {task.description}
            </p>
          )}
        </div>

        <div className="flex flex-col items-end space-y-3">
          {/* Complete toggle button */}
          <button
            onClick={handleToggleComplete}
            disabled={isUpdating}
            className={`w-10 h-10 rounded-full flex items-center justify-center transition-all duration-200 ${
              task.completed
                ? 'bg-green-500 hover:bg-green-600 text-white shadow-lg shadow-green-500/30'
                : 'bg-white/20 hover:bg-white/30 text-white border border-white/30 hover:border-white/50'
            } ${isUpdating ? 'opacity-50 cursor-not-allowed' : 'hover:scale-110'}`}
          >
            {task.completed ? (
              <CheckCircle className="w-5 h-5" />
            ) : (
              <Circle className="w-5 h-5" />
            )}
          </button>

          {/* Action buttons */}
          <div className="flex space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            {!task.completed && (
              <button
                onClick={() => onEdit(task)}
                className="p-2 rounded-lg bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 hover:text-blue-300 transition-all duration-200 hover:scale-110"
                title="Edit task ✏️"
              >
                <Edit className="w-4 h-4" />
              </button>
            )}
            <button
              onClick={handleDelete}
              disabled={isDeleting}
              className="p-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 text-red-400 hover:text-red-300 transition-all duration-200 hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
              title="Delete task 🗑️"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Completion badge */}
      {task.completed && (
        <div className="mt-4 flex items-center space-x-2">
          <div className="flex items-center space-x-1 text-green-400 text-sm font-medium">
            <CheckCircle className="w-4 h-4" />
            <span>✅ Completed</span>
          </div>
        </div>
      )}
    </div>
  );
}