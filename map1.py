import folium
import pandas


def color_producer(elevation):
    if elevation <= 1000:
        return 'green'
    elif elevation > 1000 and el <= 2000:
        return 'red'
    else:
        return 'blue'


data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[38, -99], zoom_start=5, tiles='Stamen Terrain')
fgv = folium.FeatureGroup(name='Volcanoes Layer')

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=(lt, ln), radius=6, popup=folium.Popup(iframe),
                                      fill_color=color_producer(el), color='grey', fill_opacity=0.85))

fgp = folium.FeatureGroup(name='Population Layer')

fgp.add_child(folium.GeoJson(data=(open('world.json', 'r', encoding='utf-8-sig').read()),
                             style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 20000000
                             else 'orange' if 30000000 >= x['properties']['POP2005'] < 40000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())  # put this line after "map.add_child(fg)" otherwise we lose layer created before

map.save('Map1.html')
