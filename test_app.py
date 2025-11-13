import requests
import sys

def test_routes(base_url='http://localhost:5000'):
    """
    Testuje istniejące route'y aplikacji Flask używając biblioteki requests
    """
    print(f"🧪 Testowanie aplikacji: {base_url}\n")
    
    # Test 1: Główna strona
    try:
        response = requests.get(f'{base_url}/')
        print(f"✅ Test 1 - Strona główna [GET /]")
        print(f"   Status: {response.status_code}")
        print(f"   Odpowiedź: {response.json()}\n")
        assert response.status_code == 200
    except Exception as e:
        print(f"❌ Test 1 failed: {e}\n")
        return False
    
    # Test 2: Health check
    try:
        response = requests.get(f'{base_url}/health')
        print(f"✅ Test 2 - Health check [GET /health]")
        print(f"   Status: {response.status_code}")
        print(f"   Odpowiedź: {response.json()}\n")
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'
    except Exception as e:
        print(f"❌ Test 2 failed: {e}\n")
        return False
    
    # Test 3: API Info
    try:
        response = requests.get(f'{base_url}/api/info')
        print(f"✅ Test 3 - API Info [GET /api/info]")
        print(f"   Status: {response.status_code}")
        print(f"   Liczba endpointów: {len(response.json()['endpoints'])}\n")
        assert response.status_code == 200
    except Exception as e:
        print(f"❌ Test 3 failed: {e}\n")
        return False
    
    print("🎉 Wszystkie testy przeszły pomyślnie!")
    return True

if __name__ == '__main__':
    # Możesz podać URL jako argument
    url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000'
    success = test_routes(url)
    sys.exit(0 if success else 1)
