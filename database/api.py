import typing as t
import csv

from haversine import inverse_haversine, Direction

import common.instances as instaces
import haversine as hs
from dataclasses import dataclass


@dataclass
class Rectangle:
    lt: instaces.Coordinates
    rb: instaces.Coordinates
    division_ratio: int


def construct_with_coords(
        filename: str, instance: t.Type
) -> t.List[instaces.Entity]:
    res = []
    with open(filename, newline='') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            flags = [bool(i) for i in row[2:]]
            if flags is None:
                res.append(instance(int(row[0]),
                                    instaces.Coordinates(float(row[1]), float(row[2]))))
            else:
                res.append(instance(int(row[0]),
                                    instaces.Coordinates(float(row[1]), float(row[2])), *flags))
    return res


class DatabaseApi:
    data_paths = {"RentalPoints": "./table/RentalPoints.csv",
                  "Restaurants": "./table/Restaurants.csv",
                  "TransportStops": "./table/TransportStops.csv"}
    tables = {}

    def __init__(self):
        self.tables["RentalPoints"] = construct_with_coords(self.data_paths["RentalPoints"], instaces.RentalPoint)
        self.tables["Restaurants"] = construct_with_coords(self.data_paths["Restaurants"], instaces.Restaraunt)
        self.tables["Restaurants"].sort()
        self.tables["TransportStops"] = construct_with_coords(self.data_paths["RentalPoints"], instaces.TransportStop)

    def get_all_entities(
            self, coords: instaces.Coordinates, radius: instaces.Distance
    ) -> t.List[instaces.Entity]:
        res = []
        for table in self.tables.values():
            for row in table:
                if hs.haversine((coords.lat, coords.lon), (table.coords.lat, table.coords.lon)) <= radius:
                    res.append(row)
        return res

    def evaluate_region(self, coords: instaces.Coordinates,
                        radius: instaces.Distance) -> t.Tuple[float, instaces.LocationDescription]:
        close_obj = self.get_all_entities(coords, radius)
        restaurants = [value for value in close_obj if type(value) == instaces.Restaraunt]
        stops = [value for value in close_obj if type(value) == instaces.TransportStop]
        rent_points = [value for value in close_obj if type(value) == instaces.RentalPoint]
        #   TODO: res = evaluate_area(radius, restaurants, stops, rent_points)
        return (0, instaces.LocationDescription("Evaluation of region"))

    def evaluate_regions(self, rect: Rectangle):
        all_regions: t.List[t.Tuple[instaces.Coordinates, float, instaces.LocationDescription]] = []
        width = hs.haversine((rect.lt.lat, rect.lt.lon), (rect.lt.lat, rect.rb.lon))
        height = hs.haversine((rect.lt.lat, rect.lt.lon), (rect.rb.lat, rect.lt.lon))
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
                all_regions.append((instaces.Coordinates(*cur), tmp[0], tmp[1]))

        all_regions.sort(key=lambda x: x[1])
        return all_regions

    def get_best_locations(
            self, coords: instaces.Coordinates,
            radius: instaces.Distance,
            n_max_results: int,
            division_ratio: int,
    ) -> t.List[t.Tuple[instaces.Location, instaces.LocationDescription]]:
        lt = inverse_haversine((coords.lat, coords.lon), radius, Direction.NORTH)
        lt = inverse_haversine((lt.lat, lt.lon), radius, Direction.WEST)
        rb = inverse_haversine((coords.lat, coords.lon), radius, Direction.SOUTH)
        rb = inverse_haversine((rb.lat, rb.lon), radius, Direction.EAST)
        rect = Rectangle(lt, rb, division_ratio)
        return [(instaces.Location(i[0]), i[2]) for i in self.evaluate_regions(rect)[:n_max_results]]


def get_overall_about_location(
        self, coords: instaces.Coordinates, radius: instaces.Distance
) -> instaces.LocationDescription:
    return self.evaluate_region(coords, radius)


def get_best_entites(

    coords: instaces.Coordinates,
    radius: instaces.Distance,
    n_max_results: int,
    preferences: instaces.EntityPreferences,

) -> t.List[t.Tuple[instaces.Entity, instaces.EntityDescription]]:

    return []
