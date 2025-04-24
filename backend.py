import ee
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# Initialize Earth Engine with your credentials
try:
    ee.Initialize(project='theta-totem-457716-c5')
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project='theta-totem-457716-c5')

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/data/greenhouse_data.json')
def serve_greenhouse_data():
    return send_from_directory('data', 'greenhouse_data.json')

@app.route('/extract_variables', methods=['POST'])
def extract_variables():
    data = request.get_json()
    polygon = data['polygon']  # List of [lon, lat] pairs

    # Convert to GeoJSON polygon for Earth Engine
    geom = ee.Geometry.Polygon([polygon])

    # Example: Get median NDVI from Sentinel-2 for the last month
    collection = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterBounds(geom) \
        .filterDate('2024-03-23', '2024-04-23') \
        .sort('CLOUDY_PIXEL_PERCENTAGE')

    image = collection.first()
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    mean_dict = ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geom,
        scale=10,
        maxPixels=1e7
    )
    ndvi_value = mean_dict.get('NDVI').getInfo()

    # You can add more variables here, e.g., from Landsat or NISAR when available

    return jsonify({
        "NDVI": ndvi_value,
        "Polygon": polygon
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
