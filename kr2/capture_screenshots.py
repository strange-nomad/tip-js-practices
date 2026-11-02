import subprocess
import os

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
os.makedirs(r"C:\Users\user\Desktop\ТИПЫ\kr2\screenshots", exist_ok=True)

configs = [
    (1, "1000,420"),
    (2, "1000,560"),
    (3, "1000,460"),
    (4, "1000,420"),
    (5, "1000,580"),
]

for num, size in configs:
    html = os.path.abspath(f"kr2/shot{num}.html")
    png = os.path.abspath(f"kr2/screenshots/screenshot{num}.png")
    cmd = [edge, "--headless", f"--screenshot={png}", f"--window-size={size}", f"file:///{html}"]
    print(f"Capturing screenshot {num}...")
    res = subprocess.run(cmd, timeout=20)
    print(f"Screenshot {num} saved: {os.path.exists(png)} (size: {os.path.getsize(png)} bytes)")

print("All screenshots generated successfully!")
