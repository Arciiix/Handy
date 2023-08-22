<div align="center">
    <img src="./assets/Handy512.png" width="120px" height="120px" alt="Handy">
    <h2 align="center">Handy</h2>
</div>

### Easily control your home automations using hand gestures, at any time. This app recognizes the gestures using your security camera footage and controls every IoT action you can dream of. Nothing is impossible - make your life feel like in a sci-fi movie.

# Train

1. [Gather data](./handy/train/0_Gather_Data.ipynb)

1. [Process data](./handy/train/1_Process_Data.ipynb)

1. [Train model](./handy/train/2_Train_Model.ipynb)

1. [Select ROI (region of interest)](./handy/utils/Select_ROI.ipynb)

After completing all above, you can optionally:

1. [Test model](./handy/train/3_Test_Model.ipynb)

# Const values

You can modify some of the preferences a by creating a `config.json` file (`handy/config.json`)

## Required changes:

- STREAM_URL - the URL of the camera video feed - stream
- HOME_ASSISTANT_TOKEN - your [Home Assistant long-lived access token](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token)

## Optional changes:

- FPS_IDLE - frames per second before detection
- FPS - frames per second after detection for gesture recognition
- RESIZE_WIDTH - resize your input image to that width
- RESIZE_HEIGHT - resize your input image to that height
- ENV - change the current running environment - "DEV" or "PROD"
- HOME_ASSISTANT_IP - the URL of your Home Assistant instance. Important: don't put the slash at the end
- MEDIA_PLAYER_HASS_ENTITY_ID - the entity id of the media player inside Home Assistant - used for audio playing (e.g. confirmation of gesture)
- DETECTIONS_TO_KEEP - To prevent false detections caused by accidental gestures or model inaccuracy, Handy caches the last detections. This variable sets the number of detections to store.
- MINIMAL_DETECTIONS - that number of DETECTIONS_TO_KEEP has to be the same to consider a detection as true (and perform the given action)

```json
{
  "STREAM_URL": "udp://127.0.0.1:12345",
  "HOME_ASSISTANT_TOKEN": null,

  "FPS_IDLE": 0.5,
  "FPS": 5,
  "RESIZE_WIDTH": 960,
  "RESIZE_HEIGHT": 540,
  "ENV": "DEV",
  "HOME_ASSISTANT_IP": "http://homeassistant.local:8123",
  "MEDIA_PLAYER_HASS_ENTITY_ID": "media_player.volumio_upnp_av",
  "DETECTIONS_TO_KEEP": 20,
  "MINIMAL_DETECTIONS": 10
}
```

# Command to stream webcam on Linux

ffmpeg -f v4l2 -i /dev/video0 -preset ultrafast -vcodec libx264 -tune zerolatency -b 900k -f h264 udp://<YOUR_IP>:<YOUR_PORT>
