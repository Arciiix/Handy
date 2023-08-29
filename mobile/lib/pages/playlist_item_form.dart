import "dart:async";
import "package:flutter/material.dart";
import "package:go_router/go_router.dart";
import "package:handy/components/loading_dialog/loading_dialog.dart";
import "package:handy/gen/strings.g.dart";
import "package:handy/providers/playlist_items_provider.dart";
import "package:handy/providers/socket_provider.dart";
import "package:handy/types/playlist.dart";
import "package:handy/utils/validation.dart";
import "package:hooks_riverpod/hooks_riverpod.dart";
import "package:url_launcher/url_launcher.dart";

import "../utils/process_socket_response.dart";

class PlaylistItemForm extends ConsumerStatefulWidget {
  final String? id;
  final String? overrideURL;

  final PlaylistType type;

  const PlaylistItemForm(
      {super.key, this.id, required this.type, this.overrideURL});

  @override
  PlaylistItemFormState createState() => PlaylistItemFormState();
}

class PlaylistItemFormState extends ConsumerState<PlaylistItemForm> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  TextEditingController nameController = TextEditingController();
  TextEditingController pronunciationController = TextEditingController();
  TextEditingController urlController = TextEditingController();

  bool customPronunciation = false;

  void _launchURL() async {
    Uri? url = Uri.tryParse(urlController.text);
    if (url == null || !validateURL(urlController.text)) {
      return;
    }

    await launchUrl(url);
  }

  void handleSave() async {
    // First, if it's a YouTube item, verify whether the audio URL can be retrieved
    if (widget.type == PlaylistType.youtube) {
      var socket = ref.read(socketClientProvider);

      Completer c = Completer();
      socket.emitWithAck("youtube/check", {"url": urlController.text},
          ack: (data) {
        bool isSuccess = processSocketRepsonse(context, data);

        c.complete(isSuccess);
      });

      Completer c2 = Completer();

      showLoadingDialog(context, () async {
        var data = await c.future;
        c2.complete(data);
      });

      bool isRetrievable = await c2.future;

      // Wait a bit for the dialog to close
      await Future.delayed(const Duration(seconds: 2));

      if (!isRetrievable) {
        if (mounted) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            showDialog(
              context: context,
              builder: (context) => AlertDialog(
                title: Text(t.playlist.youtube.irretrievable.title),
                content: Text(t.playlist.youtube.irretrievable.description),
                actions: <Widget>[
                  ElevatedButton(
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                    child: Text(t.buttons.ok),
                  ),
                ],
              ),
            );
          });
        }
        return;
      }
    }

    // Create the playlist item object
    PlaylistItem playlist = PlaylistItem(
        id: widget.id ?? "",
        type: widget.type,
        name: nameController.text,
        pronunciation:
            customPronunciation ? pronunciationController.text : null,
        url: Uri.parse(urlController.text));

    // Edit if the id has been provided, otherwise add a new playlist item
    Playlists playlists = ref.read(playlistItemsProvider);

    if (widget.id != null) {
      // Create a new playlist item
      ref.read(playlistItemsProvider.notifier).state =
          await playlists.updateItem(playlist);
    } else {
      ref.read(playlistItemsProvider.notifier).state =
          await playlists.addItem(playlist);
    }
    if (mounted) context.pop();
  }

  Future<void> fetchYouTubeData() async {
    if (urlController.text == "" || !validateURL(urlController.text)) return;

    var socket = ref.read(socketClientProvider);

    Completer c = Completer();
    socket.emitWithAck("youtube/info", {"url": urlController.text},
        ack: (data) {
      bool isSuccess = processSocketRepsonse(context, data);

      c.complete(isSuccess ? data : null);
    });

    showLoadingDialog(context, () async {
      var data = await c.future;

      if (data != null) {
        setState(() {
          nameController.text = data?["title"] ?? "Unknown";
        });
      }
    });
  }

  @override
  void initState() {
    super.initState();

    if (widget.id != null) {
      // Find the already existing item and if so, then set the input values
      var playlists = ref.read(playlistItemsProvider);

      var items = playlists.getForType(widget.type);
      PlaylistItem previousItem =
          items.firstWhere((element) => element.id == widget.id);

      nameController.text = previousItem.name;
      pronunciationController.text =
          previousItem.pronunciation ?? previousItem.name;
      customPronunciation = previousItem.pronunciation != null &&
          previousItem.pronunciation != previousItem.name;
      urlController.text = previousItem.url.toString();
    }

    if (widget.overrideURL != null) {
      urlController.text = widget.overrideURL!;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          title: Text(widget.id != null
              ? t.playlist.form.title_edit(
                  context: PlaylistTypesContext.values[widget.type.index])
              : t.playlist.form.title_add(
                  context: PlaylistTypesContext.values[widget.type.index]))),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.save),
        onPressed: () {
          if (_formKey.currentState?.validate() == true) {
            handleSave();
          }
        },
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            if (widget.type == PlaylistType.youtube)
              Card(
                  child: Padding(
                padding: const EdgeInsets.all(12.0),
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: Icon(Icons.info_outline, size: 32),
                        ),
                        Text(t.playlist.youtube.advice.title,
                            style: const TextStyle(fontSize: 32))
                      ],
                    ),
                    Text(t.playlist.youtube.advice.description)
                  ],
                ),
              )),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Form(
                key: _formKey,
                child: Column(
                  children: <Widget>[
                    TextFormField(
                      controller: nameController,
                      decoration: InputDecoration(
                          labelText: t.playlist.form.fields.name),
                      validator: (value) {
                        if (value?.isNotEmpty != true) {
                          return t.playlist.form.errors.name_empty;
                        }
                        return null;
                      },
                    ),
                    Padding(
                      padding: const EdgeInsets.symmetric(vertical: 12),
                      child: Column(
                        children: [
                          Row(
                            mainAxisSize: MainAxisSize.max,
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: <Widget>[
                              Text(t.playlist.form.fields.custom_pronunciation),
                              Switch(
                                value: customPronunciation,
                                onChanged: (value) {
                                  setState(() {
                                    customPronunciation = value;
                                    // Clear the pronunciation field when switching off
                                    if (!customPronunciation) {
                                      pronunciationController.clear();
                                    } else {
                                      // Set the pronunciation field to the name when switching on
                                      pronunciationController.text =
                                          nameController.text;
                                    }
                                  });
                                },
                              ),
                            ],
                          ),
                          if (customPronunciation)
                            TextFormField(
                              controller: pronunciationController,
                              decoration: InputDecoration(
                                  labelText:
                                      t.playlist.form.fields.pronunciation),
                            ),
                        ],
                      ),
                    ),
                    TextFormField(
                      controller: urlController,
                      decoration: InputDecoration(
                        labelText: t.playlist.form.fields.url,
                        helperText: t.playlist.form.fields.url_helper,
                      ),
                      validator: (value) {
                        if (!validateURL(value)) {
                          return t.playlist.form.errors.url_invalid;
                        }
                        return null;
                      },
                    ),
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: OutlinedButton.icon(
                          onPressed: _launchURL,
                          icon: const Icon(Icons.play_arrow),
                          label: Text(t.playlist.open_url)),
                    ),
                    if (widget.type == PlaylistType.youtube)
                      OutlinedButton.icon(
                          onPressed: fetchYouTubeData,
                          icon: const Icon(Icons.auto_fix_high),
                          label: Text(t.playlist.youtube.fetch_data))
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    // Clean up the controllers when the widget is disposed
    nameController.dispose();
    pronunciationController.dispose();
    urlController.dispose();
    super.dispose();
  }
}
