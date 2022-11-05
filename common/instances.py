import typing as t

from enum import Enum
from dataclasses import dataclass


# TODO: Choose better types
Coordinates = str

Distance = float

InstanceId = str


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
    has_vegeterian_options: bool


@dataclass
class RentalPoint:
    coords: Coordinates
    id: InstanceId
    kind: RentalKind


Entity = t.Union[TransportStop, Restaraunt, RentalPoint]


@dataclass
class Location:
    # TODO: Add location features
    ...


@dataclass
class EntityDescription:
    # TODO: Add common information about place - bus stop, store, ... (as strings)
    ...


@dataclass
class LocationDescription:
    # TODO: Add common information about location (city, ) (as strings)
    ...


@dataclass
class LocationPreferences:
    # TODO Add some preferences like type, ...
    ...
