import networkx as nx # crear los grafos
import matplotlib.pyplot as plt # visualizar los grafos
import random as num_random # generar números random
import tkinter as tki
from tkinter import messagebox
import tkinter.simpledialog

#menu
def menu():
    root = tki.Tk()
    root.title("Menu")

    def ingresar_n_y_matriz():
        n = tki.simpledialog.askinteger("Valor de n", "Ingresar el valor de n (8 <= n <= 16):")
        if n is None or n < 8 or n > 16:
            messagebox.showerror("Error", "Ingrese un numero entre 8 y 16.")
            return
        
        # Crear la matriz manualmente
        capacidad_m = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    capacidad_m[i][j] = tki.simpledialog.askinteger("Matriz", f"Ingrese el valor para la posicion [{i},{j}]:")
                    if capacidad_m[i][j] is None:
                        messagebox.showerror("Error", "Ingresar un valor entero valido.")
                        return
        
        mostrar(capacidad_m)
        grafo_networkx(capacidad_m)
        
        ford_fulkerson(capacidad_m)

    def generar_matriz_aleatoria():
        n = tki.simpledialog.askinteger("Valor de n", "Ingrese el valor de n (8 <= n <= 16):")
        if n is None or n < 8 or n > 16:
            messagebox.showerror("Error", "Ingrese un numero entre 8 y 16.")
            return

        # Generar matriz aleatoria
        capacidad_m = [[0 if i >= j else num_random.randint(1, 20) for j in range(n)] for i in range(n)]
        
        mostrar(capacidad_m)
        grafo_networkx(capacidad_m)

        ford_fulkerson(capacidad_m)

    def ford_fulkerson(capacidad_m):
        n = len(capacidad_m)  # Obtener el tamaño de la matriz
        # Mensaje dinámico para ingresar la fuente y el sumidero
        vertice_fuente = tki.simpledialog.askinteger("Fuente", f"Ingrese el valor de la fuente (0 y {n-1}):")
        vertice_sumidero = tki.simpledialog.askinteger("Sumidero", f"Ingrese el valor del sumidero (0 y {n-1}):")
    
        # Validar que fuente y sumidero sean valores válidos
        if vertice_fuente is None or vertice_sumidero is None or vertice_fuente < 0 or vertice_fuente >= n or vertice_sumidero < 0 or vertice_sumidero >= n:
            messagebox.showerror("Error", f"Ingrese valores entre 0 y {n-1} para la fuente y el sumidero.")
            return

        flujo_max, grafo_resul = Ford_fulkerson(capacidad_m, vertice_fuente, vertice_sumidero)
    
        messagebox.showinfo("Flujo Máximo", f"El flujo máximo entre los vértices {vertice_fuente} y {vertice_sumidero} es: {flujo_max}")
    
        grafo_networkx(grafo_resul, titulo="Grafo con Ford Fulkerson aplicado")


    def mostrar_creditos():
        messagebox.showinfo("Integrantes", "Contreras Quijua, Jhohandri Jhunior-U2021D925\nDiaz Quispe, Matias Sebastian-U202311938\nChipana Huarancca, Emanuel-U202214074\nElescano Leon, Piero Hugo-U202313354\nNieto Sivincha, Lina Mariseli-U202323427")

    def salir():
        root.quit()
    tki.Label(root, text="Tema 3: Flujo maximo", font=("Arial", 16)).pack(pady=10)
    
    tki.Button(root, text="Generar la matriz de forma manual", command=ingresar_n_y_matriz, width=40).pack(pady=5)
    tki.Button(root, text="Generar la matriz de forma aleatoria", command=generar_matriz_aleatoria, width=40).pack(pady=5)
    tki.Button(root, text="Integrantes", command=mostrar_creditos, width=40).pack(pady=5)
    tki.Button(root, text="Salir", command=salir, width=40).pack(pady=5)

    root.mainloop()

#verifivar el grafo
def grafo_camino(grafo_dirigido, vertice, linea, arista):
    visitado = [False] * len(grafo_dirigido)  #marcam los nodos visitados
    queue = []

    queue.append(vertice)  #comenza desde el inicio
    visitado[vertice] = True
    arista[vertice] = -1

    while queue:
        u = queue.pop(0)  #siguiente nodo

        for v, capacidad in enumerate(grafo_dirigido[u]):
            #si v no fue visitado 
            if not visitado[v] and capacidad > 0:
                arista[v] = u
                if v == linea:
                    return True
                queue.append(v)  #agregamos v y seguimos el grafo
                visitado[v] = True  #marcamos como visitado
    return False

#algoritmo ford fulkerson
def Ford_fulkerson(grafo, vertice, linea):
    #grafo resultante
    grafo_resul = [row[:] for row in grafo]
    arista = [-1] * len(grafo)
    flujo_max = 0 

    while grafo_camino(grafo_resul, vertice, linea, arista):
        flujo_min = float('inf')
        v = linea
        while v != vertice:
            u = arista[v]
            flujo_min = min(flujo_min, grafo_resul[u][v])
            v = arista[v]
        v = linea
        while v != vertice:
            u = arista[v]
            grafo_resul[u][v] -= flujo_min  #disminuimos la capacidad del camino
            grafo_resul[v][u] += flujo_min  #aumentamos
            v = arista[v]
        
        flujo_max += flujo_min  #sumamos los dos flujos 
    return flujo_max, grafo_resul

#mostrar matriz
def mostrar(matrix):
    print("Matriz:")
    for fila in matrix:
        print(fila)

#dibujar grafo
def grafo_networkx(matrix, titulo="Grafo"):
    G = nx.DiGraph()  # Creamos el grafo
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] > 0:
                G.add_edge(i, j, capacidad=matrix[i][j])

    #posicion de los nodos en el grafo
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): d['capacidad'] for u, v, d in G.edges(data=True)}
    
    #dibujamos el grafo
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(titulo)
    plt.show()

def main():
    menu()

if __name__ == "__main__":
    main()
