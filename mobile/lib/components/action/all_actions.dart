import "dart:async";

import "package:flutter/material.dart";
import "package:handy/components/loading_dialog/loading_dialog.dart";
import "package:handy/gen/strings.g.dart";
import "package:handy/providers/all_actions_provider.dart";
import "package:handy/providers/performed_actions_provider.dart";
import "package:handy/providers/socket_provider.dart";
import "package:handy/types/action.dart";
import "package:handy/utils/process_socket_response.dart";
import "package:handy/utils/time_ago.dart";
import 'package:flutter_riverpod/flutter_riverpod.dart';

class AllActions extends ConsumerStatefulWidget {
  const AllActions({super.key});

  @override
  AllActionsState createState() => AllActionsState();
}

class AllActionsState extends ConsumerState<AllActions> {
  bool isLoading = true;

  Future<void> getActions() async {
    var socket = ref.read(socketClientProvider);

    // If all actions have already been fetched
    if (ref.read(allActionsProvider) != null) return;

    Completer c = Completer();
    socket.emitWithAck("actions/all", {}, ack: (data) {
      bool isSuccess = processSocketRepsonse(context, data);

      c.complete(isSuccess ? data : null);
    });

    var data = await c.future;
    List<ActionObject> list = (data["actions"]).map<ActionObject>((e) {
      return ActionObject.fromJson(e);
    }).toList();

    ref.read(allActionsProvider.notifier).state = list;

    setState(() {
      isLoading = false;
    });
  }

  Future<void> tryToPerformAction(ActionObject action) async {
    if (action.changeNumericValue) {
      // If it's a numeric value, you can't perform it out-of-box, without gestures
      // TODO: In the future, add an option to perform it and set the value in the app
      showDialog(
          context: context,
          builder: (context) => AlertDialog(
                title: Text(t.actions.cannot_perform_action.title),
                content: Text(t.actions.cannot_perform_action.description),
                actions: [
                  TextButton(
                    child: Text(t.buttons.ok),
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                  ),
                ],
              ));
      return;
    }

    var socket = ref.read(socketClientProvider);

    Completer c = Completer();
    socket.emitWithAck("actions/execute", {'index': action.index}, ack: (data) {
      processSocketRepsonse(context, data);

      if (data["recentActions"] != null) {
        List<ActionPerformed> list =
            (data["recentActions"]).map<ActionPerformed>((e) {
          return ActionPerformed.fromJson(e);
        }).toList();
        ref.read(performedActionsProvider.notifier).state =
            list.reversed.toList();
      }

      c.complete();
    });

    showLoadingDialog(context, () async {
      await c.future;
    });
  }

  @override
  void initState() {
    super.initState();

    getActions();
  }

  @override
  Widget build(BuildContext context) {
    List<ActionObject>? allActions = ref.watch(allActionsProvider);
    List<ActionPerformed>? performedActions =
        ref.watch(performedActionsProvider);

    if (isLoading || allActions == null) {
      return const CircularProgressIndicator();
    }
    return ListView.builder(
      physics: const NeverScrollableScrollPhysics(),
      shrinkWrap: true,
      itemBuilder: (context, index) {
        ActionObject action = allActions[index];
        String? lastPerformed;

        if (performedActions != null) {
          // Try to find the performed action
          try {
            ActionPerformed? performed = performedActions.reversed
                .toList()
                .firstWhere((element) => element.index == action.index);

            lastPerformed = t.actions
                .last_performed(date: convertToAgo(performed.timestamp));
            // ignore: empty_catches
          } catch (err) {}
        }

        return ListTile(
            title: Text("#${action.index} ${action.name}"),
            subtitle: Text(lastPerformed ?? t.actions.didnt_perform_lately),
            onTap: () {
              tryToPerformAction(action);
            });
      },
      itemCount: allActions.length,
    );
  }
}
