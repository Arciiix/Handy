import 'package:hooks_riverpod/hooks_riverpod.dart';

import '../types/playlist.dart';

final playlistItemsProvider = StateProvider<Playlists>((ref) {
  // TODO: Get from the Handy server itself
  // DEV
  final items = [
    PlaylistItem(
        id: "test",
        type: PlaylistType.local,
        name: "test1",
        pronunciation: "test-1",
        url: Uri.parse("google.com")),
    PlaylistItem(
        id: "test2",
        type: PlaylistType.local,
        name: "test2",
        pronunciation: "test-2",
        url: Uri.parse("google.com")),
    PlaylistItem(
        id: "yttest",
        type: PlaylistType.youtube,
        name: "YouTube test",
        pronunciation: "you-tube test",
        url: Uri.parse("https://www.youtube.com/watch?v=dQw4w9WgXcQ")),
  ];

  return Playlists(items: items);
});
