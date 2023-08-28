/// Generated file. Do not edit.
///
/// Original: assets/i18n
/// To regenerate, run: `dart run slang`
///
/// Locales: 2
/// Strings: 66 (33 per locale)
///
/// Built on 2023-08-28 at 15:38 UTC

// coverage:ignore-file
// ignore_for_file: type=lint

import 'package:flutter/widgets.dart';
import 'package:slang/builder/model/node.dart';
import 'package:slang_flutter/slang_flutter.dart';
export 'package:slang_flutter/slang_flutter.dart';

const AppLocale _baseLocale = AppLocale.en;

/// Supported locales, see extension methods below.
///
/// Usage:
/// - LocaleSettings.setLocale(AppLocale.en) // set locale
/// - Locale locale = AppLocale.en.flutterLocale // get flutter locale from enum
/// - if (LocaleSettings.currentLocale == AppLocale.en) // locale check
enum AppLocale with BaseAppLocale<AppLocale, _StringsEn> {
	en(languageCode: 'en', build: _StringsEn.build),
	pl(languageCode: 'pl', build: _StringsPl.build);

	const AppLocale({required this.languageCode, this.scriptCode, this.countryCode, required this.build}); // ignore: unused_element

	@override final String languageCode;
	@override final String? scriptCode;
	@override final String? countryCode;
	@override final TranslationBuilder<AppLocale, _StringsEn> build;

	/// Gets current instance managed by [LocaleSettings].
	_StringsEn get translations => LocaleSettings.instance.translationMap[this]!;
}

/// Method A: Simple
///
/// No rebuild after locale change.
/// Translation happens during initialization of the widget (call of t).
/// Configurable via 'translate_var'.
///
/// Usage:
/// String a = t.someKey.anotherKey;
/// String b = t['someKey.anotherKey']; // Only for edge cases!
_StringsEn get t => LocaleSettings.instance.currentTranslations;

/// Method B: Advanced
///
/// All widgets using this method will trigger a rebuild when locale changes.
/// Use this if you have e.g. a settings page where the user can select the locale during runtime.
///
/// Step 1:
/// wrap your App with
/// TranslationProvider(
/// 	child: MyApp()
/// );
///
/// Step 2:
/// final t = Translations.of(context); // Get t variable.
/// String a = t.someKey.anotherKey; // Use t variable.
/// String b = t['someKey.anotherKey']; // Only for edge cases!
class Translations {
	Translations._(); // no constructor

	static _StringsEn of(BuildContext context) => InheritedLocaleData.of<AppLocale, _StringsEn>(context).translations;
}

/// The provider for method B
class TranslationProvider extends BaseTranslationProvider<AppLocale, _StringsEn> {
	TranslationProvider({required super.child}) : super(settings: LocaleSettings.instance);

	static InheritedLocaleData<AppLocale, _StringsEn> of(BuildContext context) => InheritedLocaleData.of<AppLocale, _StringsEn>(context);
}

/// Method B shorthand via [BuildContext] extension method.
/// Configurable via 'translate_var'.
///
/// Usage (e.g. in a widget's build method):
/// context.t.someKey.anotherKey
extension BuildContextTranslationsExtension on BuildContext {
	_StringsEn get t => TranslationProvider.of(this).translations;
}

/// Manages all translation instances and the current locale
class LocaleSettings extends BaseFlutterLocaleSettings<AppLocale, _StringsEn> {
	LocaleSettings._() : super(utils: AppLocaleUtils.instance);

	static final instance = LocaleSettings._();

	// static aliases (checkout base methods for documentation)
	static AppLocale get currentLocale => instance.currentLocale;
	static Stream<AppLocale> getLocaleStream() => instance.getLocaleStream();
	static AppLocale setLocale(AppLocale locale, {bool? listenToDeviceLocale = false}) => instance.setLocale(locale, listenToDeviceLocale: listenToDeviceLocale);
	static AppLocale setLocaleRaw(String rawLocale, {bool? listenToDeviceLocale = false}) => instance.setLocaleRaw(rawLocale, listenToDeviceLocale: listenToDeviceLocale);
	static AppLocale useDeviceLocale() => instance.useDeviceLocale();
	@Deprecated('Use [AppLocaleUtils.supportedLocales]') static List<Locale> get supportedLocales => instance.supportedLocales;
	@Deprecated('Use [AppLocaleUtils.supportedLocalesRaw]') static List<String> get supportedLocalesRaw => instance.supportedLocalesRaw;
	static void setPluralResolver({String? language, AppLocale? locale, PluralResolver? cardinalResolver, PluralResolver? ordinalResolver}) => instance.setPluralResolver(
		language: language,
		locale: locale,
		cardinalResolver: cardinalResolver,
		ordinalResolver: ordinalResolver,
	);
}

/// Provides utility functions without any side effects.
class AppLocaleUtils extends BaseAppLocaleUtils<AppLocale, _StringsEn> {
	AppLocaleUtils._() : super(baseLocale: _baseLocale, locales: AppLocale.values);

	static final instance = AppLocaleUtils._();

	// static aliases (checkout base methods for documentation)
	static AppLocale parse(String rawLocale) => instance.parse(rawLocale);
	static AppLocale parseLocaleParts({required String languageCode, String? scriptCode, String? countryCode}) => instance.parseLocaleParts(languageCode: languageCode, scriptCode: scriptCode, countryCode: countryCode);
	static AppLocale findDeviceLocale() => instance.findDeviceLocale();
	static List<Locale> get supportedLocales => instance.supportedLocales;
	static List<String> get supportedLocalesRaw => instance.supportedLocalesRaw;
}

// context enums

enum PlaylistTypesContext {
	local,
	youtube,
}

// translations

// Path: <root>
class _StringsEn implements BaseTranslations<AppLocale, _StringsEn> {

	/// You can call this constructor and build your own translation instance of this locale.
	/// Constructing via the enum [AppLocale.build] is preferred.
	_StringsEn.build({Map<String, Node>? overrides, PluralResolver? cardinalResolver, PluralResolver? ordinalResolver})
		: assert(overrides == null, 'Set "translation_overrides: true" in order to enable this feature.'),
		  $meta = TranslationMetadata(
		    locale: AppLocale.en,
		    overrides: overrides ?? {},
		    cardinalResolver: cardinalResolver,
		    ordinalResolver: ordinalResolver,
		  ) {
		$meta.setFlatMapFunction(_flatMapFunction);
	}

	/// Metadata for the translations of <en>.
	@override final TranslationMetadata<AppLocale, _StringsEn> $meta;

	/// Access flat map
	dynamic operator[](String key) => $meta.getTranslation(key);

	late final _StringsEn _root = this; // ignore: unused_field

	// Translations
	late final _StringsButtonsEn buttons = _StringsButtonsEn._(_root);
	late final _StringsDialogEn dialog = _StringsDialogEn._(_root);
	late final _StringsErrorEn error = _StringsErrorEn._(_root);
	String get loading => 'Loading...';
	late final _StringsNavigationEn navigation = _StringsNavigationEn._(_root);
	late final _StringsPlaylistEn playlist = _StringsPlaylistEn._(_root);
	late final _StringsSettingsEn settings = _StringsSettingsEn._(_root);
}

// Path: buttons
class _StringsButtonsEn {
	_StringsButtonsEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get cancel => 'Cancel';
	String get delete => 'Delete';
	String get ok => 'OK';
	String get save => 'Save';
}

// Path: dialog
class _StringsDialogEn {
	_StringsDialogEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	late final _StringsDialogDeleteItemEn delete_item = _StringsDialogDeleteItemEn._(_root);
}

// Path: error
class _StringsErrorEn {
	_StringsErrorEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get title => 'Error';
}

// Path: navigation
class _StringsNavigationEn {
	_StringsNavigationEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get home => 'Home';
	String get playlist => 'Playlist';
	String get settings => 'Settings';
}

// Path: playlist
class _StringsPlaylistEn {
	_StringsPlaylistEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get title => 'Playlist';
	late final _StringsPlaylistMediaEn media = _StringsPlaylistMediaEn._(_root);
	late final _StringsPlaylistYoutubeEn youtube = _StringsPlaylistYoutubeEn._(_root);
	String get open_url => 'Open URL';
	late final _StringsPlaylistFormEn form = _StringsPlaylistFormEn._(_root);
}

// Path: settings
class _StringsSettingsEn {
	_StringsSettingsEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get title => 'Settings';
	late final _StringsSettingsSectionsEn sections = _StringsSettingsSectionsEn._(_root);
	late final _StringsSettingsIpEn ip = _StringsSettingsIpEn._(_root);
}

// Path: dialog.delete_item
class _StringsDialogDeleteItemEn {
	_StringsDialogDeleteItemEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get title => 'Delete item';
	String description({required Object item_name}) => 'Are you sure you want to delete this item ${item_name}?';
}

// Path: playlist.media
class _StringsPlaylistMediaEn {
	_StringsPlaylistMediaEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get local => 'Local';
	String get youtube => 'YouTube';
}

// Path: playlist.youtube
class _StringsPlaylistYoutubeEn {
	_StringsPlaylistYoutubeEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	late final _StringsPlaylistYoutubeAdviceEn advice = _StringsPlaylistYoutubeAdviceEn._(_root);
	String get fetch_data => 'Fetch video data';
}

// Path: playlist.form
class _StringsPlaylistFormEn {
	_StringsPlaylistFormEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String edit_type({required PlaylistTypesContext context}) {
		switch (context) {
			case PlaylistTypesContext.local:
				return 'local playlist item';
			case PlaylistTypesContext.youtube:
				return 'YouTube playlist item';
		}
	}
	String title_edit({required PlaylistTypesContext context}) => 'Edit ${_root.playlist.form.edit_type(context: context)}';
	String title_add({required PlaylistTypesContext context}) => 'Add ${_root.playlist.form.edit_type(context: context)}';
	late final _StringsPlaylistFormFieldsEn fields = _StringsPlaylistFormFieldsEn._(_root);
	late final _StringsPlaylistFormErrorsEn errors = _StringsPlaylistFormErrorsEn._(_root);
}

// Path: settings.sections
class _StringsSettingsSectionsEn {
	_StringsSettingsSectionsEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get general => 'General';
}

// Path: settings.ip
class _StringsSettingsIpEn {
	_StringsSettingsIpEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get title => 'Server IP';
	String get description => 'The IP (together with the port and protocol (HTTP)) of the Handy server';
}

// Path: playlist.youtube.advice
class _StringsPlaylistYoutubeAdviceEn {
	_StringsPlaylistYoutubeAdviceEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get title => 'Advice';
	String get description => 'A better way to add YouTube videos to Handy is to use the Share button on any YouTube video and select the Handy app.';
}

// Path: playlist.form.fields
class _StringsPlaylistFormFieldsEn {
	_StringsPlaylistFormFieldsEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get name => 'Name';
	String get custom_pronunciation => 'Custom pronunciation of the name';
	String get pronunciation => 'Pronunciation';
	String get url => 'URL';
	String get url_helper => 'Start with e.g. https://';
}

// Path: playlist.form.errors
class _StringsPlaylistFormErrorsEn {
	_StringsPlaylistFormErrorsEn._(this._root);

	final _StringsEn _root; // ignore: unused_field

	// Translations
	String get name_empty => 'Please enter a name';
	String get url_invalid => 'Please enter a valid URL';
}

// Path: <root>
class _StringsPl implements _StringsEn {

	/// You can call this constructor and build your own translation instance of this locale.
	/// Constructing via the enum [AppLocale.build] is preferred.
	_StringsPl.build({Map<String, Node>? overrides, PluralResolver? cardinalResolver, PluralResolver? ordinalResolver})
		: assert(overrides == null, 'Set "translation_overrides: true" in order to enable this feature.'),
		  $meta = TranslationMetadata(
		    locale: AppLocale.pl,
		    overrides: overrides ?? {},
		    cardinalResolver: cardinalResolver,
		    ordinalResolver: ordinalResolver,
		  ) {
		$meta.setFlatMapFunction(_flatMapFunction);
	}

	/// Metadata for the translations of <pl>.
	@override final TranslationMetadata<AppLocale, _StringsEn> $meta;

	/// Access flat map
	@override dynamic operator[](String key) => $meta.getTranslation(key);

	@override late final _StringsPl _root = this; // ignore: unused_field

	// Translations
	@override late final _StringsButtonsPl buttons = _StringsButtonsPl._(_root);
	@override late final _StringsDialogPl dialog = _StringsDialogPl._(_root);
	@override late final _StringsErrorPl error = _StringsErrorPl._(_root);
	@override String get loading => 'Ładowanie...';
	@override late final _StringsNavigationPl navigation = _StringsNavigationPl._(_root);
	@override late final _StringsPlaylistPl playlist = _StringsPlaylistPl._(_root);
	@override late final _StringsSettingsPl settings = _StringsSettingsPl._(_root);
}

// Path: buttons
class _StringsButtonsPl implements _StringsButtonsEn {
	_StringsButtonsPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get cancel => 'Anuluj';
	@override String get delete => 'Usuń';
	@override String get ok => 'OK';
	@override String get save => 'Zapisz';
}

// Path: dialog
class _StringsDialogPl implements _StringsDialogEn {
	_StringsDialogPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override late final _StringsDialogDeleteItemPl delete_item = _StringsDialogDeleteItemPl._(_root);
}

// Path: error
class _StringsErrorPl implements _StringsErrorEn {
	_StringsErrorPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get title => 'Wystąpił błąd';
}

// Path: navigation
class _StringsNavigationPl implements _StringsNavigationEn {
	_StringsNavigationPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get home => 'Start';
	@override String get playlist => 'Playlista';
	@override String get settings => 'Ustawienia';
}

// Path: playlist
class _StringsPlaylistPl implements _StringsPlaylistEn {
	_StringsPlaylistPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get title => 'Playlista';
	@override late final _StringsPlaylistMediaPl media = _StringsPlaylistMediaPl._(_root);
	@override late final _StringsPlaylistYoutubePl youtube = _StringsPlaylistYoutubePl._(_root);
	@override String get open_url => 'Otwórz URL';
	@override late final _StringsPlaylistFormPl form = _StringsPlaylistFormPl._(_root);
}

// Path: settings
class _StringsSettingsPl implements _StringsSettingsEn {
	_StringsSettingsPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get title => 'Ustawienia';
	@override late final _StringsSettingsSectionsPl sections = _StringsSettingsSectionsPl._(_root);
	@override late final _StringsSettingsIpPl ip = _StringsSettingsIpPl._(_root);
}

// Path: dialog.delete_item
class _StringsDialogDeleteItemPl implements _StringsDialogDeleteItemEn {
	_StringsDialogDeleteItemPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get title => 'Usuń element';
	@override String description({required Object item_name}) => 'Czy na pewno chcesz usunąć ${item_name}?';
}

// Path: playlist.media
class _StringsPlaylistMediaPl implements _StringsPlaylistMediaEn {
	_StringsPlaylistMediaPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get local => 'Lokalna';
	@override String get youtube => 'YouTube';
}

// Path: playlist.youtube
class _StringsPlaylistYoutubePl implements _StringsPlaylistYoutubeEn {
	_StringsPlaylistYoutubePl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override late final _StringsPlaylistYoutubeAdvicePl advice = _StringsPlaylistYoutubeAdvicePl._(_root);
	@override String get fetch_data => 'Pobierz dane wideo';
}

// Path: playlist.form
class _StringsPlaylistFormPl implements _StringsPlaylistFormEn {
	_StringsPlaylistFormPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String edit_type({required PlaylistTypesContext context}) {
		switch (context) {
			case PlaylistTypesContext.local:
				return 'element lokalnej playlisty';
			case PlaylistTypesContext.youtube:
				return 'element playlisty z YouTube';
		}
	}
	@override String title_edit({required PlaylistTypesContext context}) => 'Edytuj ${_root.playlist.form.edit_type(context: context)}';
	@override String title_add({required PlaylistTypesContext context}) => 'Dodaj ${_root.playlist.form.edit_type(context: context)}';
	@override late final _StringsPlaylistFormFieldsPl fields = _StringsPlaylistFormFieldsPl._(_root);
	@override late final _StringsPlaylistFormErrorsPl errors = _StringsPlaylistFormErrorsPl._(_root);
}

// Path: settings.sections
class _StringsSettingsSectionsPl implements _StringsSettingsSectionsEn {
	_StringsSettingsSectionsPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get general => 'Ogólne';
}

// Path: settings.ip
class _StringsSettingsIpPl implements _StringsSettingsIpEn {
	_StringsSettingsIpPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get title => 'IP serwera';
	@override String get description => 'IP (wraz z portem i protokołem (HTTP)) serwera Handy';
}

// Path: playlist.youtube.advice
class _StringsPlaylistYoutubeAdvicePl implements _StringsPlaylistYoutubeAdviceEn {
	_StringsPlaylistYoutubeAdvicePl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get title => 'Porada';
	@override String get description => 'Lepszym sposobem dodawania filmów z YouTube do Handy jest użycie przycisku Udostępnij na dowolnym filmie YouTube i wybranie aplikacji Handy.';
}

// Path: playlist.form.fields
class _StringsPlaylistFormFieldsPl implements _StringsPlaylistFormFieldsEn {
	_StringsPlaylistFormFieldsPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get name => 'Nazwa';
	@override String get custom_pronunciation => 'Niestandardowa wymowa nazwy';
	@override String get pronunciation => 'Wymowa nazwy';
	@override String get url => 'Adres URL';
	@override String get url_helper => 'Zacznij od np. https://';
}

// Path: playlist.form.errors
class _StringsPlaylistFormErrorsPl implements _StringsPlaylistFormErrorsEn {
	_StringsPlaylistFormErrorsPl._(this._root);

	@override final _StringsPl _root; // ignore: unused_field

	// Translations
	@override String get name_empty => 'Proszę podać nazwę';
	@override String get url_invalid => 'Proszę podać poprawny adres URL';
}

/// Flat map(s) containing all translations.
/// Only for edge cases! For simple maps, use the map function of this library.

extension on _StringsEn {
	dynamic _flatMapFunction(String path) {
		switch (path) {
			case 'buttons.cancel': return 'Cancel';
			case 'buttons.delete': return 'Delete';
			case 'buttons.ok': return 'OK';
			case 'buttons.save': return 'Save';
			case 'dialog.delete_item.title': return 'Delete item';
			case 'dialog.delete_item.description': return ({required Object item_name}) => 'Are you sure you want to delete this item ${item_name}?';
			case 'error.title': return 'Error';
			case 'loading': return 'Loading...';
			case 'navigation.home': return 'Home';
			case 'navigation.playlist': return 'Playlist';
			case 'navigation.settings': return 'Settings';
			case 'playlist.title': return 'Playlist';
			case 'playlist.media.local': return 'Local';
			case 'playlist.media.youtube': return 'YouTube';
			case 'playlist.youtube.advice.title': return 'Advice';
			case 'playlist.youtube.advice.description': return 'A better way to add YouTube videos to Handy is to use the Share button on any YouTube video and select the Handy app.';
			case 'playlist.youtube.fetch_data': return 'Fetch video data';
			case 'playlist.open_url': return 'Open URL';
			case 'playlist.form.edit_type': return ({required PlaylistTypesContext context}) {
				switch (context) {
					case PlaylistTypesContext.local:
						return 'local playlist item';
					case PlaylistTypesContext.youtube:
						return 'YouTube playlist item';
				}
			};
			case 'playlist.form.title_edit': return ({required PlaylistTypesContext context}) => 'Edit ${_root.playlist.form.edit_type(context: context)}';
			case 'playlist.form.title_add': return ({required PlaylistTypesContext context}) => 'Add ${_root.playlist.form.edit_type(context: context)}';
			case 'playlist.form.fields.name': return 'Name';
			case 'playlist.form.fields.custom_pronunciation': return 'Custom pronunciation of the name';
			case 'playlist.form.fields.pronunciation': return 'Pronunciation';
			case 'playlist.form.fields.url': return 'URL';
			case 'playlist.form.fields.url_helper': return 'Start with e.g. https://';
			case 'playlist.form.errors.name_empty': return 'Please enter a name';
			case 'playlist.form.errors.url_invalid': return 'Please enter a valid URL';
			case 'settings.title': return 'Settings';
			case 'settings.sections.general': return 'General';
			case 'settings.ip.title': return 'Server IP';
			case 'settings.ip.description': return 'The IP (together with the port and protocol (HTTP)) of the Handy server';
			default: return null;
		}
	}
}

extension on _StringsPl {
	dynamic _flatMapFunction(String path) {
		switch (path) {
			case 'buttons.cancel': return 'Anuluj';
			case 'buttons.delete': return 'Usuń';
			case 'buttons.ok': return 'OK';
			case 'buttons.save': return 'Zapisz';
			case 'dialog.delete_item.title': return 'Usuń element';
			case 'dialog.delete_item.description': return ({required Object item_name}) => 'Czy na pewno chcesz usunąć ${item_name}?';
			case 'error.title': return 'Wystąpił błąd';
			case 'loading': return 'Ładowanie...';
			case 'navigation.home': return 'Start';
			case 'navigation.playlist': return 'Playlista';
			case 'navigation.settings': return 'Ustawienia';
			case 'playlist.title': return 'Playlista';
			case 'playlist.media.local': return 'Lokalna';
			case 'playlist.media.youtube': return 'YouTube';
			case 'playlist.youtube.advice.title': return 'Porada';
			case 'playlist.youtube.advice.description': return 'Lepszym sposobem dodawania filmów z YouTube do Handy jest użycie przycisku Udostępnij na dowolnym filmie YouTube i wybranie aplikacji Handy.';
			case 'playlist.youtube.fetch_data': return 'Pobierz dane wideo';
			case 'playlist.open_url': return 'Otwórz URL';
			case 'playlist.form.edit_type': return ({required PlaylistTypesContext context}) {
				switch (context) {
					case PlaylistTypesContext.local:
						return 'element lokalnej playlisty';
					case PlaylistTypesContext.youtube:
						return 'element playlisty z YouTube';
				}
			};
			case 'playlist.form.title_edit': return ({required PlaylistTypesContext context}) => 'Edytuj ${_root.playlist.form.edit_type(context: context)}';
			case 'playlist.form.title_add': return ({required PlaylistTypesContext context}) => 'Dodaj ${_root.playlist.form.edit_type(context: context)}';
			case 'playlist.form.fields.name': return 'Nazwa';
			case 'playlist.form.fields.custom_pronunciation': return 'Niestandardowa wymowa nazwy';
			case 'playlist.form.fields.pronunciation': return 'Wymowa nazwy';
			case 'playlist.form.fields.url': return 'Adres URL';
			case 'playlist.form.fields.url_helper': return 'Zacznij od np. https://';
			case 'playlist.form.errors.name_empty': return 'Proszę podać nazwę';
			case 'playlist.form.errors.url_invalid': return 'Proszę podać poprawny adres URL';
			case 'settings.title': return 'Ustawienia';
			case 'settings.sections.general': return 'Ogólne';
			case 'settings.ip.title': return 'IP serwera';
			case 'settings.ip.description': return 'IP (wraz z portem i protokołem (HTTP)) serwera Handy';
			default: return null;
		}
	}
}
