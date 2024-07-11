import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff

# Cargar los datos
df = pd.read_csv('/Users/aleyanez/Documents/GitHub/sisri/cucumber_greenhouse_data_penman-2.csv')

# Generar gráficos
# 1. Histogramas de las variables ambientales
histograms = []
for column in ['humidity', 'temperature', 'solar_radiation', 'wind_speed']:
    histograms.append(px.histogram(df, x=column, title=f'Histograma de {column.capitalize()}'))

# 2. Mapa de calor de correlación
correlation_matrix = df.corr()
heatmap = ff.create_annotated_heatmap(
    z=correlation_matrix.values,
    x=list(correlation_matrix.columns),
    y=list(correlation_matrix.index),
    annotation_text=correlation_matrix.round(2).values,
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
