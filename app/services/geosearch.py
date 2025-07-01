import math
from typing import List, Tuple

from app.models.organization import Organization


class GeoSearchService:
    """
    Сервис для географического поиска организаций.
    Отвечает за расчёт расстояний и фильтрацию по геозонам.
    """

    EARTH_RADIUS_KM: float = 6371.0  # радиус Земли в километрах

    @classmethod
    def haversine_distance(
            cls,
            lat1: float,
            lon1: float,
            lat2: float,
            lon2: float
    ) -> float:
        """
        Вычислить расстояние между двумя точками на поверхности Земли
        по формуле Гаверсинуса.
        """
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
                math.sin(dlat / 2) ** 2
                + math.cos(math.radians(lat1))
                * math.cos(math.radians(lat2))
                * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return cls.EARTH_RADIUS_KM * c

    def filter_by_radius(
            self,
            orgs: List[Organization],
            center: Tuple[float, float],
            radius_km: float
    ) -> List[Organization]:
        """
        Отфильтровать организации, чьи координаты в пределах заданного радиуса.
        :param orgs: список организаций с атрибутом building.latitude и building.longitude
        :param center: кортеж (lat, lon) центра
        :param radius_km: радиус поиска в км
        """
        lat0, lon0 = center
        result: List[Organization] = []
        for org in orgs:
            lat, lon = org.building.latitude, org.building.longitude
            if self.haversine_distance(lat0, lon0, lat, lon) <= radius_km:
                result.append(org)
        return result

    def filter_by_bbox(
            self,
            orgs: List[Organization],
            sw: Tuple[float, float],
            ne: Tuple[float, float]
    ) -> List[Organization]:
        """
        Отфильтровать организации, находящиеся внутри прямоугольника,
        заданного координатами юго-западного (sw) и северо-восточного (ne) углов.
        """
        sw_lat, sw_lon = sw
        ne_lat, ne_lon = ne
        return [
            org for org in orgs
            if sw_lat <= org.building.latitude <= ne_lat and sw_lon <= org.building.longitude <= ne_lon
        ]
