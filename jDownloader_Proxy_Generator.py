import sys
import subprocess
import importlib
import asyncio

def install_packages():
    """
    Checks for required packages and installs them if missing.
    """
    # Mapping of module names to package names
    packages = {
        'requests': 'requests',
        'bs4': 'beautifulsoup4',
        'aiohttp_socks': 'aiohttp-socks',
        'aiohttp': 'aiohttp'
    }

    missing_packages = []

    # Check for each required package
    for module, package in packages.items():
        try:
            importlib.import_module(module)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"Missing packages detected: {', '.join(missing_packages)}")
        try:
            print(f"Installing packages: {', '.join(missing_packages)}")
            # Install missing packages using pip
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
            print("Package installation successful.\n")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install packages: {e}")
            print("Please install the required packages manually and rerun the script.")
            sys.exit(1)
    else:
        print("All required packages are already installed.\n")

def scrape_socks4_proxies(url):
    """
    Scrapes SOCKS4 proxies from the given URL.
    """
    import requests
    from bs4 import BeautifulSoup

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'  # Mimic a real browser
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    proxies = []

    table = soup.find('table')
    if not table:
        print("No table found on the webpage.")
        return proxies

    rows = table.find_all('tr')
    if not rows:
        print("No rows found in the table.")
        return proxies

    # Assume the first row is the header
    header = [th.get_text(strip=True).lower() for th in rows[0].find_all(['th', 'td'])]

    try:
        ip_index = header.index('ip address')
        port_index = header.index('port')
        version_index = header.index('version')
        print("Successfully identified table columns.")
    except ValueError as e:
        print(f"Expected column not found: {e}")
        return proxies

    for row in rows[1:]:
        cols = row.find_all(['td', 'th'])
        if len(cols) < max(ip_index, port_index, version_index) + 1:
            continue  # Skip incomplete rows

        ip = cols[ip_index].get_text(strip=True)
        port = cols[port_index].get_text(strip=True)
        version = cols[version_index].get_text(strip=True).lower()

        if version == 'socks4':
            proxy = f"socks4://{ip}:{port}"
            proxies.append(proxy)
            print(f"Scraped proxy: {proxy}")

    return proxies

async def test_proxy(proxy, valid_proxies, semaphore, test_url='http://httpbin.org/ip', timeout=10):
    """
    Tests a single proxy by attempting to make a request through it.
    If successful, adds it to the valid_proxies list.
    """
    import aiohttp
    from aiohttp_socks import ProxyConnector

    try:
        connector = ProxyConnector.from_url(proxy)
        async with semaphore:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(test_url, timeout=timeout) as response:
                    if response.status == 200:
                        data = await response.json()
                        origin_ip = data.get('origin')
                        proxy_ip = proxy.split('//')[1].split(':')[0]
                        if proxy_ip in origin_ip:
                            print(f"Valid proxy: {proxy}")
                            valid_proxies.append(proxy)
    except aiohttp.ClientProxyConnectionError as e:
        print(f"Invalid proxy: {proxy} | Proxy Connection Error: {e}")
    except aiohttp.ClientOSError as e:
        print(f"Invalid proxy: {proxy} | OS Error: {e}")
    except asyncio.TimeoutError:
        print(f"Invalid proxy: {proxy} | Connection Timeout")
    except Exception as e:
        print(f"Invalid proxy: {proxy} | Error: {e}")

async def test_all_proxies(proxies, valid_proxies, concurrency=100):
    """
    Tests all proxies asynchronously with a limit on concurrency.
    """
    semaphore = asyncio.Semaphore(concurrency)
    tasks = [test_proxy(proxy, valid_proxies, semaphore) for proxy in proxies]
    await asyncio.gather(*tasks)

def save_proxies(filename, proxies):
    """
    Saves a list of proxies to a specified file.
    """
    try:
        with open(filename, 'w') as f:
            for proxy in proxies:
                f.write(proxy + '\n')
        print(f"\nProxies have been saved to '{filename}'.")
    except IOError as e:
        print(f"Failed to write to file '{filename}': {e}")

def main():
    """
    Main function to scrape, test, and save SOCKS4 proxies.
    """
    url = 'https://socks-proxy.net/#list'  # Replace with the actual URL if different
    print("Starting proxy scraping...")
    proxies = scrape_socks4_proxies(url)

    if proxies:
        # Save all scraped proxies
        save_proxies('all_scraped_proxies.txt', proxies)

        print(f"\nScraped {len(proxies)} SOCKS4 proxies. Starting tests...\n")

        valid_proxies = []
        asyncio.run(test_all_proxies(proxies, valid_proxies, concurrency=100))

        if valid_proxies:
            print(f"\nFound {len(valid_proxies)} valid SOCKS4 proxies:")
            for proxy in valid_proxies:
                print(proxy)
            # Save valid proxies
            save_proxies('valid_socks4_proxies.txt', valid_proxies)
        else:
            print("\nNo valid SOCKS4 proxies found.")
    else:
        print("\nNo SOCKS4 proxies scraped.")

    input("\nPress Enter to exit...")  # Keeps the window open

if __name__ == "__main__":
    install_packages()
    main()
