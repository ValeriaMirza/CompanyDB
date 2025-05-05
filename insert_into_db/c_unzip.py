import requests
import zipfile
import os
filename = "Hojinjoho.zip"
output_dir = "unzipped_hojin"
print(f"Unzipping contents to '{output_dir}'...")
os.makedirs(output_dir, exist_ok=True)
with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall(output_dir)
print("Unzipping completed.")
os.remove(filename)
print(f"Deleted '{filename}' after unzipping.")