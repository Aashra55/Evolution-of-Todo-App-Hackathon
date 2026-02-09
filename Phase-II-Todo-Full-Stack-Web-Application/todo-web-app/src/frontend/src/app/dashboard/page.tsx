'use client';

import { useRouter } from 'next/navigation';

import { useEffect, useState } from 'react';
import { logout, fetchTasks, createTask, updateTask, deleteTask, isAuthenticated } from '@/services/api';
import TaskList from '@/components/tasks/TaskList';
import TaskForm from '@/components/tasks/TaskForm';
import { FaSignOutAlt } from 'react-icons/fa'; // Import the icon

interface Task {
  id: number;
  description: string;
  completed: boolean;
  owner_id: number;
}

export default function Dashboard() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/signin');
      return; // Stop execution if not authenticated
    }

    const getTasks = async () => {
      try {
        const fetchedTasks = await fetchTasks();
        setTasks(fetchedTasks);
      } catch (err) {
        setError('Failed to fetch tasks.');
        console.error('Failed to fetch tasks:', err);
        // The outer if-block handles redirection, so this is just for API errors.
      }
    };

    getTasks();
  }, [router]);
  const handleLogout = () => {
    logout();
    router.push('/signin');
  };

  const handleCreateTask = async (description: string) => {
    setError(null);
    try {
      const newTask = await createTask(description);
      setTasks((prevTasks) => [...prevTasks, newTask]);
    } catch (err) {
      setError('Failed to create task.');
      console.error('Failed to create task:', err);
    }
  };

  const handleToggleComplete = async (id: number, completed: boolean) => {
    setError(null);
    try {
      const updatedTask = await updateTask(id, completed);
      setTasks((prevTasks) =>
        prevTasks.map((task) => (task.id === id ? updatedTask : task))
      );
    } catch (err) {
      setError('Failed to update task.');
      console.error('Failed to update task:', err);
    }
  };

  const handleDeleteTask = async (id: number) => {
    setError(null);
    try {
      await deleteTask(id);
      setTasks((prevTasks) => prevTasks.filter((task) => task.id !== id));
    } catch (err) {
      setError('Failed to delete task.');
      console.error('Failed to delete task:', err);
    }
  };

  return (
    <div className="min-h-screen">
      <nav className="bg-gray-900 pb-4 px-8 shadow-lg pt-[10vh]"> {/* Refined navbar background and padding */}
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex-shrink-0">
            <h1 className="text-2xl font-bold neon-heading">Dashboard</h1>
          </div>
          <div>
            <button
              onClick={handleLogout}
              className="neon-button"
            >
              <FaSignOutAlt className="mr-2" /> Logout
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8"> {/* Increased vertical padding */}
        <div className="modern-card"> {/* Applied modern-card class */}
            <h2 className="text-3xl font-bold mb-8 neon-heading text-center">My Tasks</h2> {/* Centered heading */}
            {error && <p className="text-red-500 mb-4 text-center">{error}</p>} {/* Centered error message */}
            <TaskForm onCreateTask={handleCreateTask} />
            {tasks.length > 0 ? (
              <TaskList
                tasks={tasks}
                onToggleComplete={handleToggleComplete}
                onDelete={handleDeleteTask}
              />
            ) : (
              <p className="text-gray-500 text-center py-8">No tasks yet. Add one above!</p>
            )}
          </div>
        </main>
    </div>
  );
}
