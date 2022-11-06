import enum

import interface.config as config


class BotString(enum.Enum):
    COMMAND_DESC_HELP = "Get help"
    COMMAND_DESC_DECIDE = "Find dream destination"
    COMMAND_DESC_OVERALL = "Get area description"
    COMMAND_DESC_INPLACE = "Show places nearby"

    INVALID_LOCATION_FORMAT = "ℹ️ Invalid location format, please select corresponding button on your input panel"
    INVALID_RADIUS_FORMAT = "ℹ️ Invalid radius format, send a number like '0.7'"
    INVALID_RADIUS_TOO_SMALL = (
        f"😞 Radius is too small, should be at least {config.MIN_RADIUS} km"
    )
    INVALID_RADIUS_TOO_BIG = (
        f"😔 Radius is too big, should be no more than {config.MAX_RADIUS} km"
    )
    INVALID_ENTITY_KIND = """😔 <b>These</b> amazing places are not yet discovered by our team :(

Try out something from the given options!
"""

    DECISION_LOCATION = """📍 <b>Send location!</b>

We will analyse this area and tell you which regions of this location are most sustainable!
"""
    DECISION_RADIUS = """🌐 <b> Send a radius </b> (in kilometers)
        
Tell us in which radius do you consider traveling
"""

    OVERALL_LOCATION = """📍 <b>Send any location!</b>

In this location we will get all information about sustainability of restaurants, grocery shops, public transport stops and bike or scooter renting services
"""
    OVERALL_RADIUS = """🌐 <b> Send a radius </b> (in kilometers)
        
The radius of the area you want a detailed report on
"""

    INPLACE_LOCATION = """📍 <b>Send location to explore!</b>

We will share with you the most sustainable places: farmer markets, cafes which are using local production and so on
"""
    INPLACE_RADIUS = """🌐 <b> Send a radius </b> (in kilometers)
        
Radius in which you want to find new places
"""
    INPLACE_ENTITY_KIND = """🧭 <b> Select specific type of place </b>

Our ✨ <i>sustainability</i> ✨ faries 🧚 will voluntary select the best places of that kind!
"""

    SHARE_LOCATION = "📍 Share Current Location"

    START = """Hello, {}! 👋

This is a [some description]


🧭 /decide - Helps you choose the most sustainable region to travel or to live

🍀 /overall - Get to know some location in terms of sustainability

🏃🏾‍♀️ /inplace - Learn about the places to go out that care most about the environment near a given location
"""

    HELP = """🧭 /decide - Helps you choose the most sustainable region to travel or to live

🍀 /overall - Get to know some location in terms of sustainability

🏃🏾‍♀️ /inplace - Learn about the places to go out that care most about the environment near a given location
"""
