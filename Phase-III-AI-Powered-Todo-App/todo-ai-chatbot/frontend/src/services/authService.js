// frontend/src/services/authService.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api'; // Your FastAPI backend URL

const authService = {
  async register(username, password, email) { // Added email parameter
    try {
      const response = await axios.post(`${API_BASE_URL}/register`, { username, password, email }); // Include email
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || error.message;
    }
  },

  async login(username, password) {
    try {
      const form_data = new URLSearchParams();
      form_data.append('username', username);
      form_data.append('password', password);

      const response = await axios.post(`${API_BASE_URL}/token`, form_data, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      const { access_token } = response.data;
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', access_token);
      }
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || error.message;
    }
  },

  logout() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
    // Optionally, clear other user-related data from local storage
  },

  getAccessToken() {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token');
    }
    return null;
  },

  isAuthenticated() {
    return !!this.getAccessToken();
  }
};

export default authService;
