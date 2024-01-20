import numpy as np
from pyproj import Transformer
from .ege_api import EGE


class CoordTrans():
    """
    Class for transforming coordinates uning Equinor Geodetic Engine.
    Takes in CRS and CT info both using autority code and Equinor alias.

    """
    def __init__(self, crs_from:str, crs_to:str, trans_from:str=None, trans_to:str=None, points:list[float]=None):
        """
        Examples:
        >>> ct = CoordTrans(crs_from="ST_ED50_G4230", crs_to="EPSG:4326", trans_from="EPSG:1612", points=[[10, 60]])
        >>> ct = CoordTrans(crs_from="ST_ED50_UTM31N_P23031_T1613", crs_to="ST_ETRS89_UTM31N_P25831_T1149", points=[[600000, 6714000]])
        >>> ct = CoordTrans(crs_from="EPSG:23031", crs_to="EPSG:25831", trans_from="EPSG:1613", trans_to="EPSG:1149",points=[[600000, 6714000]])
        """
        self.points = points
        self.crs_from = self.__strip_input(crs_from)
        self.crs_to = self.__strip_input(crs_to)
        self.trans_from = trans_from
        self.trans_to = trans_to
        self.crs_from_valid = self.validate_input(self.crs_from)[0]
        self.crs_from_authcode = f"{self.crs_from_valid['authority']}:{self.crs_from_valid['code']}"
        self.crs_to_valid = self.validate_input(self.crs_to)[0]
        if self.trans_from is not None:
            self.trans_from = self.__strip_input(trans_from)
            self.ct_from_valid = self.validate_input(self.trans_from)
        if self.trans_to is not None:
            self.trans_to = self.__strip_input(trans_to)
            self.ct_to_valid = self.validate_input(self.trans_to)

    def validate_input(self, entity):
        """
        Validates the input parameters.

        Examples:
        >>> ct = CoordTrans(crs_from="ST_ED50_G4230", crs_to="EPSG:4326",  trans_from="EPSG:1612", points=[[10,60]])
        >>> ct.validate_input(ct.crs_from)
        [{'code': 4230, 'name': 'ST_ED50_G4230', 'naming_system': 'Equinor', 'authority': 'EPSG', 'uom': 'degree', 'coord_sys': 'ellipsoidal', 'type': 'geographic 2D', 'is_alias': True, 'alias': [{'name': 'ED50', 'naming_system': 'EPSG'}, {'name': 'GCS_European_1950', 'naming_system': 'ESRI'}]}]
        """
        response = EGE().validate_input(entity).get('results')
        if response is None:
            raise ValueError(f"{entity} is not a valid entity")
        return response


    def __strip_input(self, user_input):
        """Strips input strings"""
        return user_input.strip().replace(" ","")


    def transform_pointlist(self) -> list[float]:
        """
        Transform a list of points and return a list
        of transformed coordinates

        Examples:
        >>> ct = CoordTrans(crs_from="EPSG:4230", crs_to="EPSG:4326",  trans_from="EPSG:1612", points=[[10,60]])
        >>> ct.transform_pointlist()
        [[9.99860677505385, 59.999554562447024]]
        """

        pipeline = self.get_pipeline()
        trans_coords = self.transform_from_pipeline(self.points, pipeline)
        return trans_coords


    def get_pipeline(self) -> str:
        """
        Return a PROJ transformation pipeline from Equinor Geodetic Engine.
        Examples:
        >>> ct = CoordTrans(crs_from="ST_ED50_G4230", crs_to="EPSG:4326", trans_from="EPSG:1612")
        >>> ct.get_pipeline()
        '+proj=pipeline +step +proj=push +v_3 +step +proj=cart +ellps=intl +step +proj=helmert +x=-116.641 +y=-56.931 +z=-110.559 +rx=0.893 +ry=0.921 +rz=-0.917 +s=-3.52 +convention=position_vector +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3'
        """
        crs_from = self.crs_from
        if self.trans_from:
            crs_from = f"({self.crs_from},{self.trans_from})"

        crs_to = self.crs_to
        if self.trans_to:
            crs_to = f"({self.crs_to},{self.trans_to})"
        response = EGE().get_pipeline(crs_from, crs_to)
        return response['pipeline']


    def transform_from_pipeline(self, coordinates, pipeline) -> list:
        """
        Transform a list of points using PROJ pipeline and return a list
        of transformed coordinates.

        Examples:
        >>> ct = CoordTrans(crs_from="ST_ED50_G4230", crs_to="EPSG:4326",  trans_from="EPSG:1612")
        >>> ct.transform_from_pipeline([[10,60]],ct.get_pipeline())
        [[9.99860677505385, 59.999554562447024]]
        """
        transformer = Transformer.from_pipeline(pipeline)
        np_coordinates = np.array(coordinates, dtype=np.double)
        x, y = np_coordinates.T # extract x and y
        tx, ty = transformer.transform(x, y)
        transformed_coordinates = np.vstack([tx, ty]).T.tolist()

        return transformed_coordinates


if __name__ == "__main__":
    import doctest
    doctest.testmod()