import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import SplashScreen from './components/SplashScreen';
import ThemeToggle from './components/ThemeToggle';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import './styles/global.css';
import './App.css';

function App() {
  console.log('[App] Component rendered');
  
  const [showSplash, setShowSplash] = useState(true);

  const handleSplashFinish = () => {
    console.log('[App] Splash finished, showing main app');
    setShowSplash(false);
  };
  
  // 컴포넌트 마운트 확인
  useEffect(() => {
    console.log('[App] Component mounted');
    return () => {
      console.log('[App] Component unmounted');
    };
  }, []);

  return (
    <>
      {showSplash && <SplashScreen onFinish={handleSplashFinish} />}
      {!showSplash && (
        <Router>
          <div className="App">
            <ThemeToggle />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/dashboard/:symbol" element={<Dashboard />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
        </Router>
      )}
    </>
  );
}

export default App;

