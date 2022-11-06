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
    UNKNOWN = "Unkonwn"
    BUS = "Bus"
    TRAMWAY = "Tramway"
    # TODO: Add all


class RentalKind(Enum):
    BIKE = "Bike"
    SCOOTER = "Scooter"
    # TODO: Add all


@dataclass
class TransportStop:
    coords: Coordinates
    id: InstanceId
    kind: TransportKind

    def name(self) -> str:
        return f"{self.kind.value} stop"


@dataclass
class Restaraunt:
    coords: Coordinates
    id: InstanceId
    is_bio: bool
    is_chain: bool
    is_vegan: bool
    is_vegeterian: bool
    has_vegan_options: bool
    
    def name(self) -> str:
        if self.is_vegan:
            return "Vegan restaurant"
        if self.is_vegeterian:
            return "Vegeterian restaurant"
        return "Restaurant"

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

    def name(self) -> str:
        return f"{self.kind.value} rental point"


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


@dataclass
class LocationDescription:
    desc: str = "Location score is: {}"
    score: float = 0

    def __str__(self):
        return self.desc.format(self.score)



@dataclass
class EntityPreferences:
    entity_type: EntityType
