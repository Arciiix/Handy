import 'dart:async';

import 'package:flutter/material.dart';
import 'package:handy/utils/process_socket_response.dart';
import 'package:socket_io_client/socket_io_client.dart';

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

  Future<CurrentState> toggleControl(
      BuildContext context, Socket socket) async {
    Completer c = Completer();
    socket.emitWithAck("handy/change_status", {"isEnabled": !isEnabled},
        ack: (data) {
      bool isSuccess = processSocketRepsonse(context, data);
      print("Change status - success: {isSuccess}");
      c.complete(isSuccess);
    });

    await c.future;

    return copyWith(isEnabled: !isEnabled);
  }
}
