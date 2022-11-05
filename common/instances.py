import typing as t

from enum import Enum
from dataclasses import dataclass

Coordinates = str
InstanceId = str


class TransportKind(Enum):
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
