import "package:flutter/material.dart";
import "package:go_router/go_router.dart";
import "package:handy/gen/strings.g.dart";
import "package:handy/providers/current_state_provider.dart";
import "package:hooks_riverpod/hooks_riverpod.dart";

class BottomNavigation extends ConsumerStatefulWidget {
  const BottomNavigation({
    required this.navigationShell,
    Key? key,
  }) : super(key: key ?? const ValueKey<String>('BottomNavigation'));

  final StatefulNavigationShell navigationShell;

  @override
  BottomNavigationState createState() => BottomNavigationState();
}

class BottomNavigationState extends ConsumerState<BottomNavigation> {
  void onPageChange(int index) {
    // If user wants to go to managing playlists and the socket.io connection hasn't been established, deny it and show an alert
    if (index == 1 && !ref.read(currentStateProvider).isConnected) {
      showDialog(
          context: context,
          builder: (context) => AlertDialog(
                title: Text(t.playlist.not_connected_dialog.title),
                content: Text(t.playlist.not_connected_dialog.description),
                actions: [
                  TextButton(
                    child: Text(t.buttons.ok),
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                  ),
                ],
              ));
      return;
    }

    widget.navigationShell.goBranch(index);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(child: widget.navigationShell),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: widget.navigationShell.currentIndex,
        onTap: onPageChange,
        items: [
          BottomNavigationBarItem(
              icon: const Icon(Icons.home), label: t.navigation.home),
          BottomNavigationBarItem(
              icon: const Icon(Icons.music_note), label: t.navigation.playlist),
          BottomNavigationBarItem(
              icon: const Icon(Icons.settings), label: t.navigation.settings)
        ],
      ),
    );
  }
}
