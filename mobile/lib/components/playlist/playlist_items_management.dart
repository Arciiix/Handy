import "dart:async";

import "package:flutter/material.dart";
import "package:go_router/go_router.dart";
import "package:handy/components/loading_dialog/loading_dialog.dart";
import "package:handy/gen/strings.g.dart";
import "package:handy/providers/playlist_items_provider.dart";
import "package:handy/providers/socket_provider.dart";
import "package:handy/types/playlist.dart";
import "package:handy/utils/process_socket_response.dart";
import "package:hooks_riverpod/hooks_riverpod.dart";

class PlaylistItemsManagement extends ConsumerStatefulWidget {
  final PlaylistType type;

  const PlaylistItemsManagement({super.key, required this.type});

  @override
  PlaylistItemsManagementState createState() => PlaylistItemsManagementState();
}

class PlaylistItemsManagementState
    extends ConsumerState<PlaylistItemsManagement> {
  void deleteItem(String id, String name) async {
    bool? response = await showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(t.dialog.delete_item.title),
          content: SingleChildScrollView(
            child: ListBody(
              children: <Widget>[
                Text(t.dialog.delete_item.description(item_name: name)),
              ],
            ),
          ),
          actions: <Widget>[
            TextButton(
              child: Text(t.buttons.cancel),
              onPressed: () {
                Navigator.of(context).pop(false);
              },
            ),
            TextButton(
              child: Text(t.buttons.delete),
              onPressed: () {
                Navigator.of(context).pop(true);
              },
            ),
          ],
        );
      },
    );

    if (response == true && mounted) {
      await showLoadingDialog(context, () async {
        ref.read(playlistItemsProvider.notifier).state =
            await ref.read(playlistItemsProvider).removeItem(id);
      });
    }
  }

  void handleAdd() {
    context.push("/playlist_item/${widget.type.index}/add");
  }

  void playItem(PlaylistItem item, int index) async {
    var socket = ref.read(socketClientProvider);

    Completer c = Completer();
    socket.emitWithAck("playlist_item/play", {'id': item.id}, ack: (data) {
      bool isSuccess = processSocketRepsonse(context, data);

      c.complete(isSuccess);
    });

    showLoadingDialog(context, () async {
      var success = await c.future;

      if (success) {
        ref.read(playlistItemsProvider.notifier).state = ref
            .read(playlistItemsProvider)
            .copyWith(
              currentType: item.type,
              // It will update either local or youtube index, based on the type
              currentLocalIndex: item.type == PlaylistType.local ? index : null,
              currentYouTubeIndex:
                  item.type == PlaylistType.youtube ? index : null,
            );
        setState(() {});
      }
    });
  }

  void changePlaylistType() {
    var socket = ref.read(socketClientProvider);

    Completer c = Completer();
    socket.emitWithAck("playlist/switch_type", {}, ack: (data) {
      bool isSuccess = processSocketRepsonse(context, data);

      c.complete(isSuccess ? data["mode"] : null);
    });

    showLoadingDialog(context, () async {
      var mode = await c.future;

      if (mode != null) {
        ref.read(playlistItemsProvider.notifier).state =
            ref.read(playlistItemsProvider).copyWith(
                    currentType: PlaylistType.values.firstWhere(
                  (enumValue) =>
                      enumValue.name == (mode as String).toLowerCase(),
                  orElse: () => PlaylistType.values[0],
                ));
      }
      setState(() {});
    });
  }

  @override
  Widget build(BuildContext context) {
    Playlists playlists = ref.watch(playlistItemsProvider);

    List<PlaylistItem> playlistItems = playlists.getForType(widget.type);

    return Scaffold(
      floatingActionButton: FloatingActionButton(
          onPressed: handleAdd, child: const Icon(Icons.add)),
      body: Column(
        children: [
          Expanded(
            child: ReorderableListView.builder(
              itemBuilder: (context, index) {
                PlaylistItem item = playlistItems[index];
                bool isSelected = index ==
                    (widget.type == PlaylistType.local
                        ? playlists.currentLocalIndex
                        : playlists.currentYouTubeIndex);
                return ListTile(
                  key: Key('${index}_${item.id}'),
                  title: Text(item.name),
                  subtitle: Text(item.url.toString()),
                  leading: const Icon(Icons.reorder),
                  selected: isSelected,
                  trailing: IconButton(
                      icon: const Icon(Icons.delete),
                      onPressed: () => deleteItem(item.id, item.name)),
                  onTap: () {
                    context.push(
                        "/playlist_item/${widget.type.index}/edit/${item.id}");
                  },
                  onLongPress: () => playItem(item, index),
                );
              },
              itemCount: playlistItems.length,
              onReorder: (oldIndex, newIndex) {
                print("reorder");
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Chip(
              onDeleted: changePlaylistType,
              deleteIcon: const Icon(Icons.cameraswitch),
              label: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(t.playlist.current_type.current_type_is),
                  Text(
                      t.playlist.media(
                          context: PlaylistTypesContext
                              .values[playlists.currentType.index]),
                      style: const TextStyle(fontWeight: FontWeight.bold)),
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
