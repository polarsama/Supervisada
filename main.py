import json
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple
import itertools
import math
import time
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

class SistemaDeTransporteIA:
    def __init__(self, datos_archivo: str):
        with open(datos_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        self.estaciones = {est['id']: est for est in datos['estaciones']}
        self.conexiones = datos.get('conexiones', [])
        self.reglas = datos.get('reglas', [])

        self.grafo = self._construir_grafo_networkx()
        self.modelo_prediccion, self.scaler = self._crear_modelo_prediccion()

    def _construir_grafo_networkx(self) -> nx.DiGraph:
        G = nx.DiGraph()

        for conexion in self.conexiones:
            if not self._validar_conexion(conexion):
                continue

            origen = conexion['origen']
            destino = conexion['destino']

            peso = self._calcular_peso_conexion(conexion)

            G.add_edge(origen, destino,
                       tiempo=conexion.get('tiempo', 10),
                       distancia=conexion.get('distancia', 1),
                       linea=conexion.get('linea', 'desconocida'),
                       peso=peso)

        return G

    def _validar_conexion(self, conexion: Dict) -> bool:
        for regla in self.reglas:
            if regla['tipo'] == 'mantenimiento_tramo':
                if (regla['origen'] == conexion['origen'] and regla['destino'] == conexion['destino']):
                    return False
        return True

    def _calcular_peso_conexion(self, conexion: Dict) -> float:
        tiempo = conexion.get('tiempo', 10)
        distancia = conexion.get('distancia', 1)

        for regla in self.reglas:
            if regla['tipo'] == 'congestion':
                if regla['linea'] == conexion.get('linea'):
                    tiempo *= regla.get('factor', 1)

        return tiempo / distancia

    def _crear_modelo_prediccion(self) -> Tuple[Sequential, MinMaxScaler]:
        X_train, y_train = self._preparar_datos_entrenamiento()

        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)

        modelo = Sequential([
            Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
            Dense(32, activation='relu'),
            Dense(1, activation='linear')
        ])

        modelo.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
        modelo.fit(X_train_scaled, y_train, epochs=50, verbose=0)

        return modelo, scaler

    def _preparar_datos_entrenamiento(self) -> Tuple[np.ndarray, np.ndarray]:
        caracteristicas = []
        tiempos = []

        for conexion in self.conexiones:
            caracteristica = [
                conexion.get('distancia', 1),
                conexion.get('tiempo', 10),
                len(self.estaciones[conexion['origen']]['lineas'])
            ]
            caracteristicas.append(caracteristica)
            tiempos.append(conexion.get('tiempo', 10))

        return np.array(caracteristicas), np.array(tiempos)

    def encontrar_ruta_ia(self, origen: str, destino: str) -> Dict:
        G_predicho = self.grafo.copy()

        for u, v, datos in G_predicho.edges(data=True):
            caracteristicas = np.array([
                datos['distancia'],
                datos['tiempo'],
                len(self.estaciones[u]['lineas'])
            ]).reshape(1, -1)

            caracteristicas_scaled = self.scaler.transform(caracteristicas)
            tiempo_predicho = self.modelo_prediccion.predict(caracteristicas_scaled, verbose=0)[0][0]

            G_predicho[u][v]['peso_predicho'] = max(5, tiempo_predicho)

        ruta = nx.dijkstra_path(G_predicho, origen, destino, weight='peso_predicho')

        tiempos_predichos = []
        for i in range(len(ruta) - 1):
            u = ruta[i]
            v = ruta[i+1]
            tiempos_predichos.append(G_predicho[u][v]['peso_predicho'])

        tiempo_total = sum(tiempos_predichos)
        horas_total = int(tiempo_total // 60)
        minutos_total = int(tiempo_total % 60)

        tiempos_tramos_formato = []
        for tiempo in tiempos_predichos:
            horas = int(tiempo // 60)
            minutos = int(tiempo % 60)
            tiempos_tramos_formato.append({"horas": horas, "minutos": minutos})

        return {
            "origen": origen,
            "destino": destino,
            "ruta": ruta,
            "tiempo_total": {"horas": horas_total, "minutos": minutos_total},
            "tiempos_tramos": tiempos_tramos_formato,
            "detalles_estaciones": [self.estaciones[est] for est in ruta]
        }

def convertir_numpy_a_json(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.float32):
        return float(obj)
    elif isinstance(obj, np.int64):
        return int(obj)
    elif isinstance(obj, dict):
        return {k: convertir_numpy_a_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_numpy_a_json(v) for v in obj]
    return obj

def main():
    inicio = time.time()

    print("\U0001F689 Iniciando Sistema de Transporte con IA Supervisado...")
    print("Cargando datos y configurando modelo...")

    sistema = SistemaDeTransporteIA('datos.json')

    ids_estaciones = list(sistema.estaciones.keys())
    rutas_ejemplo = list(itertools.permutations(ids_estaciones, 2))

    print(f"Total de rutas a calcular: {len(rutas_ejemplo)}")

    resultados = []
    for i, (origen, destino) in enumerate(rutas_ejemplo, 1):
        if origen != destino:
            print(f"Calculando ruta {i}/{len(rutas_ejemplo)}: {origen} → {destino}")

            ruta = sistema.encontrar_ruta_ia(origen, destino)
            resultados.append(ruta)

    resultados_json = convertir_numpy_a_json(resultados)

    with open('Resultados.json', 'w', encoding='utf-8') as f:
        json.dump(resultados_json, f, ensure_ascii=False, indent=2)

    fin = time.time()
    tiempo_ejecucion = fin - inicio

    print(f"\n✅ Proceso completado.")
    print(f"🕒 Tiempo total de ejecución: {tiempo_ejecucion:.2f} segundos")
    print(f"📄 Resultados guardados en 'Resultados.json'")

if __name__ == "__main__":
    main()
