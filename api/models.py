import time
from django.db import models

import pandas as pd

from api.utils.utils import lamber93_to_gps

# France Network Coverage by Operator: Operateur;x;y;2G;3G;4G
class NetworkCoverage(models.Model):
    operator = models.IntegerField(max_length=100)
    long = models.IntegerField()
    lat = models.IntegerField()
    twoG = models.BooleanField()
    threeG = models.BooleanField()
    fourG = models.BooleanField()

    def __str__(self):
        return self.operator
    
    @classmethod
    def import_csv(cls, csv_file):
        start_time = time.time()
        # read csv with pandas and dump it in the database
        df = pd.read_csv(csv_file, delimiter=';')
        
        # Iterate over DataFrame rows as (index, Series) pairs
        for _, row in df.iterrows():
            x, y = int(row['x']), int(row['y'])
            long, lat = lamber93_to_gps(x, y)
            twoG = row['2G'] == '1'
            threeG = row['3G'] == '1'
            fourG = row['4G'] == '1'
            
            NetworkCoverage.objects.create(
                operator=int(row['Operateur']), 
                long=long,
                lat=lat,
                twoG=twoG, 
                threeG=threeG, 
                fourG=fourG
            )

        print("--- %s seconds ---" % (time.time() - start_time))