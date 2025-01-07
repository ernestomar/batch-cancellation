# batch-cancellation
Este proyecto permite realizar la anulación de facturas en lote usando el API de Facturacion electrónica.

## Instalacion
Para hacer correr este proyecto ejecutar en una maquina con python 3 instalado lo siguiente:

```bash
# Activamos entorno virtual
source ./venv/bin/activate

# Instalamos dependencias
pip install -r requirements.txt
```

## Uso del programa.

1. Este script esta en el archivo `main.py`.
2. Crea un archivo con los BILL_ID uno por línea que se deben eliminar, por ejemplo: `bill_ids.txt`
3. Ejecuta el programa desde la terminal:
   ```bash
   python main.py CLIENT_ID CLIENT_SECRET bill_ids.txt
   ```
   - Reemplaza `CLIENT_ID` y `CLIENT_SECRET` con tus credenciales de cliente.
   - Reemplaza `bill_ids.txt` con el nombre del archivo que contiene los `BILL_ID` (uno por línea).

### Resultados:
- **success.log**: Contendrá los requests y responses para las solicitudes exitosas (código 200).
- **error.log**: Contendrá los requests y responses para las solicitudes con errores (códigos distintos de 200).
