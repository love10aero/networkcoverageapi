import time
from django.contrib.gis.db import models
import pandas as pd
from api.utils.utils import lamber93_to_gps

class NetworkCoverage(models.Model):
    operator = models.CharField(max_length=100)
    location = models.PointField(geography=True)
    twoG = models.BooleanField()
    threeG = models.BooleanField()
    fourG = models.BooleanField()

    def __str__(self):
        return self.operator
    
    @classmethod
    def import_csv(cls, csv_file):
        start_time = time.time()
        df = pd.read_csv(csv_file, delimiter=';')
        
        for _, row in df.iterrows():
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

        print("--- %s seconds ---" % (time.time() - start_time))
