# Network Coverage API

## Overview

This API allows querying the network coverage for a given address, providing information on the availability of 2G, 3G, and 4G coverage for each operator in France.

## Features

- **Network Coverage Information:** Retrieves 2G, 3G, and 4G network coverage for each operator based on the provided address.
- **Address to Coordinates Conversion:** Utilizes the `adresse.data.gouv.fr` API to convert textual addresses into geographic coordinates.
- **CSV Data Import:** Imports network coverage data from a CSV file containing Lambert93 coordinates.

<img src="https://github.com/love10aero/networkcoverageapi/blob/main/docs/logic.png"/>


## Installation

### Prerequisites

- Python 3.8+
- Django 5.0
- PostGIS-enabled PostgreSQL database
- GDAL library

### Setting Up the Environment

1. **Clone the Repository:**

    ```sh
    git clone <repository_url>
    cd networkcoverageapi
    ```

2. **Create a Virtual Environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Configure the Database:**

    Ensure that your PostgreSQL database has PostGIS installed:

    ```sql
    CREATE EXTENSION postgis;
    ```

    Confirm the installation:

    ```sql
    SELECT postgis_full_version();
    ```

5. **Set Up Environment Variables:**
1. 
    ```sh
    export DJANGO_SETTINGS_MODULE=networkcoverageapi.settings
    ```

    ```env
    POSTGRES_DB=<your_database_name>
    POSTGRES_USER=<your_database_user>
    POSTGRES_PASSWORD=<your_database_password>
    ```

6. **Apply Migrations:**

    ```sh
    python manage.py migrate
    ```

7. **Load Initial Data:**

    Ensure you have the CSV file (`2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv`) in the `docs` directory, then run:

    ```sh
    python manage.py shell
    ```

    Once the shell is running, run the following command to load the initial data:

    ```sh

    from api.models import NetworkCoverage
    from django.conf import settings
    csv_file_path = settings.BASE_DIR / 'docs' / '2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv'
    NetworkCoverage.import_csv(csv_file_path)

    ```

## Usage

### Starting the Development Server

```sh
python manage.py runserver
```	

## API Endpoints
### Get Network Coverage
#### Endpoint
```bash
GET /api/v1/coverage/?q=<address>
```	

#### Example

```bash
GET /api/v1/coverage/?q=42+rue+papernest+75011+Paris
```

#### Response
```json
{
    "SFR": {
        "location": [
            2.4235892377054817,
            48.95889881296555
        ],
        "distance_km": 1.5212682488999998,
        "2G": true,
        "3G": true,
        "4G": true
    },
    "Bouygues Telecom": {
        "location": [
            2.421175026461827,
            48.98439890573347
        ],
        "distance_km": 1.58866826603,
        "2G": true,
        "3G": true,
        "4G": true
    },
    "Free mobile": {
        "location": [
            2.410978758312727,
            48.97509605708831
        ],
        "distance_km": 1.51650544801,
        "2G": false,
        "3G": true,
        "4G": true
    },
    "Orange": {
        "location": [
            2.4151181073123005,
            48.97749931591031
        ],
        "distance_km": 1.33300976902,
        "2G": true,
        "3G": true,
        "4G": true
    }
}
```	
## Testing
Run the following command to execute tests:
```bash	
python manage.py test
```

## Docker

To run the application using Docker, you can follow the instructions provided in the [Dockerfile](Dockerfile) file. 
NOTE: The implementation is of the docker is not complete, since OSGeo4W is not installed in the container. 


## Acknowledgements

- [adresse.data.gouv.fr](https://adresse.data.gouv.fr/)
- Special thanks to all contributors and maintainers of the libraries and tools used in this project.

## Author

Lovejinder Singh
