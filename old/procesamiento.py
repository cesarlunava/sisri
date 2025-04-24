import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff

# Cargar datos del JSON
with open('data/greenhouse_data.json', 'r') as f:
    data = json.load(f)

# Crear DataFrame con las variables
df = pd.DataFrame({
    'humidity': data['variables']['humidity'],
    'temperature': data['variables']['temperature'],
    'solar_radiation': data['variables']['solar_radiation'],
    'wind_speed': data['variables']['wind_speed'],
    'soil_moisture': data['variables']['soil_moisture'],
    'eto': data['variables']['eto'],
    'irrigation': data['variables']['irrigation']
})

# Calcular matriz de correlación
correlation_matrix = df.corr().values.tolist()

# Actualizar el JSON con las correlaciones reales
data['correlations'] = {
    "labels": ["Humedad", "Temperatura", "Radiación", "Viento", "Humedad Suelo", "ETo", "Riego"],
    "matrix": correlation_matrix
}

# Guardar el JSON actualizado
with open('data/greenhouse_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Matriz de correlación actualizada:")
for row in correlation_matrix:
    print([round(x, 2) for x in row])

# Generar gráficos
# 1. Histogramas de las variables ambientales
histograms = []
for column in ['humidity', 'temperature', 'solar_radiation', 'wind_speed']:
    histograms.append(px.histogram(df, x=column, title=f'Histograma de {column.capitalize()}'))

# 2. Mapa de calor de correlación
heatmap = ff.create_annotated_heatmap(
    z=correlation_matrix,
    x=["Humedad", "Temperatura", "Radiación", "Viento", "Humedad Suelo", "ETo", "Riego"],
    y=["Humedad", "Temperatura", "Radiación", "Viento", "Humedad Suelo", "ETo", "Riego"],
    annotation_text=np.round(correlation_matrix, 2),
    showscale=True
)
heatmap.update_layout(title='Mapa de Calor de Correlación')

# 3. Riego vs. Evapotranspiración (ETo)
scatter_eto = px.scatter(df, x='eto', y='irrigation', title='Riego vs. Evapotranspiración (ETo)', labels={'eto': 'Evapotranspiración', 'irrigation': 'Riego'})

# 4. Riego vs. Humedad del Suelo
scatter_soil_moisture = px.scatter(df, x='soil_moisture', y='irrigation', title='Riego vs. Humedad del Suelo', labels={'soil_moisture': 'Humedad del Suelo', 'irrigation': 'Riego'})

# 5. Riego vs. Otras Variables Ambientales
scatter_temp = px.scatter(df, x='temperature', y='irrigation', title='Riego vs. Temperatura', labels={'temperature': 'Temperatura', 'irrigation': 'Riego'})
scatter_solar = px.scatter(df, x='solar_radiation', y='irrigation', title='Riego vs. Radiación Solar', labels={'solar_radiation': 'Radiación Solar', 'irrigation': 'Riego'})
scatter_wind = px.scatter(df, x='wind_speed', y='irrigation', title='Riego vs. Velocidad del Viento', labels={'wind_speed': 'Velocidad del Viento', 'irrigation': 'Riego'})

# Guardar gráficos como HTML
for i, fig in enumerate(histograms):
    fig.write_html(f'histogram_{i}.html')
heatmap.write_html('heatmap.html')
scatter_eto.write_html('scatter_eto.html')
scatter_soil_moisture.write_html('scatter_soil_moisture.html')
scatter_temp.write_html('scatter_temp.html')
scatter_solar.write_html('scatter_solar.html')
scatter_wind.write_html('scatter_wind.html')
