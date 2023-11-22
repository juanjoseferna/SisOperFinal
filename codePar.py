# Importar las bibliotecas necesarias
import ray
import time

# Iniciar Ray y conectar con un clúster existente en la dirección proporcionada
ray.init(address='10.80.12.42:6379')

# Obtener información sobre los nodos en el clúster
nodes = ray.nodes()

# Imprimir información sobre cada nodo en el clúster
for node in nodes:
    print(f"Node ID: {node['NodeID']}")
    print(f"Resources: {node['Resources']}")

# Definir una función remota para calcular el n-ésimo término de Fibonacci
@ray.remote
def fibo(n):
    if n <= 1:
        return n

    fib_prev, fib_actual = 0, 1

    for _ in range(2, n + 1):
        fib_prev, fib_actual = fib_actual, fib_prev + fib_actual

    return fib_actual

# Definir una función remota para verificar si un número es primo
@ray.remote
def primo(numero):
    if numero <= 1:
        return False
    elif numero == 2:
        return True
    elif numero % 2 == 0:
        return False
    else:
        # Verificar divisibilidad hasta la raíz cuadrada de numero
        limite_superior = int(numero**0.5) + 1
        for i in range(3, limite_superior, 2):
            if numero % i == 0:
                return False
        return True

# Imprimir una línea divisoria
print('-----------------------------------------------------------------------------------------------------------------------------------------')

# Obtener la cantidad de números primos que se desean imprimir
entrada = int(input("Cuantos numeros primos quieres imprimir: "))

# Calcular los primeros 'entrada' términos de la sucesión de Fibonacci de manera distribuida
results = ray.get([fibo.remote(i) for i in range(entrada)])

# Imprimir los 'entrada' términos de la sucesión de Fibonacci
print('los ', entrada, 'numeros fibonacci son: ', results)

# Filtrar los números Fibonacci que son primos
A = []
for i in results:
    if ray.get(primo.remote(i)):
        A.append(i)

# Imprimir los números Fibonacci que son primos
print('los fibonacci primos son: ', A)
