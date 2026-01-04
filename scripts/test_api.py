"""
API 테스트 스크립트
백엔드 API가 제대로 작동하는지 확인
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """헬스 체크"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✅ Health Check: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health Check 실패: {e}")
        return False

def test_dashboard(symbol="AAPL"):
    """대시보드 API 테스트"""
    try:
        url = f"{BASE_URL}/dashboard/{symbol}"
        print(f"\n📊 Dashboard API 테스트: {symbol}")
        print(f"   URL: {url}")
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 성공!")
            print(f"   Symbol: {data.get('symbol', 'N/A')}")
            print(f"   Market Data: {'있음' if data.get('market_data') else '없음'}")
            print(f"   Predictions: {len(data.get('predictions', []))}개")
            print(f"   News: {len(data.get('news', []))}개")
            return True
        else:
            print(f"❌ 실패: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ 연결 실패: 백엔드 서버가 실행 중인지 확인하세요")
        print(f"   실행 명령: python -m app.main")
        return False
    except Exception as e:
        print(f"❌ 에러: {e}")
        return False

def test_stock_quote(symbol="AAPL"):
    """주식 시세 API 테스트"""
    try:
        url = f"{BASE_URL}/stocks/quote/{symbol}"
        print(f"\n📈 Stock Quote API 테스트: {symbol}")
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 성공!")
            print(f"   Symbol: {data.get('symbol')}")
            print(f"   Current Price: ${data.get('current_price', 0):.2f}")
            print(f"   Change: {data.get('change', 0):.2f} ({data.get('change_percent', 0):.2f}%)")
            return True
        else:
            print(f"❌ 실패: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 에러: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("API 테스트 시작")
    print("=" * 50)
    
    # 헬스 체크
    if not test_health():
        print("\n⚠️  백엔드 서버를 먼저 실행하세요:")
        print("   python -m app.main")
        exit(1)
    
    # 대시보드 API 테스트
    test_dashboard("AAPL")
    
    # 주식 시세 API 테스트
    test_stock_quote("AAPL")
    
    print("\n" + "=" * 50)
    print("테스트 완료")
    print("=" * 50)

