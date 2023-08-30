import 'package:handy/gen/strings.g.dart';

String convertToAgo(DateTime input) {
  Duration diff = DateTime.now().difference(input);

  String ago = t.time_ago.ago;

  if (diff.inDays >= 1) {
    return '${t.time_ago.day(n: diff.inDays)} $ago';
  } else if (diff.inHours >= 1) {
    return '${t.time_ago.hour(n: diff.inHours)} $ago';
  } else if (diff.inMinutes >= 1) {
    return '${t.time_ago.minute(n: diff.inMinutes)} $ago';
  } else if (diff.inSeconds >= 1) {
    return '${t.time_ago.second(n: diff.inSeconds)} $ago';
  } else {
    return t.time_ago.now;
  }
}
