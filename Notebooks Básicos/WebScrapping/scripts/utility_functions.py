
"""
Funciones de utilidad para cargar datos de mercado y calcular la fuerza relativa.
"""
import yfinance as yf
import matplotlib.pyplot as plt

# Función para traer datos financieros
def market_data(ticker, desde, hasta, intervalo):
    """
    Descarga los datos de mercado para un ticker en un rango de fechas y intervalo especificado.
    """
    datos = yf.download(ticker, start=desde, end=hasta, interval=intervalo) # 1D, 5m,  30 min etc
    return datos

# Función para calcular fuerza relativa
def fuerza_relativa(serie_activo, serie_benchmark): 
    """
    Calcula la fuerza relativa entre un activo y un benchmark.
    """
    resultado = serie_activo / serie_benchmark * 100
    return resultado


# Función para graficar
def graficar_chart(serie_datos, titulo, titulo_eje_x, titulo_eje_y):
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)  # Crea una figura y un eje con un tamaño específico y un diseño ajustado automáticamente
    ax.plot(serie_datos, color='#030764', lw=1.5)  # Grafica la serie de datos en el eje con un color y grosor de línea específicos
    fig.set_facecolor('lightsteelblue')  # Establece el color de fondo de la figura
    plt.title(titulo)  # Establece el título del gráfico
    plt.grid(True)  # Activa la cuadrícula en el gráfico para facilitar la lectura
    plt.xlabel(titulo_eje_x)  # Establece el título del eje X
    plt.ylabel(titulo_eje_y)  # Establece el título del eje Y
    plt.setp(ax.get_xticklabels(), rotation=45)  # Rota las etiquetas del eje X para mejorar la legibilidad
