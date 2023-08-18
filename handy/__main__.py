import logging
from video import UDPVideo


def main():
    video = UDPVideo()
    video.init()

    while True:
        print(video.current_image)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    main()
