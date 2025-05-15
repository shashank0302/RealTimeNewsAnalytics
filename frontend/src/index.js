import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// Use createRoot API for better performance
const root = createRoot(document.getElementById('root'));
root.render(
  // Use production mode (remove React.StrictMode in production for performance)
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Measure performance
reportWebVitals(metric => {
  // Send metrics to analytics if needed
  if (metric.value > 500 && ['FCP', 'LCP', 'CLS'].includes(metric.name)) {
    console.warn(`Performance issue: ${metric.name} = ${Math.round(metric.value)}`);
  }
});
