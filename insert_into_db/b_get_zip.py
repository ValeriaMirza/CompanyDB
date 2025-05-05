import requests

url = "https://info.gbiz.go.jp/hojin/DownloadJson"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://info.gbiz.go.jp",
    "Referer": "https://info.gbiz.go.jp/hojin/DownloadTop"
}

filename = "Hojinjoho.zip"
chunk_size = 10 * 1024 * 1024
downloaded_bytes = 0
next_print_threshold = chunk_size

print("Sending POST request to initiate download...")
response = requests.post(url, headers=headers,  stream=True)

if response.status_code == 200:
    print("Download started...")
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded_bytes += len(chunk)
                if downloaded_bytes >= next_print_threshold:
                    print(f"Downloaded {downloaded_bytes / (1024 * 1024):.0f} MB")
                    next_print_threshold += chunk_size
    print("Download completed.")
else:
    print("Failed to download.")
