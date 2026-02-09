import { FaTrashAlt } from 'react-icons/fa'; // Import the icon

interface Task {
  id: number;
  description: string;
  completed: boolean;
}

interface TaskItemProps {
  task: Task;
  onToggleComplete: (id: number, completed: boolean) => void;
  onDelete: (id: number) => void;
}

export default function TaskItem({ task, onToggleComplete, onDelete }: TaskItemProps) {
  return (
    <div className="flex items-center justify-between p-6 bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 relative"> {/* Darker background, more pronounced shadow, hover effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-transparent via-transparent to-transparent opacity-0 hover:opacity-10 transition-opacity duration-300 pointer-events-none"></div> {/* Subtle overlay for depth */}
      <div className="flex items-center z-10">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggleComplete(task.id, !task.completed)}
          className="neon-checkbox" /* Applied new neon-checkbox style */
        />
        <span className={`ml-4 text-lg ${task.completed ? 'line-through text-gray-500' : 'text-foreground'}`}>
          {task.description}
        </span>
      </div>
      <button
        onClick={() => onDelete(task.id)}
        className="neon-button-red z-10 mx-2" /* Applied neon-button-red directly */
      >
        <FaTrashAlt />
      </button>
    </div>
  );
}