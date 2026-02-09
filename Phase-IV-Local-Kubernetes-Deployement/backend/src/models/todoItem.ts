export enum TodoStatus {
  Pending = 'pending',
  Completed = 'completed',
  InProgress = 'in progress',
}

export interface TodoItem {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  status: TodoStatus;
  due_date?: Date;
  created_at: Date;
  updated_at: Date;
}
