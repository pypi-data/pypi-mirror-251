# Strawberry PI

## Setup modulo LoRa

Tutorial su come impostare i Pin GPIO per il modulo di comunicazione LoRa (Sx127x):

-  **Raspberry PI model B**:

   ![Raspberry PI model B - GPIO](./_imgs/Raspberry_PI_model_b_GPIOs.png)

   | Raspberry |      |      | Raspberry |
   | :-------- | :--- | ---: | --------- |
   |           | GND  |  GND |           |
   | Ground    | GND  |  NSS | GPIO8     |
   | 3.3v      | 3.3V | MOSI | GPIO10    |
   | GPIO22    | RST  | MISO | GPIO9     |
   | GPIO4     | DIO0 |  SCK | GPIO11    |
   | GPIO17    | DIO1 | DIO5 |           |
   | GPIO18    | DIO2 | DIO4 |           |
   | GPIO27    | DIO3 |  GND |           |

-  **Raspberry Pico W**

   ![Raspberry Pico W - GPIO](./_imgs/Raspberry_Pico_W_GPIOs.svg)

   | Raspberry |      |      | Raspberry |
   | :-------- | :--- | ---: | --------- |
   |           | GND  |  GND |           |
   | Ground    | GND  |  NSS | GPIO8     |
   | 3V3 (OUT) | 3.3V | MOSI | GPIO19    |
   | GPIO9     | RST  | MISO | GPIO16    |
   | GPIO7     | DIO0 |  SCK | GPIO18    |
   | GPIO10    | DIO1 | DIO5 |           |
   |           | DIO2 | DIO4 |           |
   |           | DIO3 |  GND |           |

-  **Raspberry Pico W**

   ![Raspberry Pico Zero W - GPIO](./_imgs/Raspberry_Pi_Zero_W_GPIOs.png)

   | Raspberry |      |      | Raspberry |
   | :-------- | :--- | ---: | --------- |
   |           | GND  |  GND |           |
   | Ground    | GND  |  NSS | GPIO8     |
   | 3V3 (OUT) | 3.3V | MOSI | GPIO10    |
   | GPI25     | RST  | MISO | GPIO9     |
   | GPI22     | DIO0 |  SCK | GPIO11    |
   |           | DIO1 | DIO5 |           |
   |           | DIO2 | DIO4 |           |
   |           | DIO3 |  GND |           |

## Utils

-  **Come installare librerie su Pico W**

   1. Installare il package [pipkin](https://pypi.org/project/pipkin/) sulla propria macchina, questo package ha gli stessi comandi di `pip`
   2. Utilizzare il package appena installato come se fosse `pip`, ecco un esempio:

   ```zsh
       pipkin install <Package>
   ```

-  **Come installare librerie**

   Quando si proverà a installare le librerie python sul model B, uscirà un errore del genere:

   ```zsh
       error: `externally-managed-environment`
   ```

   Per ovviare a questo problema lanciare il comando `pip` o `pip3` con il parametro **`--break-system-packages`**, esempio:

   ```zsh
       pip install Strawberry-PI --break-system-package
   ```

-  **Come convertire uno script python in Linux Service**

   Per creare un servizio linux, che sarà lanciare lo script python all'avvio del Raspberry e ogni volta che andrà in errore sarà rilanciato, utilizzare il comando:

   ```zsh
      forge <PYTHON_SCRIPT>
   ```

   esempio:

   ```zsh
      forge ./MyGateway.py
   ```

   Ecco alcuni comandi utili per capire l'andamento del servizio appena creato: - Per visualizzare lo stato del servizio appena creato
   `zsh
    sudo journalctl -u <PYTHON_SCRIPT>
` - Restituisce una lista di tutti i servizi presenti sul Raspberry
   `xml
    sudo systemctl --type=service
`

-  **Come installare il sistema operativo su model B**: https://www.raspberrypi.com/documentation/computers/getting-started.html
-  **Come accedere con RDP (Remote Desktop Protocol) su model B**: https://www.raspberryhome.it/2020/04/23/raspberry-pi-remote-desktop-rdp/

-  **Enable SPI Interface**
   1. Aprire un terminale e digitare il seguente comando, questo aprirà un'interfaccia grafica:
   ```zsh
       sudo raspi-config
   ```
   2. Selezionare l'opzione "Interfacing Options"
   3. Selezionare l'opzione "SPI" e attivare "\<Select\>"
   4. Selezionare e attivare "\<Yes\>"
   5. Selezionare a attivare "\<Ok\>"
