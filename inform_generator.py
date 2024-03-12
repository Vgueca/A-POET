import csv

import csv

class InformGenerator:
    def __init__(self, filename):
        self.filename = filename

    def generate_inform(self, experiments):
        # Obtener todos los campos distintos
        campos_distintos = set()
        for experiment in experiments:
            campos_distintos.update(experiment.keys())

        # Ordenar los campos
        campos_ordenados = sorted(campos_distintos)

        with open(self.filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Experimento'] + campos_ordenados)
            writer.writeheader()

            # Escribir los datos de cada experimento
            for i, experiment in enumerate(experiments, start=1):
                row_data = {'Experimento': i}
                row_data.update(experiment)
                writer.writerow(row_data)

                    
# # EJEMPLO DEL USO. El archivo pondrá como labels de cada columna las distintas "keys" del diccionario e irá rellenando las filas.
# experimentos = [
#     {"Temperatura": 25, "Presion": 1013.25, "Humedad": 60},
#     {"Temperatura": 30, "Presion": 1015.5, "Humedad": 55},
#     {"Temperatura": 22, "Presion": 1010.75, "Humedad": 65}
# ]

# # Crear una instancia de InformGenerator
# generador_informes = InformGenerator("informe.csv")

# # Generar informe
# generador_informes.generate_inform(experimentos)
