import "package:flutter/material.dart";
import "package:go_router/go_router.dart";
import "package:handy/components/loading_dialog/loading_dialog.dart";
import "package:handy/gen/strings.g.dart";
import 'package:avatar_glow/avatar_glow.dart';
import "package:handy/providers/current_state_provider.dart";
import "package:handy/providers/socket_provider.dart";
import "package:handy/types/state.dart";
import "package:hooks_riverpod/hooks_riverpod.dart";

class Control extends ConsumerStatefulWidget {
  const Control({super.key});

  @override
  ControlState createState() => ControlState();
}

class ControlState extends ConsumerState<Control> {
  double deviceHeight = 1000;

  void toggleControl() async {
    var state = ref.read(currentStateProvider);

    if (!state.isConnected) return;

    ref.read(currentStateProvider.notifier).state = await showLoadingDialog(
        context, () async => await state.toggleControl());
  }

  void navigateToPreview() {
    context.push("/preview");
  }

  void reconnect() {
    ref.read(socketClientProvider).connect();
  }

  @override
  void initState() {
    super.initState();

    WidgetsBinding.instance.addPostFrameCallback((_) {
      setState(() {
        deviceHeight = MediaQuery.of(context).size.height;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    CurrentState state = ref.watch(currentStateProvider);

    return Stack(
      fit: StackFit.expand,
      children: [
        Center(
          child: AnimatedContainer(
            decoration: BoxDecoration(
                color: Colors.blue.withOpacity(0.1),
                borderRadius: BorderRadius.circular(
                    state.isEnabled ? 0 : (deviceHeight + 200))),
            width: state.isEnabled ? (deviceHeight + 200) : 0,
            height: state.isEnabled ? (deviceHeight + 200) : 0,
            duration: const Duration(milliseconds: 300),
            curve: Curves.easeInExpo,
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            mainAxisSize: MainAxisSize.max,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text("Handy", style: TextStyle(fontSize: 72)),
              AvatarGlow(
                endRadius: 100,
                animate: state.isConnected && !state.isEnabled,
                child: InkWell(
                  onTap: toggleControl,
                  borderRadius: BorderRadius.circular(100),
                  child: AnimatedContainer(
                      duration: const Duration(milliseconds: 300),
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                          color: (state.isEnabled ? Colors.blue : Colors.red)
                              .withOpacity(0.1),
                          borderRadius: BorderRadius.circular(100)),
                      child: AnimatedSwitcher(
                        duration: const Duration(milliseconds: 300),
                        child: state.isConnected
                            ? (state.isEnabled
                                ? Icon(Icons.back_hand,
                                    size: 128,
                                    color: Colors.blue[200],
                                    key: const Key("icon_enabled"))
                                : Icon(Icons.back_hand_outlined,
                                    size: 128,
                                    color: Colors.red[200],
                                    key: const Key("icon_disabled")))
                            : const Icon(Icons.do_not_touch,
                                size: 128,
                                color: Colors.grey,
                                key: Key("icon_disconnected")),
                      )),
                ),
              ),
              if (state.isConnected && state.isEnabled)
                ElevatedButton.icon(
                    onPressed: navigateToPreview,
                    icon: const Icon(Icons.remove_red_eye_outlined),
                    label: Text(t.control.see_preview)),
              Chip(
                label: Text(state.isConnected
                    ? t.control.connection_state.connected
                    : t.control.connection_state.disconnected),
                avatar: Container(
                  padding: const EdgeInsets.all(2),
                  decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      color: (state.isConnected
                              ? Colors.teal[300]
                              : Colors.red[200])!
                          .withOpacity(0.5)),
                  child: Icon(state.isConnected ? Icons.check : Icons.close,
                      color: Colors.white, size: 14),
                ),
                backgroundColor: (state.isConnected
                    ? Colors.teal[900]
                    : Colors.red[800]!.withOpacity(0.5)),
                deleteIcon:
                    !state.isConnected ? const Icon(Icons.refresh) : null,
                onDeleted: !state.isConnected ? reconnect : null,
                deleteButtonTooltipMessage: t.control.try_to_reconnect,
                side: const BorderSide(width: 0),
              )
            ],
          ),
        )
      ],
    );
  }
}
