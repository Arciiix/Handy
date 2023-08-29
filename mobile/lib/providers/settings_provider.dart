import 'package:handy/providers/shared_preferences_provider.dart';
import 'package:handy/types/settings.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

final settingsProvider = StateProvider<Settings>((ref) {
  final sharedPreferences = ref.watch(sharedPreferencesProvider);

  final handyServerIP = sharedPreferences.getString("HANDY_SERVER_IP") ??
      "http://192.168.0.105:4001";

  ref.listenSelf((previous, next) {
    // Listens for value changes - when user changes settings
    print("Settings are being saved...");
    sharedPreferences.setString(
        "HANDY_SERVER_IP", next.handyServerIP.toString());
  });

  return Settings(handyServerIP: Uri.parse(handyServerIP));
});
