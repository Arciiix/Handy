class Settings {
  Uri handyServerIP;

  Settings({required this.handyServerIP});

  Settings copyWith({Uri? handyServerIP}) {
    return Settings(handyServerIP: handyServerIP ?? this.handyServerIP);
  }
}
