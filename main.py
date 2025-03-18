import importlib
from concurrent.futures import ThreadPoolExecutor
import time

# List of API modules (add your API module names without ".py")
api_modules = [f"api_{i}" for i in range(1, 31)]  # Dynamically generate API names (api_1 to api_30)

def run_api(api_module_name, mobile, threads):
    """
    Dynamically import and run the main function of the specified API module.
    """
    try:
        api_module = importlib.import_module(api_module_name)  # Import the API module dynamically
        api_module.main(mobile, threads)  # Call the main function of the module
        print(f"[INFO] {api_module_name} executed successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to execute {api_module_name}: {e}")

def main():
    """
    Main function to run all API modules concurrently.
    """
    mobile = input("Enter mobile number (11 digits): ").strip()
    if len(mobile) != 11 or not mobile.isdigit():
        print("[ERROR] Invalid mobile number. Please enter a valid 11-digit number.")
        return

    try:
        threads = int(input("Enter number of concurrent requests per API: "))
        if threads < 1 or threads > 50:
            print("[ERROR] Threads must be between 1 and 50.")
            return
    except ValueError:
        print("[ERROR] Invalid thread count. Please enter a valid number.")
        return

    print(f"\nStarting requests for {len(api_modules)} APIs...\n")

    start_time = time.time()

    # Execute all APIs concurrently
    with ThreadPoolExecutor(max_workers=len(api_modules)) as executor:
        futures = [executor.submit(run_api, module, mobile, threads) for module in api_modules]
        for future in futures:
            future.result()  # Wait for all API threads to complete

    elapsed_time = time.time() - start_time
    print(f"\nAll APIs executed. Total time taken: {elapsed_time:.2f} seconds.\n")

if __name__ == "__main__":
    main()
