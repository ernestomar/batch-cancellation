import argparse
import requests
import json

def get_token(auth_url, client_id, client_secret):
    """Obtiene el token de acceso usando el flujo Client Credentials."""
    print(f"Obteniendo token de {auth_url}")
    try:
        response = requests.post(auth_url, data={
            'response_type': 'code',
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        })
        response.raise_for_status()
        access_token = response.json().get('access_token')
        if access_token:
            print(f"Access Token: {access_token}")
            return access_token
        else:
            print("Error: No se encontró el token en la respuesta.")
            exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el token: {e}")
        exit(1)

def annul_bill(api_url, token, bill_id):
    """Anula un bill enviando el bill_id y el motivo."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print(headers)
    payload = {
        "bill_id": bill_id,
        "reason_code": "1"
    }
    try:
        response = requests.put(api_url, headers=headers, json=payload)
        return {
            "status_code": response.status_code,
            "request": json.dumps(payload),
            "response": response.text
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": 500,
            "request": json.dumps(payload),
            "response": f"Error: {e}"
        }

def main():
    parser = argparse.ArgumentParser(description="Anulación de facturas con OAUTH.")
    parser.add_argument("client_id", help="Client ID para obtener el token.")
    parser.add_argument("client_secret", help="Client Secret para obtener el token.")
    parser.add_argument("bill_file", help="Archivo de texto con BILL_IDs (uno por línea).")
    args = parser.parse_args()

    auth_url = "https://ebill-auth.cirrus-it.net/oauth2/token"
    api_url = "https://ebill-management-api.cirrus-it.net/api/v1/bill/annulment"

    # Obtener token
    token = get_token(auth_url, args.client_id, args.client_secret)
    print("Token obtenido con éxito.")

    # Leer BILL_IDs del archivo
    try:
        with open(args.bill_file, 'r') as file:
            bill_ids = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"El archivo {args.bill_file} no existe.")
        exit(1)

    # Abrir archivos de logs
    success_log = open("success.log", "w")
    error_log = open("error.log", "w")

    # Procesar cada BILL_ID
    for bill_id in bill_ids:
        result = annul_bill(api_url, token, bill_id)
        log_entry = f"Request: {result['request']}\nResponse: {result['response']}\n\n"

        if result["status_code"] == 200:
            success_log.write(log_entry)
        else:
            error_log.write(log_entry)

    # Cerrar archivos de logs
    success_log.close()
    error_log.close()
    print("Proceso completado. Revisar los archivos success.log y error.log.")

if __name__ == "__main__":
    main()