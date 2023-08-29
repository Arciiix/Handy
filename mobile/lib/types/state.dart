class CurrentState {
  bool isConnected;
  bool isEnabled;

  CurrentState({required this.isConnected, required this.isEnabled});

  CurrentState copyWith({bool? isConnected, bool? isEnabled}) {
    return CurrentState(
        isConnected: isConnected ?? this.isConnected,
        isEnabled: isEnabled ?? this.isEnabled);
  }

  Future<CurrentState> toggleControl() async {
    // TODO DEV
    return copyWith(isEnabled: !isEnabled);
  }
}
