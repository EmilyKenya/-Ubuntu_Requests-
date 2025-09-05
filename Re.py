import requests
import os
from urllib.parse import urlparse
import hashlib

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Get one or multiple URLs from user (comma-separated)
    urls = input("https://assets.ubuntu.com/v1/29985a98-ubuntu-logo32.png, https://example.com/ubuntu-wallpaper.jpg, https://assets.ubuntu.com/v1/8dd99b80-suru-icons.png: ").split(",")

    for url in urls:
        url = url.strip()
        if not url:
            continue

        try:
            # Create directory if it doesn't exist
            os.makedirs("Fetched_Images", exist_ok=True)

            # Fetch the image with precautions
            headers = {"User-Agent": "UbuntuImageFetcher/1.0"}
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()  # Raise exception for bad status codes

            # Check important headers before saving
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"✗ Skipped {url} — not an image (Content-Type: {content_type})")
                continue

            # Extract filename from URL or generate one
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)

            if not filename:
                filename = "downloaded_image.jpg"

            # Prevent duplicate downloads (check hash of content)
            image_hash = hashlib.md5(response.content).hexdigest()
            filepath = os.path.join("Fetched_Images", filename)

            if os.path.exists(filepath):
                with open(filepath, "rb") as existing_file:
                    existing_hash = hashlib.md5(existing_file.read()).hexdigest()
                    if existing_hash == image_hash:
                        print(f"✓ Skipped duplicate: {filename}")
                        continue
                    else:
                        # If same name but different content, rename
                        filename = f"{os.path.splitext(filename)[0]}_{image_hash[:6]}.jpg"
                        filepath = os.path.join("Fetched_Images", filename)

            # Save the image
            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error for {url}: {e}")
        except Exception as e:
            print(f"✗ An error occurred: {e}")

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
