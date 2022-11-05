import enum


class BotString(enum.Enum):
    INVALID_LOCATION_FORMAT = "Invalid location format, please select corresponding button on your input panel"
    INVALID_RADIUS_FORMAT = "Invalid radius format, send a number like '0.7'"

    DECISION_LOCATION = "Send location where you want to go!"
    DECISION_RADIUS = (
        "Send a radius (in kilometers) where you are considering traveling"
    )

    OVERALL_LOCATION = "Send any location!"
    OVERALL_RADIUS = (
        "Send the radius (in kilometers) of the location you want to know about"
    )

    INPLACE_LOCATION = "Send the location you want to explore"
    INPLACE_RADIUS = "Send the radius (in kilometers) in which you can walk"
