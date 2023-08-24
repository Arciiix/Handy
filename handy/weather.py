from datetime import datetime
from action_context import ActionContext
from config import CONFIG
from announcements import say
from logger import logger


async def get_weather(ctx: ActionContext):
    hass_client = ctx.hass_client
    state = await hass_client.async_get_state(entity_id=CONFIG.entities.weather)
    logger.info("Got weather")

    # Try to get the translation for the state
    condition_translated = (
        ctx.translations.get_translation(f"weather.{state.state}") or state.state
    )

    tomorrow = state.attributes["forecast"][
        1
    ]  # Index 1 corresponds to tomorrow's forecast
    tomorrow_condition_translated = (
        ctx.translations.get_translation(f"weather.{tomorrow['condition']}")
        or tomorrow["condition"]
    )

    precipitation_tomorrow = f"{ctx.translations.format_number(tomorrow['precipitation'])} {state.attributes['precipitation_unit']}, {ctx.translations.get_translation('weather_chance_of_rain', {'percent': tomorrow.get('precipitation_probability', None)})}"
    updated_at_formatted = state.last_updated.strftime("%H:%M")
    now = datetime.now().strftime("%H:%M")

    args = {
        "condition_now": condition_translated,
        "temp_now": f"{ctx.translations.format_number(state.attributes['temperature'])}{state.attributes['temperature_unit']}",
        "pressure_now": f"{ctx.translations.format_number(state.attributes['pressure'])} {state.attributes['pressure_unit']}",
        "humidity_now": f"{ctx.translations.format_number(int(state.attributes['humidity']))}%",
        "wind_speed_now": f"{ctx.translations.format_number(state.attributes['wind_speed'])} {state.attributes['wind_speed_unit']}",
        "condition_tomorrow": tomorrow_condition_translated,
        "temp_tomorrow": f"{ctx.translations.format_number(tomorrow['temperature'])}{state.attributes['temperature_unit']}",
        "temp_min_tomorrow": f"{ctx.translations.format_number(tomorrow['templow'])}{state.attributes['temperature_unit']}",
        "precipitation_tomorrow": precipitation_tomorrow,
        "wind_speed": f"{ctx.translations.format_number(tomorrow['wind_speed'])} {state.attributes['wind_speed_unit']}",
        "updated_at": updated_at_formatted,
        "now": now,
    }

    weather_raport = ctx.translations.get_translation("weather_raport", args)
    logger.info("Weather raport generated")

    await say(ctx, weather_raport)
    logger.info("Weather has been said!")
