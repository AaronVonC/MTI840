import socket
import os
from time import sleep
import tqdm
SEPARATOR="<SEPARATOR>"
BUFFER_SIZE = 4096
host = "192.168.56.1"
port = 5001


os.system("fswebcam -r 1280x720 --no-banner image/image.jpg")
filename = "image/image.jpg"
filesize = os.path.getsize(filename)
s=socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")
s.send(f"{filename}{SEPARATOR}{filesize}".encode())
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))
s.close()
