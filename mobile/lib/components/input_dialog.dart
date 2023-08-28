import "package:flutter/material.dart";
import "package:handy/gen/strings.g.dart";

class InputDialog extends StatefulWidget {
  final String title;
  final String initialValue;
  final bool Function(String) validator;
  final String? errorMessage;
  final String? helperText;

  const InputDialog(
      {super.key,
      required this.title,
      required this.initialValue,
      required this.validator,
      this.errorMessage,
      this.helperText});

  @override
  State<InputDialog> createState() => _InputDialogState();
}

class _InputDialogState extends State<InputDialog> {
  bool showError = false;
  TextEditingController controller = TextEditingController();

  @override
  void initState() {
    super.initState();

    controller.text = widget.initialValue;
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text(widget.title),
      content: TextField(
        controller: controller,
        decoration: InputDecoration(
            helperText: widget.helperText,
            hintText: widget.initialValue,
            errorText: showError ? (widget.errorMessage ?? "Invaild") : null),
      ),
      actions: [
        OutlinedButton(
          child: Text(t.buttons.cancel),
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
        OutlinedButton(
          child: Text(t.buttons.save),
          onPressed: () {
            // Validate the input using the provided validator function
            bool isValid = widget.validator(controller.text);

            if (isValid) {
              Navigator.of(context)
                  .pop(controller.text); // Return the valid text
            } else {
              // Show validation error message
              setState(() {
                showError = true;
              });
            }
          },
        ),
      ],
    );
  }
}
