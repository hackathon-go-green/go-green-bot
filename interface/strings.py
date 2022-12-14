import enum

import interface.config as config


class BotString(enum.Enum):
    COMMAND_DESC_HELP = "Get help"
    COMMAND_DESC_DECIDE = "Find dream destination"
    COMMAND_DESC_OVERALL = "Get area description"
    COMMAND_DESC_INPLACE = "Show places nearby"

    INVALID_LOCATION_FORMAT = "⚠️ Invalid location format, please select corresponding button on your input panel"
    INVALID_RADIUS_FORMAT = "⚠️ Invalid radius format, send a number like '0.7'"
    INVALID_RADIUS_TOO_SMALL = (
        f"😞 Radius is too small, should be at least {config.MIN_RADIUS} km"
    )
    INVALID_RADIUS_TOO_BIG = (
        f"😔 Radius is too big, should be no more than {config.MAX_RADIUS} km"
    )
    INVALID_ENTITY_KIND = """😔 <b>These</b> amazing places are not yet discovered by our team 🙁

Try out something from the given options!
"""

    DECISION_LOCATION = """📍 <b>Send location!</b>

I will analyse this area and tell you which regions of this location are most sustainable!
"""
    DECISION_RADIUS = """🌐 <b> Send a radius </b> (in kilometers)
        
Tell me in which radius do you consider traveling
"""

    OVERALL_LOCATION = """📍 <b>Send any location!</b>

In this location I will gather all information about sustainability of restaurants, grocery shops, public transport stops and bike or scooter renting services
"""
    OVERALL_RADIUS = """🌐 <b> Send a radius </b> (in kilometers)
        
The radius of the area you want a detailed report on
"""

    INPLACE_LOCATION = """📍 <b>Send location to explore!</b>

I will share with you the most sustainable places: farmer markets, cafes which are using local production and so on
"""
    INPLACE_RADIUS = """🌐 <b> Send a radius </b> (in kilometers)
        
Radius in which you want to find new places
"""
    INPLACE_ENTITY_KIND = """🧭 <b> Select specific type of place </b>

My ✨ <i>sustainability</i> ✨ faries 🧚 will voluntary select the best places of that kind!
"""

    SHARE_LOCATION = "📍 Share Current Location"

    START = """Hello, {}! 👋

I'm a Toby! A bot that helps you reduce your carbon footprint in your daily life. I know everything about all the restaurants, grocery stores, and bus stops around the world (and so much more!)


🧭 /decide - Helps you choose the most sustainable region to travel to or to live in

🍀 /overall - Find out how sustainable your whereabouts and surroundings are

🏃🏾‍♀️ /inplace - Feel like going out? Want to find the best and the nearest option?
"""

    HELP = """🧭 /decide - Helps you choose the most sustainable region to travel to or to live in

🍀 /overall - Find out how sustainable your whereabouts and surroundings are

🏃🏾‍♀️ /inplace - Feel like going out? Want to find the best and the nearest option?
"""

    TOP_LOCATION = """<b>Choice 🍃 {}</b>
<i>Score: {}/10</i>
<b>*</b>

{}
"""

    REGION_DESCRIPTION = """🍃
<i>Score: {}/10</i>
<b>*</b>

{}
"""

    TOP_ENTITY = """<b>🍃 {}</b>
<i>Score: {}/10</i>
<b>*</b>

<b>Summary:</b>
{}

<i>{}</i>
"""

    ENTITY_DESC_VEGAN = "🥗 Vegan"
    ENTITY_DESC_VEGETERIAN = "🥛🥚 Vegetarian"
    ENTITY_DESC_VEG_OPTIONS = "🐣 Has vegan options"
    ENTITY_DESC_HAS_VEG_OPTIONS = "Uses local products (bio)"
    ENTITY_DESC_NO_VEG_OPTIONS = "Does not use local products (not bio)"
    ENTITY_IS_NOT_A_CHAIN = "Is not a chain"
    ENTITY_IS_A_CHAIN = "Chain restaurant"
