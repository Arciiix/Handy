import 'dart:convert';
import 'dart:typed_data';

class ActionObject {
  int index;
  String name;

  bool changeNumericValue;
  num? numericValueMultiplier;
  List<num>? numericValueRange;

  static ActionObject fromJson(Map<String, dynamic> data) {
    return ActionObject(
        index: data["index"],
        name: data["name"],
        changeNumericValue: data["changeNumericValue"],
        numericValueMultiplier: data["numericValueMultiplier"],
        numericValueRange: (data["numericValueRange"] as List<dynamic>?)
            ?.map((e) => num.parse(e.toString()))
            .toList());
  }

  ActionObject(
      {required this.index,
      required this.name,
      required this.changeNumericValue,
      this.numericValueMultiplier,
      this.numericValueRange});
}

class ActionPerformed extends ActionObject {
  DateTime timestamp;
  Uint8List? image;

  ActionPerformed(
      {required this.timestamp,
      this.image,
      required super.index,
      required super.name,
      required super.changeNumericValue,
      super.numericValueMultiplier,
      super.numericValueRange});

  static ActionPerformed fromJson(Map<String, dynamic> data) {
    return ActionPerformed(
      timestamp: DateTime.tryParse(data["timestamp"]) ?? DateTime.now(),
      image: data["image"] != null ? base64Decode(data["image"]) : null,
      index: data["index"],
      name: data["name"],
      changeNumericValue: data["changeNumericValue"],
      numericValueMultiplier: data["numericValueMultiplier"],
      numericValueRange: (data["numericValueRange"] as List<dynamic>?)
          ?.map((e) => num.parse(e.toString()))
          .toList(),
    );
  }
}
