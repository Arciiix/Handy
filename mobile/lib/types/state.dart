class CurrentState {
  bool isConnected;
  bool isEnabled;

  CurrentState({required this.isConnected, required this.isEnabled});

  Future<CurrentState> toggleControl() async {
    // TODO DEV
    return CurrentState(isConnected: true, isEnabled: !isEnabled);
  }
}
