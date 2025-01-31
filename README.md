# Jdownloader-Proxy-List-Generator

## Overview

The **Jdownloader-Proxy-List-Generator** is a Python-based tool designed to efficiently scrape SOCKS4 proxies from a specified website, validate their functionality, and organize them into separate lists for easy reference and use. Utilizing asynchronous programming, this script ensures rapid processing, making it ideal for handling large proxy lists.

## Features

- **Automatic Dependency Installation:** Checks for and installs required Python packages if they are missing.
- **Scraping Capability:** Extracts SOCKS4 proxies (IP and port) from a specified website.
- **Dual Output Files:**
  - **All Scraped Proxies:** Saved to `all_scraped_proxies.txt`.
  - **Valid Proxies:** Filtered and saved to `valid_socks4_proxies.txt`.
- **Asynchronous Validation:** Utilizes `asyncio` and `aiohttp` for fast and efficient proxy testing.
- **User-Friendly Execution:** Provides clear console outputs and pauses at the end for easy result review.

## Requirements

- **Operating System:** Windows, macOS, or Linux.
- **Python Version:** Python 3.7 or higher.
- **Internet Connection:** Required for scraping proxies and validating their functionality.

## Installation

1. **Clone or Download the Script:**
   - Save the script to your desired directory

2. **Run the Script:**
   - **Via Terminal:**
     1. Open **Command Prompt** or **PowerShell**.
     2. Navigate to the script's directory:
        ```powershell
        cd "C:\"
        ```
     3. Execute the script:
        ```powershell
        python proxy_scraper.py
        ```
   - **By Double-Clicking:**
     1. Ensure that `.py` files are associated with the official Python interpreter.
     2. Navigate to the script location in **File Explorer**.
     3. Double-click `proxy_scraper.py` to run.

> **Note:** The script automatically installs any missing dependencies (`requests`, `beautifulsoup4`, `aiohttp`, `aiohttp-socks`) at runtime. Ensure you have an active internet connection for this process.

## Usage

1. **Start the Script:**
   - Upon running, the script will:
     - Check and install necessary dependencies.
     - Scrape SOCKS4 proxies from the specified URL (`https://socks-proxy.net/#list`).
     - Save all scraped proxies to `all_scraped_proxies.txt`.
     - Asynchronously validate each proxy.
     - Save only the valid proxies to `valid_socks4_proxies.txt`.

2. **Review Outputs:**
   - **All Scraped Proxies:** Located in `all_scraped_proxies.txt`.
   - **Valid Proxies:** Located in `valid_socks4_proxies.txt`.
   - **Console Output:** Displays the scraping progress, validation results, and any errors encountered.

3. **Exit the Script:**
   - After processing, the script will prompt:
     ```
     Press Enter to exit...
     ```
   - Press **Enter** to close the script window.

## Output Files

- **`all_scraped_proxies.txt`**
  - **Description:** Contains a comprehensive list of all SOCKS4 proxies scraped from the source.
  - **Format:** Each proxy is listed on a new line in the format `socks4://IP:Port`.

- **`valid_socks4_proxies.txt`**
  - **Description:** Contains only the proxies that successfully passed the validation tests.
  - **Format:** Each valid proxy is listed on a new line in the format `socks4://IP:Port`.

## Troubleshooting

- **ModuleNotFoundError: No module named 'aiohttp'**
  - **Cause:** Dependencies are not installed before attempting to import.
  - **Solution:** Ensure that you have an active internet connection when running the script so it can install missing packages automatically. If the issue persists, manually install the required packages:
    ```powershell
    pip install requests beautifulsoup4 aiohttp aiohttp-socks
    ```

- **Script Fails to Run or Closes Immediately:**
  - **Cause:** Errors occurring before the script completes execution.
  - **Solution:** Run the script via Terminal or Command Prompt to view error messages. Ensure all dependencies are installed and that the target website (`https://socks-proxy.net/#list`) is accessible.

- **No Proxies Found or Valid Proxies List is Empty:**
  - **Cause:** The target website may have changed its structure, or the scraped proxies are mostly invalid.
  - **Solution:**
    - Verify that the website structure matches the script's scraping logic. Update the parsing logic if necessary.
    - Consider using more reliable proxy sources or paid proxy services for higher validity rates.

## Best Practices

- **Regular Updates:** Proxies can become inactive quickly. Schedule the script to run periodically (e.g., daily) to maintain an updated proxy list.
- **Ethical Usage:** Use proxies responsibly and in compliance with target websites' terms of service and legal guidelines.
- **Resource Management:** Adjust the `concurrency` parameter in the script based on your system's capabilities to optimize performance without overloading your network.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

---
