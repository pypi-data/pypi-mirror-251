"""
module that resolve the streets and neighborhoods of Latvia
"""
from abc import ABC, abstractmethod
from enum import Enum
from os import environ
from pathlib import Path
from typing import Dict

import geopandas as gpd  # type: ignore


class Language(str, Enum):
    EN = "EN"
    LAV = "LAV"


class Resolver(ABC):
    def __init__(self) -> None:
        self._gdf = self.read()
        super().__init__()

    @abstractmethod
    def read(self) -> gpd.GeoDataFrame:
        ...

    @abstractmethod
    def get_translation_dict(self) -> Dict[str, str]:
        ...

    def get_gdf(self, language: Language = Language.LAV):
        match language:
            case language.EN:
                return self._gdf.rename(columns=self.get_translation_dict())
            case Language.LAV | _:
                return self._gdf


class SteetsResolver(Resolver):
    def read(self) -> gpd.GeoDataFrame:
        if filepath := environ.get("STREETS_FILE"):  # type: ignore
            filepath = Path(filepath)  # type: ignore
            print(f"will use external file {filepath}")
        else:
            filepath = Path(__file__).parent / "data/adreses.shp"  # type: ignore
        gdf = gpd.read_file(filepath).to_crs("epsg:4326")
        gdf = gdf.apply(
            lambda col: col.map(lambda s: s.lower() if isinstance(s, str) else s)
        )
        gdf["adrese"] = gdf["adrese"].str.replace(" k-", "k-")
        # remove the duplicates based on the address column
        gdf = gdf.drop_duplicates(subset="adrese", keep="first")
        # Convert POINT to Latitude and longitude
        gdf["lat"] = gdf["geometry"].y
        gdf["lon"] = gdf["geometry"].x

        return gdf.dropna()

    def get_translation_dict(self) -> Dict[str, str]:
        translation_dict = {
            "numurs": "Number",
            "lat": "lat",
            "lon": "lon",
            "iela": "Street",
            "adrese": "Address",
            "geometry": "Geometry",
            "rotation": "Rotation",
        }
        return translation_dict


class NeighborhoodsResolver(Resolver):
    def read(self) -> gpd.GeoDataFrame:
        if filepath := environ.get("NEIGHBORHOODS_FILE"):  # type: ignore
            filepath = Path(filepath)  # type: ignore
            print(f"will use external file {filepath}")
        else:
            filepath = Path(__file__).parent / "data/Apkaimes.shp"  # type: ignore
        gdf = gpd.read_file(filepath).to_crs("epsg:4326")
        gdf = gdf.apply(
            lambda col: col.map(lambda s: s.lower() if isinstance(s, str) else s)
        )
        return gdf.dropna()

    def get_translation_dict(self) -> Dict[str, str]:
        translation_dict = {
            "apkaime": "Name",
            "saite": "Website",
            "geometry": "Geometry",
        }
        return translation_dict


class SteetsAndNeighborhoodsResolver(Resolver):
    def __init__(self) -> None:
        self._streets_resolver = SteetsResolver()
        self._neighborhoods_resolver = NeighborhoodsResolver()
        super().__init__()

    def read(self) -> gpd.GeoDataFrame:
        streets_gdf = self._streets_resolver.get_gdf()
        neighborhoods_gdf = self._neighborhoods_resolver.get_gdf()
        return streets_gdf.sjoin(
            neighborhoods_gdf, how="left", predicate="within"
        ).dropna()

    def get_translation_dict(self) -> Dict[str, str]:
        all_dict: Dict[str, str] = dict()
        all_dict.update(**self._streets_resolver.get_translation_dict())
        all_dict.update(**self._neighborhoods_resolver.get_translation_dict())
        return all_dict
