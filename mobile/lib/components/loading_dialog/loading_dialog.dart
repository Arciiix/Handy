import 'package:flutter/material.dart';
import 'package:handy/gen/strings.g.dart';

class LoadingDialog<T> extends StatelessWidget {
  final Future<T?> Function() asyncFunction;

  const LoadingDialog({required this.asyncFunction});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<T?>(
      future: asyncFunction(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Material(
            color: Colors.transparent,
            child: Column(
              mainAxisSize: MainAxisSize.max,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Padding(
                  padding: EdgeInsets.all(8.0),
                  child: CircularProgressIndicator(),
                ),
                Text(t.loading, style: const TextStyle(fontSize: 24))
              ],
            ),
          );
        } else if (snapshot.hasError) {
          return Material(
            color: Colors.transparent,
            child: AlertDialog(
              title: Text(t.error.title),
              content: Text(snapshot.error.toString()),
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
        } else {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            Navigator.of(context).pop(snapshot.data);
          });

          return Container();
        }
      },
    );
  }
}

Future<T> showLoadingDialog<T>(
    BuildContext context, Future<T?> Function() asyncFunction) async {
  return await showDialog(
    context: context,
    barrierDismissible: false,
    builder: (BuildContext context) {
      return LoadingDialog<T>(asyncFunction: asyncFunction);
    },
  );
}
