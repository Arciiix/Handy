import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../types/playlist.dart';

final playlistItemsProvider = StateProvider<Playlists>((ref) {
  // This is later updated within the socket client provider
  return Playlists(
      items: [],
      currentLocalIndex: null,
      currentYouTubeIndex: null,
      currentType: PlaylistType.local);
});
