enum PlaylistType { local, youtube }

class PlaylistItem {
  String id;
  PlaylistType type;
  String name;
  String? pronunciation;
  Uri url;

  PlaylistItem(
      {required this.id,
      required this.type,
      required this.name,
      required this.pronunciation,
      required this.url});
}

class Playlists {
  List<PlaylistItem> items;

  int? currentLocalIndex;
  int? currentYouTubeIndex;

  List<PlaylistItem> get local {
    return items
        .where((element) => element.type == PlaylistType.local)
        .toList();
  }

  List<PlaylistItem> get youtube {
    return items
        .where((element) => element.type == PlaylistType.youtube)
        .toList();
  }

  List<PlaylistItem> getForType(PlaylistType type) {
    switch (type) {
      case PlaylistType.local:
        return local;
      case PlaylistType.youtube:
        return youtube;
    }
  }

  Future<Playlists> addItem(PlaylistItem item) async {
    // TODO: Do the server-side work

    //  TODO: The id here should be obtained from the request
    var newItems = [...items, item];

    return copyWith(items: newItems);
  }

  Future<Playlists> updateItem(PlaylistItem item) async {
    // First find if id exists
    int index = items.indexWhere((e) => e.id == item.id);

// TODO: Do the server-side work

    if (index == -1) {
      // TODO: Handle error

      // Return the current playlist
      return copyWith(items: items);
    }

    var newItems = [...items];
    newItems[index] = item;

    return copyWith(items: newItems);
  }

  Future<Playlists> removeItem(String id) async {
    // TODO: Do the server-side work

    return copyWith(items: items.where((element) => element.id != id).toList());
  }

  Playlists copyWith(
      {List<PlaylistItem>? items,
      int? currentLocalIndex,
      int? currentYouTubeIndex}) {
    return Playlists(
        items: items ?? this.items,
        currentLocalIndex: currentLocalIndex ?? this.currentLocalIndex,
        currentYouTubeIndex: currentYouTubeIndex ?? this.currentYouTubeIndex);
  }

  Playlists(
      {required this.items,
      required this.currentLocalIndex,
      required this.currentYouTubeIndex});
}
