import axios from 'axios';

// Backend URL - defaults to localhost for development, uses env var for production
// Docker/Nginx serves the UI and API from the same origin.  A separate URL is
// only needed when running the Vite development server or a remote frontend.
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

export const ensureCsrfCookie = () => api.get('/api/csrf/');

export const predictDisease = async (imageFile) => {
  await ensureCsrfCookie();
  const formData = new FormData();
  formData.append('image', imageFile);

  console.log('Sending prediction request to:', API_BASE_URL + '/api/predict/');
  console.log('Image file:', imageFile);

  try {
    const response = await api.post('/api/predict/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    console.log('Prediction response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error predicting disease:', error);
    console.error('Error response:', error.response);
    console.error('Error status:', error.response?.status);
    console.error('Error data:', error.response?.data);
    throw error;
  }
};

export default api;
