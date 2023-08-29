import 'package:handy/types/state.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

final currentStateProvider = StateProvider<CurrentState>((ref) {
  return CurrentState(
      isConnected: false, isConnecting: false, isEnabled: false);
});
