# ==============================================================
# 📦 1. Importar Librerías
# ==============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Librerías para seleccionar archivo manualmente
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Estilo de gráficos
sns.set(style="whitegrid")

# ==============================================================
# 📂 2. Seleccionar Manualmente el Dataset
# ==============================================================

# Inicializar la ventana Tkinter
Tk().withdraw()

# Abrir cuadro de diálogo para seleccionar archivo
file_path = askopenfilename(title="Selecciona tu archivo de datos",
                             filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Archivos CSV", "*.csv")])

# Validar si se seleccionó un archivo
if file_path:
    print(f"✅ Archivo seleccionado: {file_path}")
else:
    raise Exception("⚠️ No seleccionaste ningún archivo.")

# ==============================================================
# 📑 3. Cargar el Archivo
# ==============================================================

if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
    df = pd.read_excel(file_path)
elif file_path.endswith('.csv'):
    df = pd.read_csv(file_path)
else:
    raise ValueError("❌ Formato de archivo no compatible. Usa .xlsx, .xls o .csv.")

print("\n👀 Primeras filas del dataset original:")
print(df.head())

# ==============================================================
# 📊 4. Análisis Exploratorio Inicial (EDA Básico)
# ==============================================================

print(f"\n📏 El dataset tiene {df.shape[0]:,} filas y {df.shape[1]} columnas.\n")

print("🧩 Tipos de datos de cada columna:")
print(df.dtypes)

print("\n📋 Información general del dataset:")
print(df.info())

print("\n📈 Resumen estadístico de columnas numéricas:")
print(df.describe().T)

print("\n🕳️ Valores nulos por columna:")
print(df.isnull().sum())

# ==============================================================
# 🧹 5. Limpieza de Datos
# ==============================================================

# 5.1 Renombrar columnas (minúsculas, sin espacios)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')

# 5.2 Eliminar duplicados
df.drop_duplicates(inplace=True)

# 5.3 Revisar nuevamente valores nulos
print("\n🧹 Después de limpieza básica:")
print(df.isnull().sum())

# ==============================================================
# 📋 6. Filtrar columnas relevantes para ofensiva
# ==============================================================

columnas_a_conservar = [
    'team', 'conference', 'year',
    'passing_attempts', 'passing_completions', 'passing_yards', 'passing_tds', 'interceptions_thrown',
    'rushing__attempts', 'rushing_yards', 'rushing_tds', 'rushing_fumbles',
    'receptions', 'receiving_yards', 'receiving_tds', 'receiver_fumbles',  # corregido
    'two_point_conversions'
]

# Revisar si todas las columnas existen
columnas_existentes = [col for col in columnas_a_conservar if col in df.columns]

df = df[columnas_existentes]

print("\n✅ Dataset filtrado (ofensiva):")
print(df.head())

# ==============================================================
# 📂 7. Crear Carpeta para Dashboards
# ==============================================================

output_folder = 'NFL_Dashboards'
os.makedirs(output_folder, exist_ok=True)

# ==============================================================
# 📊 8. Gráficas - Distribución de Passing Yards
# ==============================================================

plt.figure(figsize=(12,6))
sns.histplot(df['passing_yards'], kde=True, bins=30)
plt.title('Distribución de Passing Yards')
plt.xlabel('Passing Yards')
plt.ylabel('Frecuencia')
plt.savefig(os.path.join(output_folder, 'distribucion_passing_yards.png'))
plt.show()

# ==============================================================
# 📊 9. Matriz de Correlación
# ==============================================================

df_numerico = df.select_dtypes(include='number')

plt.figure(figsize=(16,12))
sns.heatmap(df_numerico.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriz de Correlación de Variables Ofensivas')
plt.savefig(os.path.join(output_folder, 'matriz_correlacion.png'))
plt.show()

# ==============================================================
# 📊 10. Comparativa entre Conferencias
# ==============================================================

# Passing yards por conferencia
plt.figure(figsize=(10,6))
sns.boxplot(x='conference', y='passing_yards', data=df)
plt.title('Comparación de Passing Yards por Conferencia')
plt.xlabel('Conferencia')
plt.ylabel('Passing Yards')
plt.savefig(os.path.join(output_folder, 'passing_yards_conferencia.png'))
plt.show()

# Rushing yards por conferencia
plt.figure(figsize=(10,6))
sns.boxplot(x='conference', y='rushing_yards', data=df)
plt.title('Comparación de Rushing Yards por Conferencia')
plt.xlabel('Conferencia')
plt.ylabel('Rushing Yards')
plt.savefig(os.path.join(output_folder, 'rushing_yards_conferencia.png'))
plt.show()

# ==============================================================
# 🏆 11. Top 10 Equipos en Categorías Ofensivas
# ==============================================================

# Top Passing
top_passing = df.sort_values('passing_yards', ascending=False).head(10)
print("\n🏈 Top 10 equipos con más Passing Yards:")
print(top_passing[['team', 'year', 'passing_yards']])

# Top Rushing
top_rushing = df.sort_values('rushing_yards', ascending=False).head(10)
print("\n🏈 Top 10 equipos con más Rushing Yards:")
print(top_rushing[['team', 'year', 'rushing_yards']])

# ==============================================================
# 🏁 12. Finalización
# ==============================================================

print("\n✅ ¡Análisis terminado! Gráficas guardadas en la carpeta 'NFL_Dashboards'. 🚀")
