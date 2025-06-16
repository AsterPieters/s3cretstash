// src/api/api.js
export const login = async (email, password) => {
  // Your actual API call here
  const response = await fetch('/api/login', { // Adjust this URL to your backend
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Login failed');
  }

  return response.json();
};
