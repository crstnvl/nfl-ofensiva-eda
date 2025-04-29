# 📦 1. Importar Librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

sns.set(style="whitegrid")

# 📂 2. Seleccionar Manualmente el Dataset
Tk().withdraw()
file_path = askopenfilename(title="Selecciona tu archivo de datos",
                             filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Archivos CSV", "*.csv")])
if file_path:
    print(f"✅ Archivo seleccionado: {file_path}")
else:
    raise Exception("⚠️ No seleccionaste ningún archivo.")

# 📑 3. Cargar el Archivo
if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
    df = pd.read_excel(file_path)
elif file_path.endswith('.csv'):
    df = pd.read_csv(file_path)
else:
    raise ValueError("❌ Formato de archivo no compatible.")

print("\n👀 Primeras filas del dataset original:")
print(df.head())

# 📊 4. EDA Básico
print(f"\n📏 Filas: {df.shape[0]:,} | Columnas: {df.shape[1]}")
print("🧩 Tipos de datos:")
print(df.dtypes)
print("\n📋 Info:")
print(df.info())
print("\n📈 Estadísticas:")
print(df.describe().T)
print("\n🕳️ Nulos por columna:")
print(df.isnull().sum())

# 🧹 5. Limpieza de Datos
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')
df.drop_duplicates(inplace=True)
print("\n🧹 Nulos después de limpieza:")
print(df.isnull().sum())

# 📋 6. Filtrado
columnas_a_conservar = [
    'team', 'conference', 'year',
    'passing_attempts', 'passing_completions', 'passing_yards', 'passing_tds', 'interceptions_thrown',
    'rushing__attempts', 'rushing_yards', 'rushing_tds', 'rushing_fumbles',
    'receptions', 'receiving_yards', 'receiving_tds', 'receiver_fumbles',
    'two_point_conversions'
]
df = df[[col for col in columnas_a_conservar if col in df.columns]]
print("\n✅ Dataset filtrado:")
print(df.head())

# 📂 7. Crear Carpeta de Dashboards
output_folder = 'NFL_Dashboards'
os.makedirs(output_folder, exist_ok=True)

# 📊 8. Gráfica: Distribución Passing Yards
plt.figure(figsize=(12,6))
sns.histplot(df['passing_yards'], kde=True, bins=30)
plt.title('Distribución de Passing Yards')
plt.xlabel('Passing Yards')
plt.ylabel('Frecuencia')
plt.savefig(os.path.join(output_folder, 'distribucion_passing_yards.png'))
plt.show()

# 📊 9. Matriz de Correlación
df_numerico = df.select_dtypes(include='number')
plt.figure(figsize=(16,12))
sns.heatmap(df_numerico.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriz de Correlación')
plt.savefig(os.path.join(output_folder, 'matriz_correlacion.png'))
plt.show()

# 📊 10. Comparación Conferencias
plt.figure(figsize=(10,6))
sns.boxplot(x='conference', y='passing_yards', data=df)
plt.title('Passing Yards por Conferencia')
plt.savefig(os.path.join(output_folder, 'passing_yards_conferencia.png'))
plt.show()

plt.figure(figsize=(10,6))
sns.boxplot(x='conference', y='rushing_yards', data=df)
plt.title('Rushing Yards por Conferencia')
plt.savefig(os.path.join(output_folder, 'rushing_yards_conferencia.png'))
plt.show()

# 🏆 11. Top 10 Equipos
print("\n🏈 Top 10 Passing Yards:")
print(df.sort_values('passing_yards', ascending=False).head(10)[['team', 'year', 'passing_yards']])

print("\n🏈 Top 10 Rushing Yards:")
print(df.sort_values('rushing_yards', ascending=False).head(10)[['team', 'year', 'rushing_yards']])

print("\n✅ ¡Análisis terminado! Gráficas guardadas en 'NFL_Dashboards'. 🚀")
