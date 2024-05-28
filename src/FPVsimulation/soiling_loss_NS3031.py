import geopandas as gpd
from shapely.geometry import Point

# Municipality centers is sourced from https://www.kartverket.no/til-lands/fakta-om-norge/noregs-midtpunkt
soiling_data = {
    'municipality' : ['Stavanger', 'Oslo', 'Trondheim', 'Tromsø', 
                      'Bergen', 'Kristiansand', 'Lillehammer', 'Drammen', 
                      'Skien', 'Tønsberg', 'Fredrikstad'],
    'geometry' : [Point(25308.63,6589396.19), 
                  Point(262335.42,6656953.39), 
                  Point(271498.57,7031656.93),
                  Point(658360.12,7730850.47),
                  Point(-28836.01,6730622.71),
                  Point(80506.37,6471393.70),
                  Point(251868.28,6785781.36),
                  Point(227320.62,6629577.22),
                  Point(185790.29,6581475.50),
                  Point(232453.14,6590090.30),
                  Point(267715.29,6572429.07)],
    'soiling' : [[15,15,2,2,2,2,2,2,2,2,2,15], # Stavanger
                 [60,75,60,2,2,2,2,2,2,2,15,45], # Oslo
                 [60,75,45,8,2,2,2,2,2,2,15,54], # Trondheim
                 [75,75,75,75,2,2,2,2,2,30,45,60], # Tromsø
                 [15,30,15,2,2,2,2,2,2,2,2,23], # Bergen
                 [45,75,45,2,2,2,2,2,2,2,2,38], # Kristiansand
                 [75,75,75,30,2,2,2,2,2,2,30,75], # Lillehammer 
                 [75,75,60,8,2,2,2,2,2,2,15,53], # Drammen
                 [75,75,60,8,2,2,2,2,2,2,15,53], #Skien
                 [45,75,60,8,2,2,2,2,2,2,8,38], # Tønsberg
                 [15,30,15,8,2,2,2,2,2,2,2,8] # Fredrikstad
                 ]
}

soiling_loss_NS3031_gdf = gpd.GeoDataFrame(soiling_data, geometry='geometry', crs='EPSG:32633').to_crs('EPSG:4326')
