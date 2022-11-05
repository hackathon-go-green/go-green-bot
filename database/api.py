import typing as t

import common.instances as instaces


def get_all_places(

        coords: instaces.Coordinates, radius: instaces.Distance
) -> t.List[instaces.Entity]:
    # TODO
    return []


def get_best_places(
        coords: instaces.Coordinates,
        radius: instaces.Distance,
        n_max_results: int,
        division_ratio: int,
) -> t.List[t.Tuple[instaces.Entity, instaces.EntityDescription]]:
    # TODO
    return []


def get_overall(
        coords: instaces.Coordinates, radius: instaces.Distance
) -> instaces.LocationDescription:
    # TODO
    return instaces.LocationDescription()
