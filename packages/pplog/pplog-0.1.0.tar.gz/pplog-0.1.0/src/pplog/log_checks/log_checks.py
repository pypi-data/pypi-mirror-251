""" LogEvent classes (Checks) """


from abc import ABC

from pyspark.sql import DataFrame as SparkDF


#  pylint:disable=fixme,too-few-public-methods
class _ICheck(ABC):
    """Abtract log checking class"""

    #  TODO


class CheckDataFrameCount(_ICheck):
    """Spark DataFrame Count Checker"""

    def __init__(self, sdf: SparkDF, comparison_function: str) -> None:
        self._sdf = sdf
        self._comparison_function = comparison_function
        self._sdf_count = sdf.count()
