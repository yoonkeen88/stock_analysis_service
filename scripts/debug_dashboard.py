"""
대시보드 API 디버깅 스크립트
"""
import sys
import traceback
sys.path.insert(0, '.')

try:
    from app.services.market_data_service import MarketDataService
    
    print("Testing MarketDataService...")
    service = MarketDataService()
    
    print("\n1. Testing AAPL...")
    try:
        data = service.get_market_data('AAPL', '1mo', '1d')
        print(f"✅ Success!")
        print(f"   Symbol: {data['symbol']}")
        print(f"   Current Price: ${data['current_price']:.2f}")
        print(f"   History points: {len(data['history'])}")
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
    
    print("\n2. Testing TSLA...")
    try:
        data = service.get_market_data('TSLA', '1mo', '1d')
        print(f"✅ Success!")
        print(f"   Symbol: {data['symbol']}")
        print(f"   Current Price: ${data['current_price']:.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Error type: {type(e).__name__}")

except Exception as e:
    print(f"❌ Import error: {e}")
    traceback.print_exc()

