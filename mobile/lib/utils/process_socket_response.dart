import 'package:flutter/material.dart';
import 'package:handy/gen/strings.g.dart';

bool processSocketRepsonse(BuildContext context, dynamic response) {
  // A function to show an error in case socket operation fails
  if (response?["success"] != true) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(t.error.socket(error: response?["error"] ?? "?"))));
    return false;
  } else {
    return true;
  }
}
