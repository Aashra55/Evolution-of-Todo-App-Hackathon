import TaskItem from './TaskItem';

interface Task {
  id: number;
  description: string;
  completed: boolean;
}

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (id: number, completed: boolean) => void;
  onDelete: (id: number) => void;
}

export default function TaskList({ tasks, onToggleComplete, onDelete }: TaskListProps) {
  return (
    <div className="py-4" style={{ marginTop: '24px' }}>
      {tasks.map((task, index) => (
        <div key={task.id} style={{ marginTop: index > 0 ? '1rem' : '0' }}>
          <TaskItem
            task={task}
            onToggleComplete={onToggleComplete}
            onDelete={onDelete}
          />
        </div>
      ))}
    </div>
  );
}
