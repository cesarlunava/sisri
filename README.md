# SISRI - Sistema Inteligente de Riego 🌱💧

## 🚀 Descripción del Proyecto
SISRI (Sistema Inteligente de Riego) es una solución integral desarrollada por Blue Basin que revoluciona la agricultura mediante el uso de tecnología avanzada. Nuestro sistema combina IoT, procesamiento de imágenes satelitales y análisis de datos para optimizar el uso del agua, fertilizantes y energía, creando sistemas agrícolas más sostenibles y productivos.

## 🌟 Características Principales
- **Integración con Earth Engine** 🛰️: Análisis de imágenes satelitales para monitoreo de cultivos
- **Gestión Inteligente del Agua** 💧: Reduce el consumo de agua hasta un 40% mediante algoritmos de riego precisos
- **Analítica Avanzada** 📊: Visualizaciones interactivas con Plotly y procesamiento con Pandas
- **Monitoreo IoT** 🌡️: Sistema Raspberry Pi para seguimiento en tiempo real de variables ambientales
- **Mapas Interactivos** 🗺️: Visualización geográfica con integración de datos satelitales
- **Dashboard Moderno** 📈: Interface intuitiva con múltiples visualizaciones (heatmaps, histogramas, scatter plots)
- **API REST** 🔄: Backend en Flask para procesamiento y entrega de datos

## 🛠️ Stack Tecnológico
### Frontend
- HTML5/CSS3 con diseño responsivo
- JavaScript para interactividad
- Visualizaciones avanzadas con Plotly
- Múltiples páginas para diferentes funcionalidades (dashboard, análisis, predicciones)

### Backend
- Python con Flask
- Google Earth Engine para análisis satelital
- SQLAlchemy para gestión de base de datos
- Pandas y NumPy para procesamiento de datos

### IoT
- Raspberry Pi como nodo central
- Sensores de:
  - Temperatura
  - Humedad del suelo
  - Radiación solar
  - Velocidad del viento
- Sistema de logging automático

## 📊 Componentes Principales
- **Sistema de Autenticación** 🔐: Login y registro de usuarios
- **Dashboard Principal** 📊: Visualización en tiempo real de métricas clave
- **Módulo de Predicciones** 🔮: Análisis predictivo de necesidades de riego
- **Historial de Datos** 📜: Registro histórico de variables monitoreadas
- **Análisis Avanzado** 📈: Herramientas de análisis estadístico
- **Mapas de Calor** 🗺️: Visualización espacial de variables

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- Node.js (para algunas dependencias frontend)
- Cuenta de Google Earth Engine
- Raspberry Pi (opcional, para monitoreo IoT)

### Pasos de Instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/sisri.git
   ```

2. Instalar dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno:
   - Crear archivo `.env` con credenciales necesarias
   - Configurar proyecto de Earth Engine

4. Iniciar el servidor:
   ```bash
   python backend.py
   ```

## 📈 Estructura de Datos
El sistema utiliza múltiples fuentes de datos:
- Datos IoT en tiempo real (greenhouse_data.csv)
- Imágenes satelitales (via Earth Engine)
- Logs del sistema (greenhouse_log.txt)
- Base de datos SQL para usuarios y configuraciones

## 🔄 API REST
Endpoints principales:
- `/extract_variables`: Obtiene datos satelitales de una región
- Endpoints adicionales para gestión de datos IoT y usuarios

## 📱 Interfaces de Usuario
- **Dashboard** (dassh.html): Panel principal de control
- **Análisis** (análisis.html): Herramientas analíticas
- **Predicciones** (predicciones.html): Modelos predictivos
- **Historial** (historial.html): Datos históricos
- **Tecnología** (tecnologia.html): Documentación técnica

## 👥 Equipo y Contacto
- **Email**: sisrisistemasderiego@gmail.com
- **Teléfono**: +52 662 184 7257
- **Ubicación**: Hermosillo, Sonora, México

## 📄 Licencia
© 2024 Blue Basin Co. Todos los derechos reservados.

---

**Nota**: Este proyecto está en desarrollo activo. Para contribuir o reportar problemas, por favor crear un issue en el repositorio.
