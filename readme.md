
# 🚆 Sistema de Optimización de Rutas de Transporte con IA

> Predice tiempos de viaje y encuentra las mejores rutas usando Redes Neuronales y Grafos Inteligentes.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📚 Tabla de Contenidos
- [📚 Tabla de Contenidos](#-tabla-de-contenidos)
- [📖 Descripción General](#-descripción-general)
- [🛠️ Requisitos Previos](#️-requisitos-previos)
- [📂 Estructura del Proyecto](#-estructura-del-proyecto)
- [⚙️ Pasos de Ejecución](#️-pasos-de-ejecución)
- [✨ Características Principales](#-características-principales)
- [📈 Salida](#-salida)
- [🧩 Personalización](#-personalización)

---

## 📖 Descripción General
Este proyecto implementa un sistema de optimización de rutas de transporte utilizando técnicas de Inteligencia Artificial **supervisada** a través de redes neuronales.  
Predice los tiempos de viaje entre estaciones y calcula rutas óptimas en función de dichas predicciones.

---

## 🛠️ Requisitos Previos

### 🔥 Versión de Python
- **Recomendada**: Python 3.8 - 3.11
- **Mínima**: Python 3.7+

### 📦 Librerías Necesarias
Instala los paquetes requeridos ejecutando:

```bash
pip install numpy networkx scikit-learn tensorflow
```

> Nota: `json` ya está incluido por defecto en Python.

---

## 📂 Estructura del Proyecto
| Archivo        | Descripción                                              |
|----------------|-----------------------------------------------------------|
| `main.py`      | Script principal que entrena el modelo y optimiza rutas.  |
| `datos.json`   | Datos de entrada: estaciones, conexiones y reglas.        |
| `Resultados.json` | Resultados generados: rutas optimizadas y reportes. |

---

## ⚙️ Pasos de Ejecución

1. **Preparar el Archivo `datos.json`**  
Ejemplo de estructura:

```json
{
  "estaciones": [
    {
      "id": "EST1",
      "lineas": ["L1", "L2"],
      "nombre": "Estación Central"
    }
  ],
  "conexiones": [
    {
      "origen": "EST1",
      "destino": "EST2",
      "tiempo": 10,
      "distancia": 5,
      "linea": "L1"
    }
  ],
  "reglas": [
    {
      "tipo": "mantenimiento_tramo",
      "origen": "EST1",
      "destino": "EST2"
    }
  ]
}
```

2. **Ejecutar el Script**

```bash
python main.py
```

---

## ✨ Características Principales
- 🧠 Predicción de tiempos de viaje con **redes neuronales**.
- 🛤️ Optimización de rutas en grafos ponderados dinámicamente.
- 🚧 Soporte para reglas de **mantenimiento** y **congestión**.
- 🔎 Análisis detallado de cada ruta y tiempos por tramo.
- 📝 Registro de rutas exitosas y rutas fallidas.

---

## 📈 Salida
Después de la ejecución, se generará el archivo `Resultados.json` que incluirá:
- ✅ Rutas óptimas entre todas las combinaciones posibles de estaciones.
- ⏱️ Tiempos predichos de viaje (por tramo y total).
- 🗺️ Información detallada de las estaciones.
- 🚫 Registro de rutas no posibles debido a restricciones.

---

## 🧩 Personalización
Puedes adaptar el comportamiento del sistema modificando `datos.json`:
- ➕ Añadir o eliminar estaciones.
- 🔗 Crear nuevas conexiones o modificar tiempos y distancias.
- ⚠️ Definir reglas de mantenimiento o congestión que alteren la red.

---

> Desarrollado con ❤️ y pasión por la IA.
