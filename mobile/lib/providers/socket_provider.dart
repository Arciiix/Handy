import 'dart:async';

import 'package:handy/providers/current_state_provider.dart';
import 'package:handy/providers/playlist_items_provider.dart';
import 'package:handy/providers/settings_provider.dart';
import 'package:handy/types/playlist.dart';
import 'package:handy/types/state.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:socket_io_client/socket_io_client.dart';

final socketClientProvider = Provider<Socket>((ref) {
  print("Socket init");

  // Read the current URL from the settings

  // Important: Not .watch because I want to update the socket manually (by calling .refresh on provider).
  // If you use .watch(), it will throw an error "Cannot use ref functions after the dependency of a provider changed but before the provider rebuilt" if you change the settings
  // That's because the settingsProvider changes, but you try to access ref.read in socket.onDisconnect in this provider (after the settings changed)
  var settings = ref.read(settingsProvider);

  var url = settings.handyServerIP.toString();

  var socket = io(url, <String, dynamic>{
    'transports': ['websocket'],
  });

  socket.onConnect((data) {
    print("Connected to the socket.io server!");

    // Get the current state
    getCurrentInfo(socket).future.then((e) {
      ref.read(currentStateProvider.notifier).state = CurrentState(
          isConnecting: false,
          isConnected: true,
          isEnabled: e["isEnabled"],
          isInsideWorkingHours: e["inWorkingHours"]);

      ref.read(playlistItemsProvider.notifier).state = Playlists.fromJson(e);
    });

    ref.read(currentStateProvider.notifier).state =
        ref.read(currentStateProvider).copyWith(isConnecting: true);
  });

  socket.onDisconnect((data) {
    ref.read(currentStateProvider.notifier).state =
        ref.read(currentStateProvider).copyWith(isConnected: false);
  });

  socket.on("current_state", (data) {});

  // Automatically disconnect when the provider is disposed

  ref.onDispose(() {
    socket.disconnect();
    socket.dispose();
    ref.read(currentStateProvider.notifier).state =
        ref.read(currentStateProvider).copyWith(isConnected: false);
    print("Socket disposed!");
  });

  return socket;
});

Completer getCurrentInfo(Socket socket) {
  Completer c = Completer();

  socket.emitWithAck("handy/info", {}, ack: (e) {
    print("Got info from server!");

    c.complete(e);
  });
  return c;
}
