<div align="center">
    <img src="./assets/Handy512.png" width="120px" height="120px" alt="Handy">
    <h2 align="center">Handy</h2>
</div>

### Easily control your home automations using hand gestures, at any time. This app recognizes the gestures using your security camera footage and controls every IoT action you can dream of. Nothing is impossible - make your life feel like in a sci-fi movie.

# Prerequirements

- [Home Assistant](https://www.home-assistant.io/)

**IMPORTANT:** Before using the app, please upload the audio from the /handy/audio/ directory to Home Assistant as local media.

# Train

1. [Gather data](./handy/train/0_Gather_Data.ipynb)

1. [Process data](./handy/train/1_Process_Data.ipynb)

1. [Train model](./handy/train/2_Train_Model.ipynb)

1. [Select ROI (region of interest), T-ROI (trigger region of interest), and G-ROI (gesture region of interest)](./handy/utils/Select_ROI.ipynb)

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
- ACTION_BLOCK_DELAY_SECONDS - to prevent user from accidently performing the same action after they show the gesture and didn't manage to stop showing it, add some blocking delay between next action
- FAST_MODE_DURATION_SECONDS - normally the app works in an idle mode on low FPS. When user enters the T-ROI or a gesture within G-ROI is detected, the app turns into fast mode with high FPS. This variable determines how long it should remain in the fast mode after the last movement.
- REQUIRED_TROI_PERCENT_CHANGE - this amount of the T-ROI frame has to be different for Handy to consider a movement inside it. Unit is percent [%].
- NUMERIC_VALUE_MAX_WAITING_TIME_SECONDS - there are some actions, like changing volume, that have to know the numeric value of change (see `numeric_value_track` in `numeric_value_track.py`). This value determines how many seconds user can stand without raising neither of their arms to be considered as idle (so cancel the action)
- GET_NUMERIC_VALUE_INTERVAL_SECONDS - see above - the handler will be called every n seconds, where n is this value.
- LANGUAGE - can be either "pl" or "en" - the announcements will be said in that language, e.g. the current time.
- MIN_ARM_ANGLE_FOR_NUMERIC_VALUE_CHANGE - Minimum angle for arm to be considered as raised (which, in numeric vaule mode, causes the value to be either increased or decreased).

## Action-related changes

- PLAYER_PLAYPAUSE_HASS_ENTITY_ID - this media_player entity will be used for play/pause action
- PLAYER_VOLUME_HASS_ENTITY_ID - this media_player entity will be used for volume change action
- PLAYER_NEXTPLAYLISTITEM_HASS_ENTITY_ID - this media_player entity will be used for playing next playlist item (see below for playlist)
- WEATHER_HASS_ENTITY_ID - this weather entity will be used for weather info

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
  "MEDIA_PLAYER_HASS_ENTITY_ID": "media_player.mpd",
  "DETECTIONS_TO_KEEP": 20,
  "MINIMAL_DETECTIONS": 10,
  "ACTION_BLOCK_DELAY_SECONDS": 5,
  "FAST_MODE_DURATION_SECONDS": 3,
  "REQUIRED_TROI_PERCENT_CHANGE": 0.5,
  "NUMERIC_VALUE_MAX_WAITING_TIME_SECONDS": 8,
  "GET_NUMERIC_VALUE_INTERVAL_SECONDS": 1,
  "LANGUAGE": "en",
  "MIN_ARM_ANGLE_FOR_NUMERIC_VALUE_CHANGE": 70,

  "PLAYER_PLAYPAUSE_HASS_ENTITY_ID": "media_player.volumio",
  "PLAYER_NEXTPLAYLISTITEM_HASS_ENTITY_ID": "media_player.mpd",
  "PLAYER_VOLUME_HASS_ENTITY_ID": "media_player.volumio",
  "WEATHER_HASS_ENTITY_ID": "weather.openweathermap"
}
```

# Playlist

The "next playlist item" action needs some playlist to play. You can define it in the playlist.json file using the following format:

```json
[
  {
    "name": "your_media_name",
    "pronunciation": "since radio stations and songs are often pronounced differently, provide their pronunciation here",
    "url": "your_media_url"
  }
]
```

# Using with Volumio

If you want to use Handy with [**Volumio**](https://volumio.com/en/get-started/) (like I do), you have to note that there's a huge difference between the [**Volumio integration in Home Assistant**](https://www.home-assistant.io/integrations/volumio/) and [**MPD**](https://www.home-assistant.io/integrations/mpd/) (it's not the same as [**DLNA Digital Media Renderer**](https://www.home-assistant.io/integrations/dlna_dmr/) - this one is useless and buggy for Volumio).

You should use both [Volumio](https://www.home-assistant.io/integrations/volumio/) and [MPD](https://www.home-assistant.io/integrations/mpd/) integration. The first one is good for just controlling Volumio, whereas the second one is required to get current played media or play something on Volumio. See the default config - `media_player.volumio` is the Volumio integration and `media_player.mpd` is the Music Player Daemon (which is still Volumio). The MPD is a perfect thing - it comes back to the previously played media when using TTS (announce mode) - which is just ideal for Handy and solves tones of unnecessary problems DLNA_DMR or Volumio has.

To set up MPD in Home Assistant, please add:

```yaml
- platform: mpd
  name: volumio_mpd
  host: your.volumio.ip.address
```

# Command to stream webcam on Linux

ffmpeg -f v4l2 -i /dev/video0 -preset ultrafast -vcodec libx264 -tune zerolatency -b 900k -f h264 udp://<YOUR_IP>:<YOUR_PORT>
