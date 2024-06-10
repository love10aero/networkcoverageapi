from api.models import NetworkCoverage
from django.conf import settings

csv_file_path = settings.BASE_DIR / 'docs' / '2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv'
NetworkCoverage.import_csv(csv_file_path)
