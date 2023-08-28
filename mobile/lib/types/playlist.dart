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

  Future<Playlists> addItem(PlaylistItem item) async {
    // TODO: Do the server-side work

    var newItems = [...items, item];

    return Playlists(items: newItems);
  }

  Future<Playlists> updateItem(PlaylistItem item) async {
    // First find if id exists
    int index = items.indexWhere((e) => e.id == item.id);

// TODO: Do the server-side work

    if (index == -1) {
      // TODO: Handle error

      // Return the current playlist
      return Playlists(items: items);
    }

    var newItems = [...items];
    newItems[index] = item;

    return Playlists(items: newItems);
  }

  Future<Playlists> removeItem(String id) async {
    // TODO: Do the server-side work

    return Playlists(
        items: items.where((element) => element.id != id).toList());
  }

  Playlists({required this.items});
}
