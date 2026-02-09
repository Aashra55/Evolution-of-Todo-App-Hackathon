import { useState } from 'react';
import { FaPlus } from 'react-icons/fa'; // Import the icon

interface TaskFormProps {
  onCreateTask: (description: string) => void;
}

export default function TaskForm({ onCreateTask }: TaskFormProps) {
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim()) return;
    onCreateTask(description);
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex mb-10" style={{gap: '1.5rem'}}> {/* Adjusted margin-bottom */}
      <input
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Add a new task"
        className="input-field-modern flex-grow" /* Applied modern input style */
      />
      <button
        type="submit"
        className="neon-button"
      >
        <FaPlus /> Add Task
      </button>
    </form>
  );
}
