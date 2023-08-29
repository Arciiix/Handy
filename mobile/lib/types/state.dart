class CurrentState {
  bool isConnected;
  bool?
      isConnecting; // Connected to the socket server and now waiting for response
  bool isEnabled;
  bool? isInsideWorkingHours;

  CurrentState({
    required this.isConnected,
    required this.isEnabled,
    this.isConnecting,
    this.isInsideWorkingHours,
  });

  CurrentState copyWith(
      {bool? isConnected,
      bool? isConnecting,
      bool? isEnabled,
      bool? isInsideWorkingHours}) {
    return CurrentState(
        isConnected: isConnected ?? this.isConnected,
        isConnecting: isConnecting ?? this.isConnecting,
        isEnabled: isEnabled ?? this.isEnabled,
        isInsideWorkingHours:
            isInsideWorkingHours ?? this.isInsideWorkingHours);
  }

  Future<CurrentState> toggleControl() async {
    // TODO DEV
    return copyWith(isEnabled: !isEnabled);
  }
}
