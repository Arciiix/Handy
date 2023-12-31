import "dart:async";

import "package:flutter/material.dart";
import "package:flutter/services.dart";
import "package:go_router/go_router.dart";
import "package:handy/components/control/control.dart";
import "package:handy/providers/socket_provider.dart";
import "package:handy/types/playlist.dart";
import 'package:flutter_riverpod/flutter_riverpod.dart';

class HomePage extends ConsumerStatefulWidget {
  const HomePage({super.key});

  @override
  HomePageState createState() => HomePageState();
}

class HomePageState extends ConsumerState<HomePage>
    with WidgetsBindingObserver {
  static const platform = MethodChannel('app.channel.shared.data');

  Future<void> getSharedData() async {
    String? sharedData = await platform.invokeMethod('getSharedText');
    if (sharedData != null) {
      print("Received a sharing intent: $sharedData");
      PlaylistType type = PlaylistType.local;

      if (sharedData.contains("youtube.com")) {
        type = PlaylistType.youtube;
      }

      if (mounted) {
        context.go(
            "/playlist_item/${type.index}/add?url=$sharedData&closeAppOnSave=1");
      }
    } else {
      print("Didn't receive any sharing intent!");
    }
  }

  @override
  void initState() {
    super.initState();
    // Add this widget as an observer to detect app lifecycle changes
    WidgetsBinding.instance.addObserver(this);

    ref.read(socketClientProvider);

    getSharedData();
  }

  @override
  void dispose() {
    // Remove this widget as an observer when it's no longer needed
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    super.didChangeAppLifecycleState(state);

    if (state == AppLifecycleState.resumed) {
      getSharedData();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Focus(
      onFocusChange: (hasFocus) {
        if (hasFocus) getSharedData();
      },
      child: const SafeArea(child: Control()),
    );
  }
}
