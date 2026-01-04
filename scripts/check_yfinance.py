"""
yfinance 작동 확인 스크립트
"""
import sys

try:
    import yfinance as yf
    print("✅ yfinance 설치됨")
except ImportError:
    print("❌ yfinance가 설치되지 않았습니다")
    print("   설치: pip install yfinance")
    sys.exit(1)

# 테스트 심볼들
test_symbols = ['AAPL', 'TSLA', 'MSFT', 'BTC-USD']

print("\n📊 yfinance 테스트 시작...\n")

for symbol in test_symbols:
    try:
        print(f"테스트: {symbol}")
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if info and 'symbol' in info:
            print(f"  ✅ 성공!")
            print(f"     심볼: {info.get('symbol')}")
            print(f"     이름: {info.get('longName', 'N/A')}")
            print(f"     현재가: ${info.get('currentPrice', 'N/A')}")
        else:
            print(f"  ⚠️  데이터 없음 (심볼이 올바른지 확인)")
            
        # 히스토리 데이터 테스트
        hist = ticker.history(period="5d", interval="1d")
        if not hist.empty:
            print(f"     히스토리: {len(hist)}개 데이터 포인트")
        else:
            print(f"     ⚠️  히스토리 데이터 없음")
            
    except Exception as e:
        print(f"  ❌ 에러: {str(e)}")
    
    print()

print("=" * 50)
print("테스트 완료")
print("=" * 50)
print("\n💡 팁:")
print("   - 주식: AAPL, TSLA, MSFT 등")
print("   - 암호화폐: BTC-USD, ETH-USD 등 (반드시 -USD 붙이기)")

