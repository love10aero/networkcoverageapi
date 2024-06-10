import pyproj


def lamber93_to_gps(x, y):
    """
    Converts Lambert93 coordinates to GPS coordinates.

    :param x: The x-coordinate in Lambert93 projection.
    :type x: int or float
    :param y: The y-coordinate in Lambert93 projection.
    :type y: int or float
    :return: A tuple of the longitude and latitude in GPS coordinates.
    :rtype: tuple
    """
    transformer = pyproj.Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
    long, lat = transformer.transform(x, y)
    return long, lat


def get_operator_name(operator_id):
    """
    Retrieves the name of an operator based on its ID.

    Args:
        operator_id (str): The ID of the operator.

    Returns:
        str: The name of the operator if found, otherwise "Operator not found".
    """
    # Codes extracted from source: https://fr.wikipedia.org/wiki/Mobile_Network_Code#Tableau_des_MNC_pour_la_France_m%C3%A9tropolitaine
    operator_dict = {
        '20801': 'Orange',
        '20802': 'Orange',
        '20803': 'MobiquiThings',
        '20804': 'Netcom Group',
        '20805': 'Globalstar Europe',
        '20806': 'Globalstar Europe',
        '20807': 'Globalstar Europe',
        '20808': 'SFR',
        '20809': 'SFR',
        '20810': 'SFR',
        '20811': 'SFR',
        '20812': 'Hewlett-Packard France',
        '20813': 'SFR',
        '20814': 'RFF',
        '20815': 'Free mobile',
        '20816': 'Free mobile',
        '20817': 'Legos',
        '20818': 'Voxbone',
        '20819': 'Altitude infrastructure',
        '20820': 'Bouygues Telecom',
        '20821': 'Bouygues Telecom',
        '20822': 'Transatel Mobile',
        '20823': 'Syndicat mixte ouvert Charente numérique',
        '20824': 'MobiquiThings',
        '20825': 'Lycamobile',
        '20826': 'Bouygues Télécom Business distribution',
        '20827': 'Coriolis Télécom',
        '20828': 'Airmob',
        '20829': 'Cubic telecom France',
        '20830': 'Symacom',
        '20831': 'Mundio Mobile',
        '20832': 'Orange',
        '20834': 'Cellhire France',
        '20835': 'Free mobile',
        '20886': 'SEM@FOR77',
        '20888': 'Bouygues Telecom',
        '20889': 'Fondation b-com',
        '20890': 'Association Images & Réseaux',
        '20891': 'Orange',
        '20892': 'Association Plate-forme Telecom',
        '20893': 'Thales communications',
        '20894': 'Halys',
        '20895': 'Orange',
        '20896': 'Axione',
        '20897': 'Thales communications',
        '20898': 'Air France'
    }
    operator = operator_dict.get(operator_id, 'Unknown')
    return operator
