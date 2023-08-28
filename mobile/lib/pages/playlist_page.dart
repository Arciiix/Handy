import "package:flutter/material.dart";
import "package:handy/components/playlist/playlist_items_management.dart";
import "package:handy/gen/strings.g.dart";
import "package:handy/types/playlist.dart";

class PlaylistPage extends StatefulWidget {
  const PlaylistPage({super.key});

  @override
  State<PlaylistPage> createState() => _PlaylistPageState();
}

class _PlaylistPageState extends State<PlaylistPage> {
  final tabs = [
    Tab(
        icon: const Icon(Icons.perm_media_outlined),
        text: t.playlist.media.local),
    Tab(
        icon: const Icon(Icons.open_in_new_outlined),
        text: t.playlist.media.youtube),
  ];

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
        length: tabs.length,
        child: Scaffold(
            body: Column(
          children: [
            TabBar(tabs: tabs),
            const Expanded(
                child: TabBarView(children: [
              PlaylistItemsManagement(type: PlaylistType.local),
              PlaylistItemsManagement(type: PlaylistType.youtube),
            ])),
          ],
        )));
  }
}
