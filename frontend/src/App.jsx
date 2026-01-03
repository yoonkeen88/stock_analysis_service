import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Stock Analysis Service</h1>
          <p>최신 논문 기반 주식/비트코인 예측 웹 서비스</p>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<div>Home Page - Coming Soon</div>} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

