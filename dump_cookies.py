import os
import browser_cookie3

# Path to Yandex Browser Cookies DB (macOS)
path = os.path.expanduser(
    "~/Library/Application Support/Yandex/YandexBrowser/Default/Cookies"
)

# Load cookies for youtube.com
cj = browser_cookie3.chrome(cookie_file=path, domain_name="youtube.com")

# Save in Netscape format for yt-dlp
with open("cookies.txt", "w") as f:
    for c in cj:
        f.write(
            f"{c.domain}\tTRUE\t{c.path}\t"
            f"{str(c.secure).upper()}\t"
            f"{c.expires}\t{c.name}\t{c.value}\n"
        )

print("✅ cookies.txt will be generated in the current directory when this script is run")
