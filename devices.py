import socket
import os
from time import sleep
import tqdm
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, GPIO.PUD_DOWN)
SEPARATOR="<SEPARATOR>"
BUFFER_SIZE = 4096
host = "10.196.113.18"
port = 8080
while(1):
    if GPIO.input(13)==0:
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
