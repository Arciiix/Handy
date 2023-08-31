import "dart:async";

import "package:flutter/material.dart";
import "package:handy/gen/strings.g.dart";
import "package:handy/providers/performed_actions_provider.dart";
import "package:handy/providers/socket_provider.dart";
import "package:handy/types/action.dart";
import "package:handy/utils/process_socket_response.dart";
import "package:handy/utils/time_ago.dart";
import "package:hooks_riverpod/hooks_riverpod.dart";

class PerformedActions extends ConsumerStatefulWidget {
  const PerformedActions({super.key});

  @override
  PerformedActionsState createState() => PerformedActionsState();
}

class PerformedActionsState extends ConsumerState<PerformedActions> {
  bool isLoading = true;
  DateTime? lastUpdated;

  Timer? performedActionsRefreshTimer;

  Future<void> getActionsPerformed({bool? firstTime = false}) async {
    // If first time is true, the app won't send notification on new action

    var socket = ref.read(socketClientProvider);

    Completer c = Completer();
    socket.emitWithAck("actions/performed", {}, ack: (data) {
      bool isSuccess = processSocketRepsonse(context, data);

      c.complete(isSuccess ? data : null);
    });

    var data = await c.future;

    List<ActionPerformed> list =
        (data["performedActions"]).map<ActionPerformed>((e) {
      return ActionPerformed.fromJson(e);
    }).toList();
    ref.read(performedActionsProvider.notifier).state = list.reversed.toList();

    var newLastUpdated = DateTime.tryParse(data["lastUpdatedAt"] ?? "");

    if (firstTime != true && lastUpdated != newLastUpdated && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(t.actions
              .action_was_performed(action: list.reversed.first.name))));
    }

    setState(() {
      isLoading = false;
      lastUpdated = newLastUpdated;
    });
  }

  void showDialogWithImage(ActionPerformed action) {
    if (action.image == null) return;

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(action.name),
        content: Image.memory(
          action.image!,
          fit: BoxFit.cover,
        ),
        actions: [
          TextButton(
            child: Text(t.buttons.ok),
            onPressed: () {
              Navigator.of(context).pop();
            },
          ),
        ],
      ),
    );
  }

  @override
  void initState() {
    super.initState();

    getActionsPerformed(firstTime: true);

    performedActionsRefreshTimer =
        Timer.periodic(const Duration(seconds: 3), (timer) {
      getActionsPerformed();
    });
  }

  @override
  Widget build(BuildContext context) {
    List<ActionPerformed>? performedActions =
        ref.watch(performedActionsProvider);

    if (isLoading || performedActions == null) {
      return const CircularProgressIndicator();
    }
    return ListView.builder(
      physics: const NeverScrollableScrollPhysics(),
      shrinkWrap: true,
      itemBuilder: (context, index) {
        ActionPerformed action = performedActions[index];

        return ListTile(
            title: Text(action.name),
            subtitle: Text(convertToAgo(action.timestamp)),
            onTap: action.image != null
                ? () => showDialogWithImage(action)
                : null);
      },
      itemCount: performedActions.length,
    );
  }

  @override
  void dispose() {
    performedActionsRefreshTimer?.cancel();

    super.dispose();
  }
}
