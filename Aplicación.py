import networkx as nx
import matplotlib.pyplot as plt

#Brayan Stiven Bonilla Castellanos
#Juan Carlos Monsalve Gómez

#Lugares reales representativos del municipio de Santa Rosa de Osos
#Con valores simulados para el ejercicio
base_real = [
    {
        'antecedentes': {'origen': 'marcotobon', 'destino': 'parque'},
        'consecuente': {'linea': 'roja', 'distancia': 150}
    },
    {
        'antecedentes': {'origen': 'parque', 'destino': 'capilla'},
        'consecuente': {'linea': 'verde', 'distancia': 100}
    },
    {
        'antecedentes': {'origen': 'capilla', 'destino': 'hospital'},
        'consecuente': {'linea': 'amarilla', 'distancia': 100}
    },
    {
        'antecedentes': {'origen': 'hospital', 'destino': 'basilica'},
        'consecuente': {'linea': 'azul', 'distancia': 200}
    },
    {
        'antecedentes': {'origen': 'marcotobon', 'destino': 'capilla'},
        'consecuente': {'linea': 'blanca', 'distancia': 300}
    },       
    {
        'antecedentes': {'origen': 'marcotobon', 'destino': 'hospital'},
        'consecuente': {'linea': 'negra', 'distancia': 450}
    },     
    {
        'antecedentes': {'origen': 'marcotobon', 'destino': 'basilica'},
        'consecuente': {'linea': 'violeta', 'distancia': 700}
    },    

]

#Representación del grafo del sistema de transporte
#Distancia en metros (simulada) desde cada uno de los lugares hacia el otro
grafo_transporte = {
    'marcotobon': {'info': 'Marco Tobon', 'distancias': {'parque': 150, 'capilla': 300, 'hospital': 450, 'basilica': 700}},
    'parque': {'info': 'Parque Principal', 'distancias': {'marcotobon': 150, 'capilla': 100}},    
    'capilla': {'info': 'Capilla de la Humildad', 'distancias': {'parque': 100, 'hospital': 100, 'marcotobon': 300}},  
    'hospital': {'info': 'Hospital', 'distancias': {'capilla': 100, 'basilica': 200, 'marcotobon': 450}}, 
    'basilica': {'info': 'basilica', 'distancias': {'hospital': 200, 'marcotobon': 700}}, 
}

#Extraccion de las distancias segun la estacion a validar
def expansion(origen_actual):
    adyacentes = []
    for nodo_adyacente in grafo_transporte[origen_actual]['distancias']:
        distancia = grafo_transporte[origen_actual]['distancias'][nodo_adyacente]
        adyacentes.append((nodo_adyacente, distancia))
    return adyacentes

#Busqueda de la mejor ruta para desplazarse
def buscar_ruta(origen, destino):
    matriz = [(origen, 0, [])]
    estaciones = set()

    while matriz:
        origen_actual, distancia_recorrida, ruta_optima = matriz.pop(0)
        
        if origen_actual == destino:
            return ruta_optima, distancia_recorrida
        
        estaciones.add(origen_actual)
        
        for siguiente_estacion, distancia in expansion(origen_actual):
            distancia_total = distancia_recorrida + distancia
            ruta_optimizada = ruta_optima + [siguiente_estacion]
            if siguiente_estacion not in estaciones:
                matriz.append((siguiente_estacion, distancia_total, ruta_optimizada))
        
        matriz.sort(key=lambda x: x[1])
    return None, None



# Función para dibujar el grafo del sistema de transporte
def dibujar_grafo():
    G = nx.Graph()

    # Agregar nodos al grafo
    for nodo in grafo_transporte:
        G.add_node(nodo, info=grafo_transporte[nodo]['info'])

    # Agregar arcos al grafo
    for nodo_actual in grafo_transporte:
        for nodo_adyacente, distancia in grafo_transporte[nodo_actual]['distancias'].items():
            G.add_edge(nodo_actual, nodo_adyacente, weight=distancia)

    # Obtener la posición de los nodos para dibujar el grafo
    pos = nx.spring_layout(G)

    # Dibujar los nodos con su información
    labels = nx.get_node_attributes(G, 'info')
    nx.draw_networkx_labels(G, pos, labels=labels)

    # Dibujar los arcos con las distancias
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw(G, pos, with_labels=False, node_size=2000, node_color='lightblue')

    # Mostrar la gráfica
    plt.show()
    
# Interfaz de usuario
def main():
    origen = input("Ingrese la estación de origen: ")
    destino = input("Ingrese la estación de destino: ")
    
    ruta_optima, distancia = buscar_ruta(origen, destino)
    
    if ruta_optima is not None:
        print("La mejor ruta es:", ruta_optima)
        print("La mejor ruta tiene una distancia de:", distancia)
    else:
        print("No se encontró una ruta desde", origen, "hasta", destino)
    
    dibujar_grafo()

# Ejecución del programa
if __name__ == '__main__':
    main()

