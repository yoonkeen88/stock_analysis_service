import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

const rootElement = document.getElementById('root');
console.log('[Main] Root element:', rootElement);

if (!rootElement) {
  console.error('[Main] ❌ Root element not found!');
} else {
  console.log('[Main] Creating React root...');
  const root = ReactDOM.createRoot(rootElement);
  
  console.log('[Main] Rendering App component...');
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  );
  console.log('[Main] ✅ App rendered');
}

