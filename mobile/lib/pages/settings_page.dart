import 'package:flutter/material.dart';
import 'package:handy/components/input_dialog.dart';
import 'package:handy/gen/strings.g.dart';
import 'package:handy/providers/settings_provider.dart';
import 'package:handy/providers/socket_provider.dart';
import 'package:handy/utils/validation.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

class SettingsPage extends ConsumerStatefulWidget {
  const SettingsPage({super.key});

  @override
  SettingsPageState createState() => SettingsPageState();
}

class SettingsPageState extends ConsumerState<SettingsPage> {
  String serverUrl = '';

  @override
  Widget build(BuildContext context) {
    final settings = ref.watch(settingsProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text(t.settings.title),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(8),
              children: [
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    t.settings.sections.general,
                    style: const TextStyle(
                        fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                ),
                ListTile(
                    leading: const Icon(Icons.public),
                    title: Text(t.settings.ip.title),
                    subtitle: Text(t.settings.ip.description),
                    onTap: () async {
                      String? output = await showDialog(
                        context: context,
                        builder: (BuildContext context) {
                          return InputDialog(
                              title: t.settings.ip.title,
                              initialValue: settings.handyServerIP.toString(),
                              validator: validateURL,
                              errorMessage: "Invalid URL",
                              helperText: "Start with e.g. http://");
                        },
                      );

                      if (output != null) {
                        WidgetsBinding.instance.addPostFrameCallback(
                          (timeStamp) {
                            ref.read(settingsProvider.notifier).state = settings
                                .copyWith(handyServerIP: Uri.parse(output));
                            ref.refresh(
                                socketClientProvider); // Has to be refresh because we need the socket to rebuild
                          },
                        );
                      }
                    }),
              ],
            ),
          ),
          Chip(
            label: const Text("Made with ❤️ by Artur Nowak"),
            backgroundColor: Colors.red[400]!.withOpacity(0.2),
          )
        ],
      ),
    );
  }
}
