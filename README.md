# Genesis Block Miner for Custom Cryptocurrency sha256

Este script en Python está diseñado para facilitar la minería del bloque génesis de una criptomoneda personalizada. Permite a los usuarios configurar los parámetros clave del bloque génesis y ejecutar la minería para encontrar un nonce válido que cumpla con la dificultad de la red especificada.

## Características

- **Minería de bloque génesis**: Calcula el nonce que satisface la condición de dificultad para un bloque génesis.
- **Configurable mediante argumentos de línea de comando**: Permite personalizar el timestamp, el tiempo UNIX, la clave pública y la recompensa del bloque génesis.
- **Salida detallada**: Muestra el nonce, el hash del bloque génesis y el hash de la raíz de Merkle.

## Cómo usar

El script se ejecuta desde la línea de comando y acepta varios argumentos para personalizar el bloque génesis. A continuación se describen los argumentos disponibles:

- `-z`, `--timestamp`: Define el timestamp del bloque génesis como una cadena de texto. Debe estar entre comillas si contiene espacios.
- `-t`, `--time`: Establece el tiempo UNIX (epoch time) del bloque génesis. Debe ser un número entero.
- `-p`, `--pubkey`: Define la clave pública en formato hexadecimal que se usará en la transacción coinbase del bloque génesis.
- `-r`, `--reward`: Establece la recompensa del bloque génesis. Debe ser un número entero que representa la cantidad de la criptomoneda.

### Ejemplo de uso

Para ejecutar el script con los valores por defecto, simplemente navega a la carpeta del script y usa el siguiente comando:

```bash
python genesis_block_miner.py
```
Para especificar un timestamp personalizado y otros parámetros, puedes usar el comando de la siguiente manera:

```bash
python genesis_block_miner.py -z "El inicio de mi criptomoneda" -t 1609459200 -p "0411abcde..." -r 1000000000
```
Esto configurará el bloque génesis con un timestamp personalizado, un tiempo UNIX específico, una clave pública determinada y una recompensa de 1000000000 unidades de la criptomoneda.

### Requisitos

Para ejecutar este script, necesitarás Python 3.x instalado en tu máquina. No se requieren bibliotecas externas adicionales fuera de las que vienen por defecto con Python.

### Contribuir

Si deseas contribuir al proyecto, puedes clonar el repositorio y enviar tus pull requests o abrir issues para discutir mejoras o reportar bugs. Todo tipo de contribuciones son bienvenidas!


