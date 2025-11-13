import requests
import sys

def test_routes(base_url='http://localhost:5000'):
    """
    Tests existing Flask application routes using the requests library
    """
    print(f" Application Testing: {base_url}\n")
    
    # Test 1: Main Site
    try:
        response = requests.get(f'{base_url}/')
        print(f"✅ Test 1 - Main Site [GET /]")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
        assert response.status_code == 200
    except Exception as e:
        print(f"❌ Test 1 failed: {e}\n")
        return False
    
    # Test 2: Health check
    try:
        response = requests.get(f'{base_url}/health')
        print(f"✅ Test 2 - Health check [GET /health]")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
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
        print(f"   Number of Endpoints: {len(response.json()['endpoints'])}\n")
        assert response.status_code == 200
    except Exception as e:
        print(f"❌ Test 3 failed: {e}\n")
        return False
    
    print(" All tests passed successfully!")
    return True

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000'
    success = test_routes(url)
    sys.exit(0 if success else 1)
