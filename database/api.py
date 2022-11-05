import typing as t

import common.instances as instaces


def get_all_entities(
    coords: instaces.Coordinates, radius: instaces.Distance
) -> t.List[instaces.Entity]:
    # TODO
    return []


def get_best_locations(
    coords: instaces.Coordinates,
    radius: instaces.Distance,
    n_max_results: int,
    division_ratio: int,
) -> t.List[t.Tuple[instaces.Location, instaces.LocationDescription]]:
    # TODO
    return []


def get_overall_about_location(
    coords: instaces.Coordinates, radius: instaces.Distance
) -> instaces.LocationDescription:
    # TODO
    return instaces.LocationDescription()


def get_best_entites(
    coords: instaces.Coordinates,
    radius: instaces.Distance,
    n_max_results: int,
) -> t.List[t.Tuple[instaces.Entity, instaces.EntityDescription]]:
    # TODO
    return []
