

import requests
import math


MAPQUEST_API_KEY = "Pvh7ltUH2RDORpx2mFpFvDBgx7GDxzlH"

def obtener_ruta_mapquest(ciudad_origen, ciudad_destino, modo_transporte="auto"):
    """
    Obtiene la información de la ruta entre dos ciudades utilizando la API de MapQuest.
    Permite seleccionar el tipo de transporte.
    """
    
    modos_api = {
        "auto": "fastest",
        "bicicleta": "bicycle",
        "peatón": "pedestrian"
    }

    if modo_transporte not in modos_api:
        print(f"⚠️ Modo de transporte '{modo_transporte}' no soportado. Usando 'auto' por defecto.")
        modo_api = "fastest"
    else:
        modo_api = modos_api[modo_transporte]

    url = f"http://www.mapquestapi.com/directions/v2/route?key={MAPQUEST_API_KEY}&from={ciudad_origen}&to={ciudad_destino}&unit=k&routeType={modo_api}&locale=es_ES"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de MapQuest: {e}")
        return None


def main():
    print("--- Medidor de Distancia y Duración de Viaje ---")
    print("Escribe 's' en cualquier momento para salir.")

    while True:
        ciudad_origen = input("\nIntroduce la Ciudad de Origen: ").strip()
        if ciudad_origen.lower() == 's':
            break

        ciudad_destino = input("Introduce la Ciudad de Destino: ").strip()
        if ciudad_destino.lower() == 's':
            break

        print("\nSelecciona el modo de transporte:")
        print("1. Auto")
        print("2. Bicicleta")
        print("3. Peatón")
        print("4. Moto ")
        print("5. Autobús ")

        opcion = input("Opción (1-5): ").strip()
        modos = {
            "1": "auto",
            "2": "bicicleta",
            "3": "peatón",
            "4": "",
            "5": ""
        }

        modo_transporte = modos.get(opcion, "auto")

        if modo_transporte == "no_soportado":
            print("🚫 El modo 'autobús' no está soportado por la API de MapQuest.")
            continue

        if not ciudad_origen or not ciudad_destino:
            print("Ambas ciudades son obligatorias. Inténtalo de nuevo.")
            continue

        ruta_data = obtener_ruta_mapquest(ciudad_origen, ciudad_destino, modo_transporte)

        if ruta_data and ruta_data.get("info", {}).get("statuscode") == 0:
            ruta = ruta_data.get("route", {})
            distancia_km = ruta.get("distance", 0)
            duracion_segundos = ruta.get("realTime", 0)

            horas = math.floor(duracion_segundos / 3600)
            minutos = math.floor((duracion_segundos % 3600) / 60)
            segundos = duracion_segundos % 60

            
            combustible_litros = 0
            if modo_transporte == "auto":
                combustible_por_100km = 10.0
                combustible_litros = (distancia_km / 100) * combustible_por_100km

            print("\n--- Resultados del Viaje ---")
            print(f"Modo de Transporte: {modo_transporte.capitalize()}")
            print(f"Ciudad de Origen: {ciudad_origen.title()}")
            print(f"Ciudad de Destino: {ciudad_destino.title()}")
            print(f"Distancia: {distancia_km:.2f} km")
            print(f"Duración del Viaje: {int(horas)}h {int(minutos)}m {int(segundos)}s")
            if combustible_litros:
                print(f"Combustible Estimado: {combustible_litros:.2f} litros")

            print("\n--- Indicaciones del Viaje ---")
            legs = ruta.get("legs", [])
            if legs:
                for leg in legs:
                    for i, maneuver in enumerate(leg.get("maneuvers", [])):
                        narrative = maneuver.get("narrative", "")
                        if narrative:
                            print(f"{i+1}. {narrative}")
            else:
                print("No se encontraron instrucciones detalladas.")
        elif ruta_data:
            print(f"❌ Error de la API: {ruta_data.get('info', {}).get('messages', ['Error desconocido'])}")
        else:
            print("No se pudo procesar la solicitud.")

        continuar = input("\n¿Deseas realizar otra búsqueda? (s/n): ").strip().lower()
        if continuar != 's':
            break

    print("\n¡Gracias por usar el Medidor de Distancia!")

if __name__ == "__main__":
    main()
