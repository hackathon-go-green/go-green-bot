import typing as t

from enum import Enum
from dataclasses import dataclass


# TODO: Choose better types
@dataclass
class Coordinates:
    lat: float
    lon: float


Distance = float

InstanceId = int


class TransportKind(Enum):
    UNKNOWN = "unkonwn"
    BUS = "bus"
    TRAMWAY = "tramway"
    # TODO: Add all


class RentalKind(Enum):
    BIKE = "bike"
    SCOOTER = "scooter"
    # TODO: Add all


@dataclass
class TransportStop:
    coords: Coordinates
    id: InstanceId
    kind: TransportKind


@dataclass
class Restaraunt:
    coords: Coordinates
    id: InstanceId
    is_bio: bool
    is_chain: bool
    is_vegan: bool
    is_vegeterian: bool
    has_vegan_options: bool

    def rank(self):
        bio = 1.5
        vegan_options = 1
        veget = 1.5
        vegan = 4
        chain = -0.8
        score = 0
        if self.is_vegan == 1:
            score += vegan
        if self.is_vegeterian == 1:
            score += veget
        if self.has_vegan_options == 1:
            score += vegan_options
        if self.is_bio == 1:
            score += bio
        if self.is_chain == 1:
            score += chain
        return round(max(score, 0) * 1.25, 1)

    def descr(self):
        msg = ""
        # TO BE DEV - location - maybe?
        # rstr.msg = "The restaurant found at the lat:  "
        # rstr.msg += rstr.lat
        # rstr.msg += " and long: "
        # rstr.msg += rstr.lon
        # CHECK rstr.vegan AND rstr.veget RETURNS

        # TO BE Approved

        msg += "This restaurant has a score"
        msg += " of " + "{:.1f}/10.0"
        if self.is_vegan == 1:
            msg += " and it's Vegan."
            return msg
        elif self.is_vegeterian == 1:
            msg += " and it's Vegetarian."
            return msg

        msg += ". It is "

        # output based on is_chain value
        if self.is_chain == 0:
            msg += "not "

        # standard output
        msg += "part of a chain and it "

        # output based on is_bio value
        if self.is_bio == 1:
            msg += "offers "
        else:
            msg += "doesn't offer "

        # standard output
        msg += "bio and organic products. "
        msg += "However, the restaurant "

        # output based on is_vegan option value
        if self.has_vegan_options == 1:
            msg += "offers vegan dishes."
        else:
            msg += "does not offer vegan dishes."

        return msg


def compare_restaurants(a, b):
    return a.rank() - b.rank()


@dataclass
class RentalPoint:
    coords: Coordinates
    id: InstanceId
    kind: RentalKind


class EntityType(Enum):
    RESTARAUNT = "restaurant"
    TRANSPORT = "transport"
    RENTAL_POINT = "rental"


Entity = t.Union[TransportStop, Restaraunt, RentalPoint]


@dataclass
class Location:
    coord: Coordinates
    radius: Distance

    def __str__(self):
        return "lat: {}, lon: {}, radius: {}".format(self.coord.lat, self.coord.lon, self.radius)


@dataclass
class EntityDescription:
    desc: str = "Entity score is: {:.1f}"
    score: float = 0

    def __str__(self):
        return self.desc.format(self.score)

    # TODO: Add common information about place - bus stop, store, ... (as strings)


@dataclass
class LocationDescription:
    desc: str = "Location score is: {:.1f}"
    score: float = 0

    def __str__(self):
        return self.desc.format(self.score)

    # TODO: Add common information about location (city, ) (as strings)


@dataclass
class EntityPreferences:
    entity_type: EntityType
