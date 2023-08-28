import "package:flutter/material.dart";
import "package:go_router/go_router.dart";
import "package:handy/gen/strings.g.dart";

class BottomNavigation extends StatelessWidget {
  const BottomNavigation({
    required this.navigationShell,
    Key? key,
  }) : super(key: key ?? const ValueKey<String>('BottomNavigation'));

  final StatefulNavigationShell navigationShell;

  void onPageChange(int index) {
    navigationShell.goBranch(index);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(child: navigationShell),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: navigationShell.currentIndex,
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
