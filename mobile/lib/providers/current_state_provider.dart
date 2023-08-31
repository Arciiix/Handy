import 'package:handy/types/state.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

final currentStateProvider = StateProvider<CurrentState>((ref) {
  return CurrentState(
      isConnected: false, isConnecting: false, isEnabled: false);
});
