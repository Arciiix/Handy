import "package:flutter/material.dart";
import "package:handy/components/loading_dialog/loading_dialog.dart";
import "package:handy/providers/playlist_items_provider.dart";
import "package:handy/types/playlist.dart";
import "package:hooks_riverpod/hooks_riverpod.dart";

class PlaylistItemsManagement extends ConsumerStatefulWidget {
  final PlaylistType type;

  const PlaylistItemsManagement({super.key, required this.type});

  @override
  PlaylistItemsManagementState createState() => PlaylistItemsManagementState();
}

class PlaylistItemsManagementState
    extends ConsumerState<PlaylistItemsManagement> {
  @override
  Widget build(BuildContext context) {
    Playlists playlists = ref.watch(playlistItemsProvider);

    List<PlaylistItem> playlistItems;
    switch (widget.type) {
      case PlaylistType.local:
        playlistItems = playlists.local;
        break;
      case PlaylistType.youtube:
        playlistItems = playlists.youtube;
        break;
    }

    void deleteItem(String id) async {
      await showLoadingDialog(context, () async {
        ref.read(playlistItemsProvider.notifier).state =
            await playlists.removeItem(id);
      });
    }

    return ReorderableListView.builder(
      itemBuilder: (context, index) {
        PlaylistItem item = playlistItems[index];

        return ListTile(
          key: Key('${index}_${item.id}'),
          title: Text(item.name),
          subtitle: Text(item.url.toString()),
          leading: const Icon(Icons.reorder),
          trailing: IconButton(
              icon: const Icon(Icons.delete),
              onPressed: () => deleteItem(item.id)),
        );
      },
      itemCount: playlistItems.length,
      onReorder: (oldIndex, newIndex) {
        print("reorder");
      },
    );
  }
}
