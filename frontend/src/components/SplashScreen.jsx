import { useEffect, useState } from 'react';
import './SplashScreen.css';

/**
 * 스플래시 화면 컴포넌트
 * 앱 로딩 시 표시되는 초기 화면
 */
const SplashScreen = ({ onFinish }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // 최소 1.5초 표시 후 페이드 아웃
    const timer = setTimeout(() => {
      setIsVisible(false);
      // 페이드 아웃 애니메이션 후 콜백 실행
      setTimeout(() => {
        onFinish?.();
      }, 500); // CSS transition 시간과 맞춤
    }, 1500);

    return () => clearTimeout(timer);
  }, [onFinish]);

  return (
    <div className={`splash-screen ${isVisible ? 'visible' : 'hidden'}`}>
      <div className="splash-content">
        <div className="splash-logo">
          <div className="logo-icon">📈</div>
          <h1 className="logo-text">Stock Analysis</h1>
        </div>
        <div className="splash-subtitle">
          최신 논문 기반 주식/비트코인 예측 서비스
        </div>
        <div className="splash-loader">
          <div className="loader-dot"></div>
          <div className="loader-dot"></div>
          <div className="loader-dot"></div>
        </div>
      </div>
    </div>
  );
};

export default SplashScreen;

