import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:handy/gen/strings.g.dart';
import 'package:handy/providers/socket_provider.dart';
import 'package:handy/utils/process_socket_response.dart';
import 'package:handy/utils/time_ago.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

class PreviewPage extends ConsumerStatefulWidget {
  const PreviewPage({super.key});

  @override
  PreviewPageState createState() => PreviewPageState();
}

class PreviewPageState extends ConsumerState<PreviewPage> {
  DateTime dateUpdated = DateTime.now();
  Uint8List? image;

  String timeAgo = "";

  late Timer _imageUpdateTimer;
  late Timer _timeUpdateTimer;

  void refreshImage() {
    ref.read(socketClientProvider).emitWithAck("handy/preview", {},
        ack: (data) {
      bool isSuccess = processSocketRepsonse(context, data);
      setState(() {
        dateUpdated = DateTime.tryParse(data["changed_at"]) ?? DateTime.now();
        image = isSuccess && data?["preview"] != null
            ? base64Decode(data["preview"])
            : null;
      });
    });
  }

  @override
  void initState() {
    super.initState();

    _imageUpdateTimer = Timer.periodic(
      const Duration(seconds: 2),
      (timer) {
        // If for some reason the last image update was longer than a minute ago
        if (DateTime.now().difference(dateUpdated).inSeconds >= 60) return;

        refreshImage();
      },
    );

    _timeUpdateTimer = Timer.periodic(
      const Duration(seconds: 1),
      (timer) {
        setState(() {
          timeAgo = convertToAgo(dateUpdated);
        });
      },
    );

    refreshImage();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text(t.preview.title), actions: [
          IconButton(onPressed: refreshImage, icon: const Icon(Icons.refresh))
        ]),
        body: SingleChildScrollView(
          scrollDirection: Axis.vertical,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Chip(
                    label: Text(t.preview.last_updated(time_ago: timeAgo))),
              ),
              if (image != null)
                Image.memory(
                  image!,
                  fit: BoxFit.cover,
                )
            ],
          ),
        ));
  }

  @override
  void dispose() {
    super.dispose();

    _timeUpdateTimer.cancel();
    _imageUpdateTimer.cancel();
  }
}
