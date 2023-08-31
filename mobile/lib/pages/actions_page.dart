import "package:flutter/material.dart";
import "package:handy/components/action/all_actions.dart";
import "package:handy/components/action/performed_actions.dart";
import "package:handy/gen/strings.g.dart";

class ActionsPage extends StatelessWidget {
  const ActionsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text(t.actions.title)),
        body: SingleChildScrollView(
          child: Column(
            children: [
              const AllActions(),
              Padding(
                padding: const EdgeInsets.all(12.0),
                child: Text(t.actions.recent,
                    style: const TextStyle(fontSize: 32)),
              ),
              const PerformedActions()
            ],
          ),
        ));
  }
}
