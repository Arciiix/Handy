<div align="center">
    <img src="./assets/Handy512.png" width="120px" height="120px" alt="Handy">
    <h2 align="center">Handy</h2>
</div>

### Easily control your home automations using hand gestures, at any time. This app recognizes the gestures using your security camera footage and controls every IoT action you can dream of. Nothing is impossible - make your life feel like in a sci-fi movie.

# Const values

You can modify some of the preferences a by creating a `config.json` file (`handy/config.json`)

- STREAM_URL - the URL of the camera video feed - stream
- FPS - frames per second
- RESIZE_WIDTH - resize your input image to that width
- RESIZE_HEIGHT - resize your input image to that height

```json
{
  "STREAM_URL": "udp://127.0.0.1:12345",
  "FPS": 1,
  "RESIZE_WIDTH": 960,
  "RESIZE_HEIGHT": 540
}
```

# Command to stream webcam on Linux

ffmpeg -f v4l2 -i /dev/video0 -preset ultrafast -vcodec libx264 -tune zerolatency -b 900k -f h264 udp://<YOUR_IP>:<YOUR_PORT>
