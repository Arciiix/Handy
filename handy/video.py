import threading
import cv2
import socket
import pickle
import zlib
from datetime import datetime

from config import CONFIG

class UDPVideo():
    thread = None
    current_image = None
    
    def init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", CONFIG["UDP_PORT"]))

        self.thread = threading.Thread(target=self.work)
        self.thread.start()
    
    def work(self):
        received_data = b""
        while True:
            segment, addr = self.sock.recvfrom(CONFIG["MAX_PACKET_SIZE"])
            received_data += segment

            try:
                # Attempt to decompress and deserialize the frame
                decompressed_frame = zlib.decompress(received_data)
                serialized_frame = pickle.loads(decompressed_frame)

                self.current_image = serialized_frame

                received_data = b""  # Reset received_data for the next frame
            except zlib.error:
                pass

    def stop(self):
        self.sock.close()
