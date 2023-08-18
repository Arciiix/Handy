<div align="center">
    <img src="./assets/Handy512.png" width="120px" height="120px" alt="Handy">
    <h2 align="center">Handy</h2>
</div>

### Easily control your home automations using hand gestures, at any time. This app recognizes the gestures using your security camera footage and controls every IoT action you can dream of. Nothing is impossible - make your life feel like in a sci-fi movie.

# Const values

You can modify some of the preferences a by creating a `config.json` file (`handy/config.json`)

```json
{
  // If you want to receive the camera stream from UDP, you can modify the values below. Note that they have to match with your cilent settings (see below).
  "UDP_PORT": 30001,
  "MAX_PACKET_SIZE": 65507 // Better to not change it
}
```

If you also want to use the client script (to stream the webcam), you can additionally modify another preferences also by creating a `config.json` file (`handy/client/config.json`) and using the template below:

```json
{
  "UDP_IP": "YOUR_SERVER_IP",
  "UDP_PORT": 30001,
  "MAX_PACKET_SIZE": 65507, // Better to not change it,
  "CAMERA": "/dev/video0",
  "FPS": 1
}
```
