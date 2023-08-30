import 'dart:async';

import 'package:flutter/material.dart';
import 'package:handy/types/result.dart';
import 'package:socket_io_client/socket_io_client.dart';

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

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'type': type.name.toUpperCase(),
      'name': name,
      'pronunciation': pronunciation,
      'url': url.toString()
    };
  }
}

class Playlists {
  List<PlaylistItem> items;

  int? currentLocalIndex;
  int? currentYouTubeIndex;

  PlaylistType currentType;

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

  Future<Result<Playlists>> addItem(PlaylistItem item, Socket socket) async {
    Completer c = Completer();
    socket.emitWithAck("playlist_item/add",
        item.toJson()..removeWhere((key, value) => key == "id"), ack: (data) {
      c.complete(data);
    });

    var response = await c.future;

    if (response?["success"] && response?["playlistItem"] != null) {
      var newItems = [...items, item..id = response["playlistItem"]["id"]];
      return Result(data: copyWith(items: newItems));
    } else {
      return Result(data: this, error: response?["error"] ?? "unknown");
    }
  }

  Future<Result<Playlists>> updateItem(PlaylistItem item, Socket socket) async {
    // First find if id exists
    int index = items.indexWhere((e) => e.id == item.id);

    if (index == -1) {
      // Return the current playlist
      return Result(data: this, error: "not exists");
    }

    Completer c = Completer();
    socket.emitWithAck("playlist_item/edit", item.toJson(), ack: (data) {
      c.complete(data);
    });

    var response = await c.future;

    if (response?["success"] && response?["playlistItem"] != null) {
      var newItems = [...items];
      newItems[index] = item;

      return Result(data: copyWith(items: newItems));
    } else {
      return Result(data: this, error: response?["error"] ?? "unknown");
    }
  }

  Future<Result<Playlists>> removeItem(String id, Socket socket) async {
    Completer c = Completer();
    socket.emitWithAck("playlist_item/delete", {"id": id}, ack: (data) {
      c.complete(data);
    });

    var response = await c.future;

    if (response?["success"]) {
      return Result(
          data: copyWith(
              items: items.where((element) => element.id != id).toList()));
    } else {
      return Result(data: this, error: response?["error"] ?? "unknown");
    }
  }

  Playlists copyWith(
      {List<PlaylistItem>? items,
      int? currentLocalIndex,
      int? currentYouTubeIndex,
      PlaylistType? currentType}) {
    return Playlists(
        items: items ?? this.items,
        currentLocalIndex: currentLocalIndex ?? this.currentLocalIndex,
        currentYouTubeIndex: currentYouTubeIndex ?? this.currentYouTubeIndex,
        currentType: currentType ?? this.currentType);
  }

  Playlists(
      {required this.items,
      required this.currentLocalIndex,
      required this.currentYouTubeIndex,
      required this.currentType});
}
