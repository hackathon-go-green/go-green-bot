import typing as t
import csv
from functools import cmp_to_key

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
            flags = [bool(int(i)) for i in row[3:] if len(i) > 0]
            coords = instaces.Coordinates(float(row[1]), float(row[2]))
            other = []
            id = int(row[0])
            if instance is instaces.RentalPoint:
                other.append(instaces.RentalKind.BIKE)
            elif instance is instaces.TransportStop:
                other.append(instaces.TransportKind.BUS)
            res.append(instance(coords, id, *tuple(flags), *tuple(other)))
    return res


class DatabaseApi:
    data_paths: t.Dict[str, Path] = {"RentalPoints": Path("tables") / "RentalPoints.csv",
                                     "Restaurants": Path("tables") / "Restaurants.csv",
                                     "TransportStops": Path("tables") / "TransportStops.csv"}
    tables = {}

    def __init__(self, root: Path):
        self.tables["RentalPoints"] = construct_with_coords(root / self.data_paths["RentalPoints"],
                                                            instaces.RentalPoint)
        self.tables["Restaurants"] = construct_with_coords(root / self.data_paths["Restaurants"], instaces.Restaraunt)
        self.tables["Restaurants"].sort(key=cmp_to_key(instaces.compare_restaurants), reverse=True)
        self.tables["TransportStops"] = construct_with_coords(root / self.data_paths["RentalPoints"],
                                                              instaces.TransportStop)

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
        return instaces.LocationDescription(score=self.area_score(radius, stops, restaurants, rent_points))

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

        all_regions.sort(key=lambda x: x[1].score, reverse=True)
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
            restaurants = [value for value in close_obj if
                           type(value) == instaces.Restaraunt]
            return [(i, instaces.EntityDescription(i.descr(), i.rank())) for i in restaurants][:n_max_results]
        elif preferences.entity_type == instaces.EntityType.RENTAL_POINT:
            return [(value, instaces.EntityDescription()) for value in close_obj if
                    type(value) == instaces.TransportStop][:n_max_results]
        elif preferences.entity_type == instaces.EntityType.TRANSPORT:
            return [(value, instaces.EntityDescription()) for value in close_obj if
                    type(value) == instaces.RentalPoint][:n_max_results]
        return []

    # FIRST Function - busses ±score calculator

    def bus_rad_score(self, radius, busStopss):
        bad = "Bad"
        poor = "Poor"
        decent = "Decent"
        good = "Good"
        excellent = "Excellent"
        errorMsg = "Something went wrong"
        stops = len(busStopss)
        if radius <= 0.5:
            if stops >= 3:
                return excellent
            elif stops >= 1:
                return good
            else:
                return poor
        elif radius <= 1:
            if stops >= 6:
                return excellent
            elif stops >= 3:
                return good
            elif stops == 2:
                return poor
            else:
                return bad
        elif radius <= 3:
            if stops >= 12:
                return excellent
            elif stops >= 8:
                return good
            elif stops >= 5:
                return decent
            elif stops >= 3:
                return poor
            else:
                return bad
        elif radius <= 5:
            if stops >= 32:
                return excellent
            elif stops >= 20:
                return good
            elif stops >= 13:
                return decent
            elif stops >= 5:
                return poor
            else:
                return bad
        elif radius >= 5:
            area = 3.14 * radius ** 2
            ratio = stops / (area / 5.5)
            if ratio >= 1.3:
                return excellent
            elif ratio >= 1.15:
                return good
            elif ratio >= 0.85:
                return decent
            elif ratio >= 0.75:
                return poor
            else:
                return bad
        else:
            return errorMsg + " - busRadScore"

    # FIRST END

    # should return the restaurant's, given
    # as a parameter, score _ Not Necessarily
    # the scale from 1 to 10
    # also requested by - KATE -

    # FUN END

    # CHECK RETURN VALUES, last things
    # - they have a comment above -
    # SECOND Function - restaurantTop 3 creator and ±score calculator
    def restr_score(self, radius, restaurants):
        sum = 0
        for x in restaurants:
            sum += x.rank()
        return sum / (len(restaurants)+1)

    # SECOND END

    # THIRD Function - rental ±score calculator
    def rental(self, radius, rentalPoints):
        bad = "Bad"
        poor = "Poor"
        decent = "Decent"
        good = "Good"
        excellent = "Excellent"
        errorMsg = "Something went wrong"
        if (radius < 0.1):
            return "Huh, well someone messed up - rental_fun"
        # rentalPlaces = rentalPoints.count()
        rentalPlaces = len(rentalPoints)

        if (radius <= 2.5):
            if (rentalPlaces >= 1):
                return excellent
        elif (radius <= 5):
            if (rentalPlaces >= 3):
                return excellent
            elif (rentalPlaces >= 1):
                return good
            else:
                return poor
        elif (radius <= 10):
            if (rentalPlaces >= 7):
                return excellent
            elif (rentalPlaces >= 5):
                return good
            elif (rentalPlaces >= 3):
                return decent
            elif (rentalPlaces >= 1):
                return poor
            else:
                return bad
        # I'd put a limit,
        # just to be more foolProof
        # this time I'll just do it
        # like this tho - please put the
        # right input :) -
        else:
            area = 3.14 * radius ** 2
            area = area ** 0.5
            # 5.5 is not random, it's just kinda close
            # to giving the actual area of Berlin
            # GEneralizing - BAD - Ik, with time we'll
            # do it better '-_-'
            ratio = rentalPlaces / (area / 5.5)
            if (ratio >= 0.9):
                return excellent
            elif (ratio >= 0.7):
                return good
            elif (ratio >= 0.55):
                return decent
            elif (ratio >= 0.4):
                return poor
            else:
                return bad

    # THIRD END

    # FOURTH and final Function
    # It aims to generate a score for the Entire Area
    def area_score(self, radius, busStops, restaurants, rentalPoints):
        bad = "Bad"
        poor = "Poor"
        decent = "Decent"
        good = "Good"
        excellent = "Excellent"
        errorMsg = "Something went wrong"
        scorePublicTrasns = self.bus_rad_score(radius, busStops)
        # I don't know if this will work - literally no clue
        # scoreRestaurants should return a special defined class ?

        resultRest = self.restr_score(radius, restaurants)
        scoreRest = resultRest * 1.25
        scoreRental = self.rental(radius, rentalPoints)

        if (scorePublicTrasns == excellent):
            scorePublicTrasns = 10
        elif (scorePublicTrasns == good):
            scorePublicTrasns = 8
        elif (scorePublicTrasns == decent):
            scorePublicTrasns = 6.25
        elif (scorePublicTrasns == poor):
            scorePublicTrasns = 5
        elif (scorePublicTrasns == bad):
            scorePublicTrasns = 4

        if (scoreRental == excellent):
            scoreRental = 10
        elif (scoreRental == good):
            scoreRental = 8
        elif (scoreRental == decent):
            scoreRental = 6.25
        elif (scoreRental == poor):
            scoreRental = 5
        elif (scoreRental == bad):
            scoreRental = 4

        if (scoreRental == scorePublicTrasns and scorePublicTrasns == 4):
            areaScore = scoreRest * 1 / 3
        elif (scoreRental == scorePublicTrasns and scorePublicTrasns > 4):
            areaScore = scoreRental * 2 / 3 + scoreRest * 1 / 3
        else:
            areaScore = (scorePublicTrasns + scorePublicTrasns + scoreRest) / 3

        return areaScore

    # FOURTH END
