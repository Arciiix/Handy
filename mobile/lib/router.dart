import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:handy/components/bottom_navigation.dart';
import 'package:handy/pages/home_page.dart';
import 'package:handy/pages/playlist_page.dart';
import 'package:handy/pages/settings_page.dart';

final router = GoRouter(
  initialLocation: "/",
  routes: [
    StatefulShellRoute.indexedStack(
      builder: (BuildContext context, GoRouterState state,
          StatefulNavigationShell navigationShell) {
        return BottomNavigation(
          navigationShell: navigationShell,
        );
      },
      branches: <StatefulShellBranch>[
        StatefulShellBranch(
          routes: <RouteBase>[
            GoRoute(
                path: '/',
                builder: (BuildContext context, GoRouterState state) {
                  return const HomePage();
                }),
          ],
        ),
        StatefulShellBranch(
          routes: <RouteBase>[
            GoRoute(
                path: '/playlist',
                builder: (BuildContext context, GoRouterState state) {
                  return const PlaylistPage();
                }),
          ],
        ),
        StatefulShellBranch(routes: [
          GoRoute(
            path: '/settings',
            builder: (BuildContext context, GoRouterState state) {
              return const SettingsPage();
            },
          ),
        ])
      ],
    ),
  ],
);
