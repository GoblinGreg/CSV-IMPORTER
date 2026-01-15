import requests
import sys
import time


def test_routes(base_url='http://localhost:5000'):
    """Tests updated to match UI endpoints: / (HTML), /health (JSON), /api/info (JSON).
    Also performs a sample upload to ensure the upload endpoint accepts files."""
    print(f" Application Testing: {base_url}\n")

    # Test 1: Main Site (HTML)
    try:
        response = requests.get(f'{base_url}/')
        print(f"✅ Test 1 - Main Site [GET /]")
        print(f"   Status: {response.status_code}")
        assert response.status_code == 200
        assert 'CSV Importer' in response.text
    except Exception as e:
        print(f"❌ Test 1 failed: {e}\n")
        return False

    # Test 2: Health check (JSON)
    try:
        response = requests.get(f'{base_url}/health')
        print(f"✅ Test 2 - Health check [GET /health]")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
        assert response.status_code == 200
        assert response.json().get('status') == 'healthy'
    except Exception as e:
        print(f"❌ Test 2 failed: {e}\n")
        return False

    # Test 3: API Info (JSON)
    try:
        response = requests.get(f'{base_url}/api/info')
        print(f"✅ Test 3 - API Info [GET /api/info]")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Number of Endpoints: {len(data.get('endpoints', []))}\n")
        assert response.status_code == 200
        assert isinstance(data.get('endpoints'), list)
    except Exception as e:
        print(f"❌ Test 3 failed: {e}\n")
        return False

    # Test 4: Upload a small CSV (multipart)
    try:
        csv_content = 'col1,col2\n10,20\n30,40\n'
        files = {'file': ('sample.csv', csv_content, 'text/csv')}
        headers = {'Accept': 'application/json'}
        resp = requests.post(
            f'{base_url}/upload', files=files, headers=headers, allow_redirects=False)
        print(f"✅ Test 4 - Upload CSV [POST /upload]")
        print(f"   Status: {resp.status_code}")
        assert resp.status_code in (200, 302, 303)
    except Exception as e:
        print(f"❌ Test 4 failed: {e}\n")
        return False

    print(" All tests passed successfully!")
    return True


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000'
    success = test_routes(url)
    sys.exit(0 if success else 1)
