import "dart:async";

import "package:flutter/material.dart";
import "package:handy/gen/strings.g.dart";
import "package:handy/providers/socket_provider.dart";
import "package:handy/utils/process_socket_response.dart";
import "package:hooks_riverpod/hooks_riverpod.dart";

class ControlDialog extends ConsumerStatefulWidget {
  const ControlDialog({super.key});

  @override
  ControlDialogState createState() => ControlDialogState();
}

class ControlDialogState extends ConsumerState<ControlDialog> {
  int currentVolume = 50;
  bool isPlaying = false;

  int localVolume = 50;

  bool isLoading = true;

  bool isChangingPlaybackState = false;

  Timer?
      volumeDebounce; // To not spam the server, use a debounce for changing volume

  void getCurrentState() async {
    setState(() {
      isLoading = true;
    });
    print("do stuff");

    var socket = ref.read(socketClientProvider);

    Completer c = Completer();
    print("start!");
    socket.emitWithAck("playback/state", {}, ack: (data) {
      print("Received callback");
      print(data);
      bool isSuccess = processSocketRepsonse(context, data);

      if (isSuccess && mounted) {
        setState(() {
          isPlaying = data["state"] == "playing";
          currentVolume = data["volume"];
          localVolume = data["volume"];
        });
      }

      c.complete(data);
    });

    await c.future;
    setState(() {
      isLoading = false;
    });
  }

  void onVolumeValueChange(double value) {
    setState(() {
      localVolume = value.toInt();

      // To not spam the server, use a debounce for changing volume
      volumeDebounce?.cancel();
      volumeDebounce = Timer(const Duration(milliseconds: 500), updateVolume);
    });
  }

  Future<void> togglePlayback() async {
    setState(() {
      isChangingPlaybackState = true;
    });
    var socket = ref.read(socketClientProvider);

    Completer c = Completer();

    socket.emitWithAck("playback/toggle", {}, ack: (data) {
      bool isSuccess = processSocketRepsonse(context, data);

      c.complete(isSuccess);
    });

    await c.future;

    setState(() {
      isChangingPlaybackState = false;
      isPlaying = !isPlaying;
    });
  }

  Future<void> updateVolume() async {
    var socket = ref.read(socketClientProvider);

    socket.emitWithAck("playback/volume", {'volume': localVolume}, ack: (data) {
      processSocketRepsonse(context, data);

      setState(() {
        currentVolume = localVolume;
      });
    });
  }

  @override
  void initState() {
    super.initState();

    getCurrentState();
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return Dialog(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const Padding(
                padding: EdgeInsets.all(12.0),
                child: CircularProgressIndicator(),
              ),
              Text(t.loading, style: const TextStyle(fontSize: 24))
            ],
          ),
        ),
      );
    }
    return WillPopScope(
      onWillPop: () async {
        if (localVolume != currentVolume) {
          await updateVolume();
        }
        return true;
      },
      child: Dialog(
        child: Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.music_note, size: 24),
                    Text(t.control.control_dialog.playback,
                        style: const TextStyle(fontSize: 16)),
                  ],
                ),
                IconButton(
                    onPressed: isLoading && !isChangingPlaybackState
                        ? null
                        : togglePlayback,
                    icon: Icon(isPlaying ? Icons.pause : Icons.play_arrow,
                        size: 48)),
                const SizedBox(height: 40),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.volume_down, size: 24),
                    Text(t.control.control_dialog.volume,
                        style: const TextStyle(fontSize: 16)),
                  ],
                ),
                Slider(
                  value: localVolume.toDouble(),
                  min: 0,
                  max: 100,
                  activeColor: isLoading ? Colors.grey : Colors.blue,
                  onChanged: onVolumeValueChange,
                ),
                Text(
                  '$localVolume%',
                  style: const TextStyle(fontSize: 20),
                ),
              ],
            )),
      ),
    );
  }

  @override
  void dispose() {
    volumeDebounce?.cancel();

    super.dispose();
  }
}
