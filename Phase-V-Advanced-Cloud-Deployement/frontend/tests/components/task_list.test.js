// frontend/tests/components/task_list.test.js
import { render, screen } from '@testing-library/react';
import TaskList from '../../src/components/task_list'; // Assuming a TaskList component will be created

describe('TaskList Component', () => {
  it('renders without crashing', () => {
    // This is a placeholder test.
    // In a real scenario, you'd render the TaskList component and assert its initial state.
    const tasks = []; // Mock tasks
    render(<TaskList tasks={tasks} />);
    expect(screen.getByText(/No tasks yet/i)).toBeInTheDocument();
  });

  it('displays a list of tasks', () => {
    // This is a placeholder test.
    // In a real scenario, you'd render the TaskList with mock tasks and assert their presence.
    const tasks = [
      { id: '1', title: 'Buy groceries', status: 'pending' },
      { id: '2', title: 'Finish report', status: 'completed' },
    ];
    render(<TaskList tasks={tasks} />);
    expect(screen.getByText(/Buy groceries/i)).toBeInTheDocument();
    expect(screen.getByText(/Finish report/i)).toBeInTheDocument();
  });
});
