import typing as t
import csv

from haversine import inverse_haversine, Direction, haversine
from dataclasses import dataclass
from pathlib import Path

import common.instances as instaces


@dataclass
class Rectangle:
    lt: t.Tuple[float, float]
    rb: t.Tuple[float, float]
    division_ratio: int


def construct_with_coords(
        filename: str, instance: t.Type
) -> t.List[instaces.Entity]:
    res = []
    with open(filename, newline='') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            flags = [bool(i) for i in row[3:]]
            coords = instaces.Coordinates(float(row[1]), float(row[2]))
            id = int(row[0])
            if instance is instaces.RentalPoint:
                other = instaces.RentalKind.BIKE
            elif instance is instaces.TransportStop:
                other = instaces.TransportKind.BUS
            if len(flags) == 0:
                res.append(instance(coords, id, *(other,)))
            else:
                id = int(row[0])
                res.append(instance(coords, id, *flags))
    return res


class DatabaseApi:
    data_paths: t.Dict[str, Path] = {"RentalPoints": Path("tables") / "RentalPoints.csv",
                  "Restaurants": Path("tables") / "Restaurants.csv",
                  "TransportStops": Path("tables") / "TransportStops.csv"}
    tables = {}

    def __init__(self, root: Path):
        self.tables["RentalPoints"] = construct_with_coords(root / self.data_paths["RentalPoints"], instaces.RentalPoint)
        self.tables["Restaurants"] = construct_with_coords(root / self.data_paths["Restaurants"], instaces.Restaraunt)
        self.tables["Restaurants"].sort()
        self.tables["TransportStops"] = construct_with_coords(root / self.data_paths["RentalPoints"], instaces.TransportStop)

    def get_all_entities(
            self, coords: instaces.Coordinates, radius: instaces.Distance
    ) -> t.List[instaces.Entity]:
        res = []
        for table in self.tables.values():
            for row in table:
                if haversine((coords.lat, coords.lon), (row.coords.lat, row.coords.lon)) <= radius:
                    res.append(row)
        return res

    def evaluate_region(self, coords: instaces.Coordinates,
                        radius: instaces.Distance) -> instaces.LocationDescription:
        close_obj = self.get_all_entities(coords, radius)
        restaurants = [value for value in close_obj if type(value) == instaces.Restaraunt]
        stops = [value for value in close_obj if type(value) == instaces.TransportStop]
        rent_points = [value for value in close_obj if type(value) == instaces.RentalPoint]
        #   TODO: res = evaluate_area(radius, restaurants, stops, rent_points)
        return instaces.LocationDescription()

    def evaluate_regions(self, rect: Rectangle):
        all_regions: t.List[t.Tuple[instaces.Coordinates, instaces.LocationDescription]] = []
        width = haversine(rect.lt, (rect.lt[0], rect.rb[1]))
        height = haversine(rect.lt, (rect.rb[0], rect.lt[1]))
        radius = max(height, width) / (2 * rect.division_ratio)
        step_right = width / rect.division_ratio
        step_down = height / rect.division_ratio
        diag = ((step_right / 2) ** 2 + (step_down / 2) ** 2) ** 0.5
        initial: instaces.Coordinates = inverse_haversine(rect.lt, diag,
                                                          Direction.NORTHEAST)
        for i in range(rect.division_ratio):
            cur = inverse_haversine(initial, i * step_down, Direction.NORTHEAST)
            for j in range(rect.division_ratio):
                cur = inverse_haversine(cur, step_right, Direction.WEST)
                tmp = self.evaluate_region(instaces.Coordinates(*cur), radius)
                all_regions.append((instaces.Coordinates(*cur), tmp))

        all_regions.sort(key=lambda x: x[1].score)
        return all_regions

    def get_best_locations(
            self, coords: instaces.Coordinates,
            radius: instaces.Distance,
            n_max_results: int,
            division_ratio: int,
    ) -> t.List[t.Tuple[instaces.Location, instaces.LocationDescription]]:
        lt = inverse_haversine((coords.lat, coords.lon), radius, Direction.NORTH)
        lt = inverse_haversine(lt, radius, Direction.WEST)
        rb = inverse_haversine((coords.lat, coords.lon), radius, Direction.SOUTH)
        rb = inverse_haversine(rb, radius, Direction.EAST)
        rect = Rectangle(lt, rb, division_ratio)
        return [(instaces.Location(i[0], radius), i[1]) for i in self.evaluate_regions(rect)[:n_max_results]]

    def get_overall_about_location(
            self, coords: instaces.Coordinates, radius: instaces.Distance
    ) -> instaces.LocationDescription:
        return self.evaluate_region(coords, radius)

    def get_best_entites(
            self,
            coords: instaces.Coordinates,
            radius: instaces.Distance,
            n_max_results: int,
            preferences: instaces.EntityPreferences,
    ) -> t.List[t.Tuple[instaces.Entity, instaces.EntityDescription]]:
        close_obj = self.get_all_entities(coords, radius)
        if preferences.entity_type == instaces.EntityType.RESTARAUNT:
            restaurants = [(value, instaces.EntityDescription()) for value in close_obj if
                           type(value) == instaces.Restaraunt]
            restaurants.sort()
            return restaurants[:n_max_results]
        elif preferences.entity_type == instaces.EntityType.RENTAL_POINT:
            return [(value, instaces.EntityDescription()) for value in close_obj if
                    type(value) == instaces.TransportStop][:n_max_results]
        elif preferences.entity_type == instaces.EntityType.TRANSPORT:
            return [(value, instaces.EntityDescription()) for value in close_obj if
                    type(value) == instaces.RentalPoint][:n_max_results]
        assert False
        return []
