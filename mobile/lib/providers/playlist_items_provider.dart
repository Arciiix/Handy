import 'package:hooks_riverpod/hooks_riverpod.dart';

import '../types/playlist.dart';

final playlistItemsProvider = StateProvider<Playlists>((ref) {
  // This is later updated within the socket client provider
  return Playlists(
      items: [], currentLocalIndex: null, currentYouTubeIndex: null);
});
