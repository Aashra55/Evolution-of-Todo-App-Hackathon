const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export const signup = async (email: string, password: string) => {
  const response = await fetch(`${API_BASE_URL}auth/signup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    throw new Error('Signup failed');
  }
  return response.json();
};

export const signin = async (email: string, password: string) => {
  const response = await fetch(`${API_BASE_URL}auth/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      username: email,
      password: password,
    }),
  });
  if (!response.ok) {
    throw new Error('Signin failed');
  }
  return response.json();
};

export const logout = () => {
  localStorage.removeItem('token');
};

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No authentication token found');
  }
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

export const isAuthenticated = (): boolean => {
  return localStorage.getItem('token') !== null;
};

export const fetchTasks = async () => {
  const response = await fetch(`${API_BASE_URL}tasks/`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    const errorBody = await response.text();
    console.error('Failed to fetch tasks:', response.status, response.statusText, errorBody);
    throw new Error('Failed to fetch tasks');
  }
  return response.json();
};

export const createTask = async (description: string) => {
  const response = await fetch(`${API_BASE_URL}tasks/`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ description }),
  });
  if (!response.ok) {
    throw new Error('Failed to create task');
  }
  return response.json();
};

export const updateTask = async (id: number, completed: boolean) => {
  const response = await fetch(`${API_BASE_URL}tasks/${id}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify({ completed }),
  });
  if (!response.ok) {
    throw new Error('Failed to update task');
  }
  return response.json();
};

export const deleteTask = async (id: number) => {
  const response = await fetch(`${API_BASE_URL}tasks/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    throw new Error('Failed to delete task');
  }
};
