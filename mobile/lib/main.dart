import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:handy/gen/strings.g.dart';
import 'package:handy/providers/shared_preferences_provider.dart';
import 'package:handy/router.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  LocaleSettings.useDeviceLocale();

  final sharedPrefs = await SharedPreferences.getInstance();

  runApp(ProviderScope(overrides: [
    sharedPreferencesProvider.overrideWithValue(sharedPrefs),
  ], child: TranslationProvider(child: const HandyApp())));
}

class HandyApp extends StatelessWidget {
  const HandyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Handy',
      locale: TranslationProvider.of(context).flutterLocale, // use provider
      supportedLocales: AppLocaleUtils.supportedLocales,
      localizationsDelegates: GlobalMaterialLocalizations.delegates,
      theme: ThemeData(
        colorScheme: const ColorScheme.dark(),
        useMaterial3: true,
      ),
      routerConfig: router,
    );
  }
}
