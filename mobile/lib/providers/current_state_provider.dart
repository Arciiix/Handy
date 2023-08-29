import 'package:handy/types/state.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

final currentStateProvider = StateProvider<CurrentState>((ref) {
  // TODO
  return CurrentState(isConnected: true, isEnabled: false);
});
