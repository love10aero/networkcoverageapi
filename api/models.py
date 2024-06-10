import time
from django.contrib.gis.db import models
import pandas as pd
from api.utils.converters import lamber93_to_gps


class NetworkCoverage(models.Model):
    """
    Model to store network coverage information for different operators.

    Attributes:
        operator (str): The operator code.
        location (Point): The geographic location of the network coverage.
        twoG (bool): Indicates if 2G coverage is available.
        threeG (bool): Indicates if 3G coverage is available.
        fourG (bool): Indicates if 4G coverage is available.
    """
    operator = models.CharField(max_length=100)
    location = models.PointField(geography=True)
    twoG = models.BooleanField()
    threeG = models.BooleanField()
    fourG = models.BooleanField()

    def __str__(self):
        return str(self.operator)

    @classmethod
    def import_csv(cls, csv_file):
        """
        Imports network coverage data from a CSV file and saves it to the database.

        Args:
            csv_file (str): The path to the CSV file containing network coverage data.

        Returns:
            None
        """
        start_time = time.time()
        df = pd.read_csv(csv_file, delimiter=';')

        for _, row in df.iterrows():
            # check if there is any Nan in thhe row, if so, skip
            if row.isnull().values.any():
                continue

            # Convert Lambert93 coordinates to GPS (WGS84)
            x, y = int(row['x']), int(row['y'])
            long, lat = lamber93_to_gps(x, y)
            twoG = row['2G'] == 1.0
            threeG = row['3G'] == 1.0
            fourG = row['4G'] == 1.0

            NetworkCoverage.objects.create(
                operator=int(row['Operateur']),
                location=f'POINT({long} {lat})',
                twoG=twoG,
                threeG=threeG,
                fourG=fourG
            )

        print(f"--- {round(time.time() - start_time, 2)} seconds ---")
