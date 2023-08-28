bool validateURL(String? url) {
  if (url == null) return false;

  // A URL regex that allows either IP addresses with ports or URLs, also without the TLD, e.g. http://localhost
  RegExp urlRegex = RegExp(
      r"^(https?:\/\/(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d{1,5})?|[a-zA-Z0-9.-]+[a-zA-Z0-9](?::\d{1,5})?)(?:\/[^\s]*)?)$");

  return urlRegex.hasMatch(url);
}
