from pathlib import Path

import pytest
from geopandas import GeoDataFrame  # type: ignore
from shapely.geometry import Point  # type: ignore

from latviastreetify.resolvers import Language, SteetsAndNeighborhoodsResolver


@pytest.fixture
def streets_and_neighborhoods_resolver():
    return SteetsAndNeighborhoodsResolver()


def test_read(streets_and_neighborhoods_resolver):
    result = streets_and_neighborhoods_resolver.read()
    assert isinstance(result, GeoDataFrame)
    assert "geometry" in result.columns
    assert "iela" in result.columns
    assert "adrese" in result.columns
    assert "numurs" in result.columns
    assert "apkaime" in result.columns


def test_get_translation_dict(streets_and_neighborhoods_resolver):
    result = set(streets_and_neighborhoods_resolver.get_translation_dict().values())
    expected_set = set(
        {
            "numurs": "Number",
            "lat": "lat",
            "lon": "lon",
            "iela": "Street",
            "adrese": "Address",
            "geometry": "Geometry",
            "rotation": "Rotation",
            "apkaime": "Name",
            "saite": "Website",
        }.values()
    )
    assert result == expected_set


def test_get_gdf(streets_and_neighborhoods_resolver):
    gdf = streets_and_neighborhoods_resolver.get_gdf(language=Language.EN)
    assert isinstance(gdf, GeoDataFrame)
    assert "Geometry" in gdf.columns
    assert "Street" in gdf.columns
    assert "Address" in gdf.columns
    assert "Number" in gdf.columns
    assert "Name" in gdf.columns

    gdf_lav = streets_and_neighborhoods_resolver.get_gdf()
    assert isinstance(gdf_lav, GeoDataFrame)
    assert "geometry" in gdf_lav.columns
    assert "iela" in gdf_lav.columns
    assert "adrese" in gdf_lav.columns
    assert "numurs" in gdf_lav.columns
    assert "apkaime" in gdf_lav.columns
