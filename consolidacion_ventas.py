import pandas as pd
import glob
import mysql.connector
import os

# Configuración de la conexión a la base de datos MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="241196",
    database="integracionex"
)

# Directorio donde se encuentran los archivos Excel
directory = r"C:\Users\carol\Downloads\ArchivosTiendas"

# Obtener la lista de archivos Excel en el directorio
files = glob.glob(directory + "/Local_*.xlsx")

for file in files:
    # Leer el archivo Excel
    df = pd.read_excel(file)

    # Obtener el idLocal del nombre del archivo
    idLocal = int(os.path.basename(file).split('Local_')[1].split('.')[0])
    print(f"idLocal: {idLocal}")  # Debugging

    # Agregar el idLocal al DataFrame
    df['idLocal'] = idLocal

    # Verificar si la columna 'Fecha' está presente y convertirla a datetime
    if 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'])

        # Insertar los registros en la base de datos
        cursor = mydb.cursor()

        # Insertar registros en la base de datos
        for index, row in df.iterrows():
            sql = """INSERT INTO ventas (idTransaccion, idLocal, Fecha, IdCategoria, Producto, Cantidad, PrecioUnitario, TotalVenta) 
                    VALUES (%s, %s, %s, (SELECT IdCategoria FROM categorias WHERE Nombre = %s), %s, %s, %s, %s)"""
            values = (row['idTransaccion'], row['idLocal'], row['Fecha'], row['Producto'], row['Producto'], row['Cantidad'], row['PrecioUnitario'], row['TotalVenta'])
            try:
                cursor.execute(sql, values)
            except mysql.connector.Error as err:
                print(f"Error al insertar registro: {err}")
                continue

        mydb.commit()
        cursor.close()
    else:
        print("No se encontró la columna 'Fecha' en el archivo:", file)

print("Datos consolidados en la base de datos MySQL.")
