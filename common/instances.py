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

    def __lt__(self, other):
        return self.rank() < other.rank()

    def rank(self):
        return self.is_bio - self.is_chain + self.is_vegan \
               + self.is_vegeterian + self.has_vegan_options


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
    desc: str = "Entity score is: "
    score: float = 0

    def __str__(self):
        return self.desc.format(self.score)

    # TODO: Add common information about place - bus stop, store, ... (as strings)



@dataclass
class LocationDescription:
    desc: str = "Location score is: {}"
    score: float = 0

    def __str__(self):
        return self.desc.format(self.score)

    # TODO: Add common information about location (city, ) (as strings)



@dataclass
class EntityPreferences:
    entity_type: EntityType
