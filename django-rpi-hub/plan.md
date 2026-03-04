# Django RPi Hub — Plano de Implementação

**Data:** 2026-02-20
**Status:** DRAFT
**Target System:** Raspberry Pi 5 (Standalone — Django + Hardware)
**Python:** 3.12+
**Nível:** Junior Developer

---

## 1. Resumo do Projecto

Plataforma Django que corre num Raspberry Pi 5 e expõe uma API Socket.IO para clientes web interagirem com hardware físico (sensores, LEDs, câmara, RFID, etc.).

**Princípio central:** O cliente Socket.IO é quem decide que hardware quer usar — ao fazer `subscribe`, o driver inicializa on-demand (lazy). Quando ninguém está à escuta, o driver desliga-se.

### Características

- **Bidirecional**: leitura de sensores (inputs) e controlo de actuadores (outputs)
- **Configurável em runtime**: sem ficheiros de config no RPi — o cliente envia a configuração
- **Histórico em SQLite**: eventos gravados com TTL curto para não encher o disco
- **Rede isolada**: sem autenticação (hotspot local)
- **Escala**: 1 RPi, < 5 clientes simultâneos

---

## 2. Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                     Raspberry Pi 5                              │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Django ASGI Application (Uvicorn)                       │   │
│  │                                                          │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │   │
│  │  │ Socket.IO    │  │ Driver       │  │ Django ORM   │   │   │
│  │  │ (consumers)  │←→│ Registry     │  │ (EventLog)   │   │   │
│  │  │              │  │              │  │ SQLite + WAL  │   │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────────────┘   │   │
│  │         │                 │                              │   │
│  │         │    ┌────────────┼────────────┐                 │   │
│  │         │    │            │            │                 │   │
│  │         │  ┌─┴──────┐ ┌──┴─────┐ ┌───┴────┐            │   │
│  │         │  │ RFID   │ │ LED    │ │ MPR121 │  ...        │   │
│  │         │  │ Driver │ │ Driver │ │ Driver │             │   │
│  │         │  └─┬──────┘ └──┬─────┘ └───┬────┘            │   │
│  └─────────┼────┼───────────┼───────────┼──────────────────┘   │
│            │    │           │           │                       │
│       ┌────┘    │           │           │                       │
│       │    ┌────┘      ┌────┘      ┌────┘                      │
│   ┌───┴──┐│ ┌──────┐  │┌──────┐   │┌──────────┐               │
│   │WiFi  ││ │SPI   │  ││GPIO  │   ││I2C Bus   │               │
│   │Client││ │RC522 │  ││Pins  │   ││MPR121 x2 │               │
│   └──────┘│ └──────┘  │└──────┘   │└──────────┘               │
│           └───────────┘───────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Stack Tecnológica

| Componente      | Tecnologia                      | Versão   | Razão                                               |
| --------------- | ------------------------------- | -------- | --------------------------------------------------- |
| **Framework**   | Django                          | 5.1+     | ORM, admin, migrations, middleware                  |
| **ASGI Server** | Uvicorn                         | 0.30+    | Suporte async nativo, leve                          |
| **Socket.IO**   | python-socketio                 | 5.11+    | Protocolo standard, clientes em todas as linguagens |
| **Validação**   | Pydantic                        | 2.x      | Schemas de payloads Socket.IO (input/output)        |
| **DB**          | SQLite                          | built-in | Leve, zero config, ideal para RPi standalone        |
| **Hardware**    | RPi.GPIO / gpiozero             | latest   | GPIO control (LEDs, buttons)                        |
| **I2C**         | adafruit-blinka + circuitpython | latest   | MPR121 e outros sensores I2C                        |
| **SPI/RFID**    | mfrc522 ou spidev               | latest   | Leitor RFID RC522                                   |
| **Camera**      | picamera2                       | latest   | RPi Camera Module v2/v3                             |
| **CV / ArUco**  | opencv-contrib-python-headless  | 4.9+     | Detecção de marcadores ArUco + processamento imagem |
| **YOLO**        | ultralytics (YOLOv8n)           | 8.x      | Detecção de pessoas — modelo nano para RPi          |

---

## 4. Estrutura do Projecto

```
django-rpi-hub/
├── plan.md                          ← este ficheiro
├── requirements.txt
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py                      ← monta Django + Socket.IO no mesmo ASGI app
├── hardware/                        ← app Django principal
│   ├── __init__.py
│   ├── models.py                    ← EventLog (histórico com TTL)
│   ├── admin.py                     ← Admin para EventLog (debugging)
│   ├── consumers.py                 ← Socket.IO event handlers
│   ├── registry.py                  ← DriverRegistry (singleton, gestão lazy)
│   ├── schemas.py                   ← Pydantic schemas para validação
│   ├── cleanup.py                   ← tarefa periódica de limpeza de logs
│   ├── drivers/
│   │   ├── __init__.py
│   │   ├── base.py                  ← BaseDriver (ABC)
│   │   ├── rfid.py                  ← RFID RC522 (SPI) — Fase 1
│   │   ├── led.py                   ← LED GPIO — Fase 1
│   │   ├── button.py                ← Button GPIO — Fase 2  (*)
│   │   ├── mpr121.py                ← Capacitivo I2C — Fase 2  (*)
│   │   ├── camera.py                ← RPi Camera — Fase 3  (*)
│   │   ├── aruco.py                 ← ArUco marker detection — Fase 3  (*)
│   │   ├── ir_sensor.py             ← Infrared — Fase 3  (*)
│   │   └── person_detector.py       ← YOLO person detection — Fase 4  (*)
│   └── migrations/
├── static/
│   └── test.html                    ← Página HTML simples de teste
└── templates/                       ← (vazio, reservado para futuro)
```

_(\*) — ficheiros criados nas fases posteriores_

---

## 5. Fases de Implementação

---

### FASE 0 — Setup do Projecto (Dia 1-2)

**Objectivo:** Ter o projecto Django a arrancar com Uvicorn e Socket.IO a responder.

#### Tarefas

- [ ] **0.1** Criar virtualenv e instalar dependências base

  ```bash
  python -m venv venv && source venv/bin/activate
  pip install django uvicorn python-socketio pydantic
  pip freeze > requirements.txt
  ```

- [ ] **0.2** Criar projecto Django

  ```bash
  django-admin startproject config .
  python manage.py startapp hardware
  ```

- [ ] **0.3** Configurar `settings.py`
  - Adicionar `"hardware"` a `INSTALLED_APPS`
  - Configurar `DATABASES` para SQLite com WAL mode:

    ```python
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
            "OPTIONS": {
                "init_command": "PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;",
            },
        }
    }
    ```

  - Configurar `STATIC_URL` e `STATICFILES_DIRS`
  - `ALLOWED_HOSTS = ["*"]` (rede isolada)

- [ ] **0.4** Configurar `asgi.py` — montar Django + Socket.IO

  ```python
  import django
  django.setup()

  import socketio
  from django.core.asgi import get_asgi_application

  sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
  django_asgi = get_asgi_application()
  application = socketio.ASGIApp(sio, django_asgi)
  ```

- [ ] **0.5** Criar handler Socket.IO mínimo em `consumers.py`
  - `connect` → log "Client connected"
  - `disconnect` → log "Client disconnected"
  - `ping` → responde `pong` (para validar que funciona)

- [ ] **0.6** Criar `static/test.html` com Socket.IO client
  - Botão "Connect", mostra estado da ligação
  - Botão "Ping" que envia evento e mostra resposta

- [ ] **0.7** Testar

  ```bash
  uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload
  ```

  - Abrir `http://localhost:8000/static/test.html`
  - Verificar que connect/ping/pong funciona

#### Critérios de Aceitação (Fase 0)

- [ ] `uvicorn` arranca sem erros
- [ ] Socket.IO conecta e responde a `ping`
- [ ] Página HTML de teste mostra "Connected"

---

### FASE 1 — Core: BaseDriver + Registry + RFID + LED (Dia 3-7)

**Objectivo:** Arquitectura de drivers funcional com 1 input (RFID) e 1 output (LED).

#### 1A — BaseDriver (ABC)

- [ ] **1A.1** Criar `drivers/base.py` com a classe abstracta:

  ```python
  from abc import ABC, abstractmethod
  from typing import Any

  class BaseDriver(ABC):
      """Interface que todos os drivers de hardware devem implementar."""

      # Identificador único do tipo de driver
      DRIVER_TYPE: str = ""

      # "input", "output", ou "both"
      DIRECTION: str = "input"

      def __init__(self, config: dict[str, Any]):
          self.config = config
          self._running = False

      @abstractmethod
      async def init(self) -> None:
          """Inicializa o hardware (chamado uma vez, lazy)."""
          ...

      @abstractmethod
      async def start(self) -> None:
          """Começa a ler/escutar (para inputs)."""
          ...

      @abstractmethod
      async def stop(self) -> None:
          """Para a leitura e liberta recursos."""
          ...

      @abstractmethod
      async def cleanup(self) -> None:
          """Shutdown final — liberta GPIO/I2C/SPI."""
          ...

      async def read(self) -> dict[str, Any]:
          """Lê o último estado (inputs)."""
          raise NotImplementedError

      async def write(self, command: dict[str, Any]) -> dict[str, Any]:
          """Envia comando ao hardware (outputs)."""
          raise NotImplementedError
  ```

- [ ] **1A.2** O que o junior deve entender:
  - **ABC** = classe que não pode ser instanciada directamente; obriga subclasses a implementar os métodos
  - **`async`** = todas as operações são assíncronas; nunca bloquear o event loop
  - **`config: dict`** = vem do cliente Socket.IO no momento do subscribe

#### 1B — DriverRegistry

- [ ] **1B.1** Criar `registry.py`:

  ```python
  class DriverRegistry:
      """Singleton que gere o ciclo de vida de todos os drivers activos."""
  ```

  O registry deve:
  - Manter um dicionário `{driver_key: DriverInstance}`
  - `driver_key` = combinação de `type + config hash` (para permitir 2 LEDs em pins diferentes)
  - Ter um `asyncio.Lock` por operação de init/stop
  - Contar subscribers por driver (`ref_count`)
  - Quando `ref_count` chega a 0 → agendar `stop()` com grace period (ex: 5s)
  - Registar os tipos de driver disponíveis num dicionário de classes:

    ```python
    DRIVER_CLASSES = {
        "rfid": RFIDDriver,
        "led": LEDDriver,
    }
    ```

- [ ] **1B.2** Métodos principais:
  - `subscribe(sid, driver_type, config) → DriverInstance`
  - `unsubscribe(sid, driver_type)`
  - `unsubscribe_all(sid)` — chamado no `disconnect`
  - `send_command(driver_type, command) → response`
  - `get_status() → dict` — estado de todos os drivers activos

#### 1C — Schemas Pydantic

- [ ] **1C.1** Criar `schemas.py` com validação de payloads:

  ```python
  from pydantic import BaseModel, Field
  from typing import Any

  class SubscribePayload(BaseModel):
      type: str                             # "rfid", "led", etc.
      config: dict[str, Any] = Field(default_factory=dict)

  class UnsubscribePayload(BaseModel):
      type: str

  class CommandPayload(BaseModel):
      type: str                             # tipo do driver
      action: str                           # "on", "off", "blink", "snapshot", etc.
      params: dict[str, Any] = Field(default_factory=dict)

  class EventPayload(BaseModel):
      type: str
      event: str
      data: dict[str, Any]
      timestamp: str
  ```

#### 1D — Consumers Socket.IO

- [ ] **1D.1** Expandir `consumers.py` com os handlers reais:
  - **`subscribe`**: valida payload → `registry.subscribe(sid, ...)` → junta sid ao room → responde
  - **`unsubscribe`**: `registry.unsubscribe(sid, ...)` → remove do room
  - **`command`**: valida → `registry.send_command(...)` → responde com resultado
  - **`disconnect`**: `registry.unsubscribe_all(sid)` — **crítico, não esquecer**

- [ ] **1D.2** Ao emitir eventos de hardware, usar **rooms** Socket.IO:
  - Room name = `driver_{type}` (ex: `driver_rfid`)
  - Assim só os clientes subscritos recebem eventos daquele sensor

#### 1E — LED Driver (Output)

- [ ] **1E.1** Criar `drivers/led.py`:
  - `DRIVER_TYPE = "led"`
  - `DIRECTION = "output"`
  - `init()`: configura GPIO pin como output via `gpiozero.LED` ou `RPi.GPIO`
  - `write(command)`: suporta acções:
    - `{"action": "on"}` → liga LED
    - `{"action": "off"}` → desliga LED
    - `{"action": "toggle"}` → inverte estado
    - `{"action": "blink", "params": {"interval": 0.5}}` → pisca
  - `cleanup()`: desliga LED e limpa GPIO

- [ ] **1E.2** Config esperada do cliente:

  ```json
  { "type": "led", "config": { "pin": 17 } }
  ```

- [ ] **1E.3** **SEGURANÇA GPIO**: Validar que o pin está numa lista de pins permitidos (não deixar o cliente usar qualquer GPIO):

  ```python
  ALLOWED_GPIO_PINS = [17, 18, 22, 23, 24, 25, 27]
  ```

#### 1F — RFID Driver (Input)

- [ ] **1F.1** Criar `drivers/rfid.py`:
  - `DRIVER_TYPE = "rfid"`
  - `DIRECTION = "input"`
  - `init()`: inicializa leitor RC522 via SPI
  - `start()`: arranca um `asyncio.Task` que faz polling:

    ```python
    async def _poll_loop(self):
        while self._running:
            uid = await asyncio.to_thread(self._read_card)  # blocking → thread
            if uid:
                await self._emit_event({"uid": uid})
            await asyncio.sleep(0.1)
    ```

  - `_read_card()`: função síncrona (SPI é blocking) — wrapped em `asyncio.to_thread`
  - `cleanup()`: para o loop, limpa SPI

- [ ] **1F.2** Config esperada do cliente:

  ```json
  { "type": "rfid", "config": { "pin_rst": 25 } }
  ```

- [ ] **1F.3** Evento emitido:

  ```json
  { "type": "rfid", "event": "card_read", "data": { "uid": "AB:CD:EF:12" } }
  ```

- [ ] **1F.4** **Deduplicação**: Não emitir o mesmo UID seguido (debounce de 2s para o mesmo cartão).

#### 1G — Callback de Eventos: Driver → Socket.IO

- [ ] **1G.1** O driver precisa de emitir eventos via Socket.IO. A forma mais limpa:
  - O `DriverRegistry` ao criar um driver, injecta-lhe uma callback:

    ```python
    driver._on_event = lambda event_data: sio.emit("event", event_data, room=f"driver_{driver_type}")
    ```

  - O driver chama `await self._on_event(data)` quando tem algo para reportar
  - Isto evita que o driver conheça o Socket.IO directamente (desacoplamento)

#### 1H — EventLog Model

- [ ] **1H.1** Criar `models.py`:

  ```python
  from django.db import models
  from django.utils import timezone
  from datetime import timedelta

  class EventLog(models.Model):
      timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
      driver_type = models.CharField(max_length=50, db_index=True)
      event_type = models.CharField(max_length=50)
      payload = models.JSONField(default=dict)
      expires_at = models.DateTimeField(db_index=True)

      class Meta:
          ordering = ["-timestamp"]
          indexes = [
              models.Index(fields=["driver_type", "timestamp"]),
          ]

      def save(self, *args, **kwargs):
          if not self.expires_at:
              self.expires_at = timezone.now() + timedelta(hours=1)
          super().save(*args, **kwargs)
  ```

- [ ] **1H.2** `python manage.py makemigrations && python manage.py migrate`

#### 1I — Limpeza de Logs

- [ ] **1I.1** Criar `cleanup.py` com tarefa periódica:

  ```python
  async def cleanup_expired_logs():
      """Corre a cada 5 minutos, apaga logs expirados."""
      while True:
          count = await database_sync_to_async(
              EventLog.objects.filter(expires_at__lt=timezone.now()).delete
          )()
          if count[0] > 0:
              logger.info("Cleaned %d expired logs", count[0])
          await asyncio.sleep(300)  # 5 min
  ```

- [ ] **1I.2** Lançar esta tarefa no `on_startup` do ASGI app, como um `asyncio.create_task`.

#### Critérios de Aceitação (Fase 1)

- [ ] Cliente HTML subscreve `rfid` → quando leitor detecta cartão → página mostra UID
- [ ] Cliente HTML subscreve `led` → envia comando `on`/`off` → LED físico liga/desliga
- [ ] Desligar o cliente → driver para após grace period
- [ ] Eventos ficam gravados no `EventLog`
- [ ] Admin Django (`/admin/`) mostra os logs

---

### FASE 2 — Button + MPR121 Capacitivo (Dia 8-11)

**Objectivo:** Adicionar 2 drivers de input com características diferentes.

#### 2A — Button Driver

- [ ] **2A.1** Criar `drivers/button.py`:
  - `DRIVER_TYPE = "button"`
  - `DIRECTION = "input"`
  - Usa `gpiozero.Button` com callback (interrupt-based, não polling)
  - Config: `{ "pin": 18, "pull_up": true, "bounce_time": 0.05 }`
  - Eventos: `{ "event": "pressed" }` e `{ "event": "released" }`

- [ ] **2A.2** Diferença para o junior:
  - O **RFID faz polling** (pergunta "tem cartão?" de 100 em 100ms)
  - O **Button usa interrupt** (o hardware avisa quando o botão é premido)
  - Ambas são abordagens válidas — depende do periférico

#### 2B — MPR121 Capacitive Touch Driver

- [ ] **2B.1** Criar `drivers/mpr121.py`:
  - `DRIVER_TYPE = "capacitive"`
  - `DIRECTION = "input"`
  - Config: `{ "addresses": ["0x5A", "0x5B"], "touch_threshold": 12, "release_threshold": 6 }`
  - Suporta 1 ou 2 boards (12 ou 24 zonas)
  - Polling loop (como RFID) — emite eventos só quando há mudança de estado (diff)
  - Eventos: `{ "event": "touch", "data": { "zone": 5 } }` e `{ "event": "release", "data": { "zone": 5 } }`

- [ ] **2B.2** Lidar com I2C errors:
  - `try/except OSError` no read
  - Re-inicializar bus em caso de falha
  - Devolver último estado conhecido enquanto recupera

#### 2C — Registar Novos Drivers

- [ ] **2C.1** Adicionar ao `DRIVER_CLASSES` no registry:

  ```python
  DRIVER_CLASSES = {
      "rfid": RFIDDriver,
      "led": LEDDriver,
      "button": ButtonDriver,          # novo
      "capacitive": MPR121Driver,      # novo
  }
  ```

#### 2D — Actualizar Página de Teste

- [ ] **2D.1** Adicionar na `test.html`:
  - Secção para subscribe de `button` com campo de pin
  - Secção para subscribe de `capacitive` com visual dos 24 sensores (grelha)
  - Log de eventos unificado

#### Critérios de Aceitação (Fase 2)

- [ ] Pressionar botão físico → evento aparece no browser
- [ ] Tocar em superfície com MPR121 → zona ilumina no browser
- [ ] Múltiplos drivers activos em simultâneo sem conflitos

---

### FASE 3 — Camera + ArUco + IR Sensor (Dia 12-17)

**Objectivo:** Adicionar drivers mais complexos — stream de vídeo, detecção de marcadores ArUco e sensor infrared.

#### 3A — Camera Driver (Base)

- [ ] **3A.1** Criar `drivers/camera.py`:
  - `DRIVER_TYPE = "camera"`
  - `DIRECTION = "both"` (input: snapshot/stream, output: configuração)
  - Usa `picamera2`
  - **A câmara é um recurso partilhado** — só pode haver 1 instância de `picamera2`. O `DriverRegistry` precisa de garantir que tanto o driver `camera` como o `aruco` (e mais tarde o `person_detector`) partilham a mesma instância da câmara.
  - Criar uma classe auxiliar `CameraProvider` (singleton) que gere o ciclo de vida:

    ```python
    class CameraProvider:
        """Singleton — gere a instância partilhada de picamera2."""
        _instance: Picamera2 | None = None
        _ref_count: int = 0
        _lock: asyncio.Lock

        async def acquire(self, config: dict) -> Picamera2: ...
        async def release(self) -> None: ...
    ```

- [ ] **3A.2** Duas funcionalidades:

  **Stream MJPEG (endpoint HTTP)**:
  - Criar view Django/aiohttp: `GET /camera/stream`
  - Content-Type: `multipart/x-mixed-replace; boundary=frame`
  - Captura frames num loop e envia como JPEG
  - O cliente abre este URL num `<img>` tag — **não usar Socket.IO para frames** (muito pesado)

  **Snapshot on-demand (Socket.IO)**:
  - Cliente envia: `{ "type": "camera", "action": "snapshot" }`
  - Responde com frame JPEG em base64 ou URL de ficheiro temporário

- [ ] **3A.3** Config: `{ "resolution": [640, 480], "framerate": 15 }`

#### 3B — ArUco Marker Detection Driver

- [ ] **3B.1** Criar `drivers/aruco.py`:
  - `DRIVER_TYPE = "aruco"`
  - `DIRECTION = "input"`
  - Usa `cv2.aruco` (do pacote `opencv-contrib-python-headless`)
  - Obtém frames da câmara via `CameraProvider` (partilhado)

- [ ] **3B.2** Lógica do driver:

  ```python
  import cv2

  # Dicionário de marcadores — configurável pelo cliente
  ARUCO_DICTS = {
      "4x4_50": cv2.aruco.DICT_4X4_50,
      "4x4_100": cv2.aruco.DICT_4X4_100,
      "5x5_100": cv2.aruco.DICT_5X5_100,
      "6x6_250": cv2.aruco.DICT_6X6_250,
      "original": cv2.aruco.DICT_ARUCO_ORIGINAL,
  }

  async def _detect_loop(self):
      detector = cv2.aruco.ArucoDetector(
          cv2.aruco.getPredefinedDictionary(self._dict_type),
          cv2.aruco.DetectorParameters(),
      )
      while self._running:
          frame = await asyncio.to_thread(self._camera.capture_array)
          gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
          corners, ids, _ = detector.detectMarkers(gray)
          if ids is not None:
              detected = [int(id) for id in ids.flatten()]
              # Emitir só quando muda (diff com estado anterior)
              if detected != self._previous_ids:
                  await self._on_event({
                      "event": "markers_detected",
                      "data": {"marker_ids": detected, "count": len(detected)},
                  })
                  self._previous_ids = detected
          elif self._previous_ids:
              await self._on_event({"event": "markers_cleared", "data": {}})
              self._previous_ids = []
          await asyncio.sleep(self._poll_interval)
  ```

- [ ] **3B.3** Config esperada do cliente:

  ```json
  {
    "type": "aruco",
    "config": {
      "dictionary": "4x4_50",
      "poll_interval": 0.1,
      "resolution": [640, 480]
    }
  }
  ```

- [ ] **3B.4** Eventos emitidos:

  ```json
  { "type": "aruco", "event": "markers_detected", "data": { "marker_ids": [0, 3, 7], "count": 3 } }
  { "type": "aruco", "event": "markers_cleared", "data": {} }
  ```

- [ ] **3B.5** Notas para o junior:
  - **ArUco markers** são imagens quadradas com padrões preto/branco que a câmara reconhece — como QR codes mas mais simples e rápidos de detectar
  - A detecção em OpenCV é **leve** (~5-10ms por frame 640×480 no RPi 5) — não tem o overhead de modelos ML
  - Usar `opencv-contrib-python-headless` (sem GUI) — muito mais leve que a versão completa
  - O `poll_interval` controla a frequência de detecção; 0.1s (10 FPS de análise) é um bom default
  - Implementar **deduplicação**: só emitir evento quando o conjunto de IDs detectados muda

- [ ] **3B.6** Testar sem câmara real (dev mode):
  - Carregar uma imagem estática com marcadores ArUco e simular a detecção
  - Ferramenta útil: gerar marcadores em <https://chev.me/arucogen/>

#### 3C — IR Sensor Driver

- [ ] **3C.1** Criar `drivers/ir_sensor.py`:
  - `DRIVER_TYPE = "ir"`
  - `DIRECTION = "input"`
  - Dois modos possíveis:
    - **Proximidade** (digital): detecta presença — GPIO interrupt
    - **Controlo remoto IR** (com receptor tipo TSOP): decodifica comandos — usa `lirc` ou bitbang
  - Começar pelo modo proximidade (simples — similar ao Button)

- [ ] **3C.2** Config: `{ "pin": 24, "mode": "proximity" }`
- [ ] **3C.3** Evento: `{ "event": "detected" }` / `{ "event": "cleared" }`

#### 3D — Registar Novos Drivers

- [ ] **3D.1** Adicionar ao `DRIVER_CLASSES` no registry:

  ```python
  DRIVER_CLASSES = {
      ...,
      "camera": CameraDriver,          # novo
      "aruco": ArucoDriver,            # novo
      "ir": IRSensorDriver,            # novo
  }
  ```

#### 3E — Actualizar Página de Teste

- [ ] **3E.1** Adicionar na `test.html`:
  - `<img>` com source `/camera/stream` para ver stream em tempo real
  - Botão para tirar snapshot
  - Secção ArUco que mostra IDs dos marcadores detectados em tempo real
  - Indicador de presença IR

#### Critérios de Aceitação (Fase 3)

- [ ] Stream da câmara visível num `<img>` no browser
- [ ] Snapshot capturado e exibido no browser
- [ ] Colocar marcador ArUco em frente à câmara → IDs aparecem no browser
- [ ] Remover marcador → evento `markers_cleared` recebido
- [ ] Sensor IR detecta presença → evento no browser
- [ ] Camera driver e ArUco driver partilham a mesma instância `picamera2` sem conflitos

---

### FASE 4 — Detecção de Pessoas com YOLO (Dia 18-23)

**Objectivo:** Adicionar detecção de pessoas via câmara usando YOLOv8, com atenção especial à performance no RPi 5.

> ⚠️ **ATENÇÃO — OVERHEAD**: YOLO é um modelo de deep learning. Mesmo a versão nano (YOLOv8n) exige significativamente mais recursos que a detecção ArUco. Esta fase requer cuidados extra de performance.

#### 4A — Análise de Performance (ANTES de implementar)

- [ ] **4A.1** Entender as limitações do RPi 5:

  | Métrica             | ArUco (Fase 3)  | YOLOv8n (esta fase)     | Impacto                     |
  | ------------------- | --------------- | ----------------------- | --------------------------- |
  | **Tempo por frame** | ~5-10ms         | ~150-300ms              | 30x mais lento              |
  | **CPU**             | ~5% de 1 core   | ~80-100% de 1 core      | Impacta outros drivers      |
  | **RAM**             | ~20 MB (OpenCV) | ~200-400 MB extra       | RPi 4GB pode ficar apertado |
  | **Resolução útil**  | 640×480         | **320×240 recomendado** | Reduzir para ganhar FPS     |
  | **FPS análise**     | 10 FPS          | **2-4 FPS máximo**      | Não é real-time suave       |

- [ ] **4A.2** Decisão de runtime — **não usar GPU** (RPi 5 não tem CUDA):
  - YOLO corre em **CPU only** via PyTorch ou ONNX Runtime
  - Alternativa mais performante: exportar para **NCNN** (optimizado para ARM):

    ```python
    from ultralytics import YOLO
    model = YOLO("yolov8n.pt")
    model.export(format="ncnn")  # Gera modelo optimizado para ARM
    ```

  - Com NCNN: ganho de ~2x performance vs PyTorch puro

#### 4B — Person Detector Driver

- [ ] **4B.1** Criar `drivers/person_detector.py`:
  - `DRIVER_TYPE = "person_detector"`
  - `DIRECTION = "input"`
  - Obtém frames da câmara via `CameraProvider` (partilhado com camera/aruco)
  - Filtra detecções: **só classe "person" (class_id=0)** — ignorar outros objectos

- [ ] **4B.2** Lógica do driver (com protecções de performance):

  ```python
  from ultralytics import YOLO

  class PersonDetectorDriver(BaseDriver):
      DRIVER_TYPE = "person_detector"
      DIRECTION = "input"

      # Limites de segurança
      MAX_RESOLUTION = (640, 480)       # Nunca aceitar mais que isto
      DEFAULT_RESOLUTION = (320, 240)   # Optimizado para RPi
      MIN_POLL_INTERVAL = 0.25          # Máximo 4 FPS de análise
      DEFAULT_CONFIDENCE = 0.5          # Threshold de confiança

      async def init(self) -> None:
          # Carregar modelo em thread separada (demora 2-5s)
          self._model = await asyncio.to_thread(
              YOLO, self.config.get("model_path", "yolov8n.pt")
          )
          self._camera = await CameraProvider().acquire(self.config)
          logger.info("YOLO model loaded: %s", self._model.model_name)

      async def _detect_loop(self):
          poll_interval = max(
              self.config.get("poll_interval", 0.5),
              self.MIN_POLL_INTERVAL,  # Nunca mais rápido que 4 FPS
          )
          confidence = self.config.get("confidence", self.DEFAULT_CONFIDENCE)

          while self._running:
              frame = await asyncio.to_thread(self._camera.capture_array)

              # Resize para resolução de análise (não da câmara)
              analysis_res = self.config.get("analysis_resolution",
                                             self.DEFAULT_RESOLUTION)
              resized = cv2.resize(frame, analysis_res)

              # Inferência em thread separada — NUNCA no event loop
              results = await asyncio.to_thread(
                  self._model.predict,
                  resized,
                  conf=confidence,
                  classes=[0],    # só "person"
                  verbose=False,
              )

              persons = []
              for r in results:
                  for box in r.boxes:
                      persons.append({
                          "confidence": round(float(box.conf[0]), 2),
                          "bbox": [round(float(x), 1) for x in box.xyxy[0]],
                      })

              current_count = len(persons)
              if current_count != self._previous_count:
                  await self._on_event({
                      "event": "person_count_changed",
                      "data": {
                          "count": current_count,
                          "persons": persons,
                      },
                  })
                  self._previous_count = current_count

              await asyncio.sleep(poll_interval)
  ```

- [ ] **4B.3** Config esperada do cliente:

  ```json
  {
    "type": "person_detector",
    "config": {
      "model_path": "yolov8n.pt",
      "analysis_resolution": [320, 240],
      "poll_interval": 0.5,
      "confidence": 0.5
    }
  }
  ```

- [ ] **4B.4** Eventos emitidos:

  ```json
  {
    "type": "person_detector",
    "event": "person_count_changed",
    "data": {
      "count": 2,
      "persons": [
        { "confidence": 0.87, "bbox": [10.0, 20.0, 150.0, 300.0] },
        { "confidence": 0.72, "bbox": [200.0, 30.0, 340.0, 310.0] }
      ]
    }
  }
  ```

#### 4C — Protecções de Performance (OBRIGATÓRIO)

- [ ] **4C.1** **Isolamento de processo** — considerar correr YOLO num processo separado:
  - Porquê: se YOLO consumir 100% do CPU num core, os outros drivers (RFID, capacitivo) podem ficar lentos
  - Opção A: `asyncio.to_thread()` — corre numa thread do ThreadPoolExecutor (mais simples)
  - Opção B: `multiprocessing` — corre num processo separado com comunicação via `multiprocessing.Queue` (mais robusto)
  - **Recomendação**: começar com `asyncio.to_thread()` (Opção A). Se houver problemas de latência nos outros drivers, migrar para Opção B.

- [ ] **4C.2** **Limites configuráveis no servidor** (não confiar no cliente):

  ```python
  # Em settings.py ou constantes do driver
  YOLO_LIMITS = {
      "max_resolution": (640, 480),     # Nunca aceitar mais
      "min_poll_interval": 0.25,        # Máximo 4 FPS
      "max_model_size": "yolov8s",      # Bloquear modelos grandes (m, l, x)
      "allowed_models": ["yolov8n", "yolov8n-ncnn"],  # Whitelist
  }
  ```

- [ ] **4C.3** **Monitorização de recursos** — adicionar ao driver:

  ```python
  import psutil

  async def _check_system_health(self) -> bool:
      """Verificar se o sistema está saudável antes de correr inferência."""
      cpu_percent = psutil.cpu_percent(interval=0.1)
      memory = psutil.virtual_memory()

      if cpu_percent > 90:
          logger.warning("CPU > 90%% — skipping YOLO frame")
          return False
      if memory.percent > 85:
          logger.warning("RAM > 85%% — skipping YOLO frame")
          return False
      return True
  ```

  - Se sistema sob pressão → **skip frame** em vez de bloquear tudo

- [ ] **4C.4** **Download do modelo na primeira utilização**:
  - O modelo `yolov8n.pt` (~6MB) é descarregado automaticamente pela lib `ultralytics`
  - Em rede isolada: pré-descarregar durante o setup:

    ```bash
    python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
    ```

  - Guardar em `/home/pi/.cache/ultralytics/` ou directório configurável

- [ ] **4C.5** **Throttle adaptativo** — se a inferência demorar mais que o `poll_interval`, ajustar automaticamente:

  ```python
  start = time.monotonic()
  results = await asyncio.to_thread(self._model.predict, ...)
  elapsed = time.monotonic() - start

  # Se inferência demorou mais que o intervalo, aumentar intervalo
  actual_interval = max(self._poll_interval, elapsed * 1.2)
  await asyncio.sleep(actual_interval)
  ```

#### 4D — Optimização NCNN (Opcional mas Recomendado)

- [ ] **4D.1** Exportar modelo para NCNN:

  ```python
  from ultralytics import YOLO
  model = YOLO("yolov8n.pt")
  model.export(format="ncnn")  # Gera pasta yolov8n_ncnn_model/
  ```

- [ ] **4D.2** Usar o modelo NCNN no driver:

  ```python
  model = YOLO("yolov8n_ncnn_model")  # Carrega automaticamente o formato NCNN
  ```

- [ ] **4D.3** Benchmarks esperados no RPi 5:
      | Formato | FPS (320×240) | FPS (640×480) | RAM |
      |---|---|---|---|
      | PyTorch (.pt) | ~2-3 FPS | ~1-2 FPS | ~350 MB |
      | NCNN | ~4-6 FPS | ~2-3 FPS | ~200 MB |

#### 4E — Registar Driver + Actualizar Página de Teste

- [ ] **4E.1** Adicionar ao `DRIVER_CLASSES`:

  ```python
  DRIVER_CLASSES = {
      ...,
      "person_detector": PersonDetectorDriver,  # novo
  }
  ```

- [ ] **4E.2** Dependências extra no `requirements.txt`:

  ```
  ultralytics>=8.0,<9.0
  psutil>=5.9
  # ncnn (instalado via ultralytics export)
  ```

- [ ] **4E.3** Adicionar na `test.html`:
  - Contador de pessoas detectadas em tempo real
  - Indicador de performance (ms por frame)
  - Indicador de carga CPU/RAM
  - Aviso visual quando sistema está sob pressão

#### Critérios de Aceitação (Fase 4)

- [ ] Subscrever `person_detector` → começa a detectar pessoas
- [ ] Pessoa entra no campo de visão → evento `person_count_changed` com `count: 1`
- [ ] Pessoa sai → evento com `count: 0`
- [ ] Os outros drivers (RFID, capacitivo, etc.) continuam responsivos durante detecção YOLO
- [ ] Sistema não crasha quando CPU/RAM estão sob pressão — skip frames em vez de bloquear
- [ ] `poll_interval` mínimo de 0.25s é respeitado mesmo que o cliente peça menos

---

## 6. Contrato Socket.IO (Referência Completa)

### Eventos Client → Server

| Evento        | Payload                                  | Descrição                                                   |
| ------------- | ---------------------------------------- | ----------------------------------------------------------- |
| `subscribe`   | `{ type: str, config: {} }`              | Subscreve um driver; inicializa hardware se necessário      |
| `unsubscribe` | `{ type: str }`                          | Cancela subscrição; liberta hardware se ninguém mais escuta |
| `command`     | `{ type: str, action: str, params: {} }` | Envia comando a um driver output                            |
| `status`      | _(vazio)_                                | Pede estado de todos os drivers activos                     |

### Eventos Server → Client

| Evento           | Payload                                               | Descrição                                   |
| ---------------- | ----------------------------------------------------- | ------------------------------------------- |
| `subscribed`     | `{ type: str, status: "ok" }`                         | Confirmação de subscrição                   |
| `unsubscribed`   | `{ type: str, status: "ok" }`                         | Confirmação de cancelamento                 |
| `event`          | `{ type: str, event: str, data: {}, timestamp: str }` | Evento de hardware (touch, card_read, etc.) |
| `command_result` | `{ type: str, status: "ok"/"error", data: {} }`       | Resposta a um comando                       |
| `driver_status`  | `{ drivers: [{ type, running, subscribers }] }`       | Estado dos drivers activos                  |
| `error`          | `{ code: str, message: str }`                         | Erro de validação ou hardware               |

---

## 7. Modelo de Dados

### EventLog

| Campo         | Tipo          | Notas                                 |
| ------------- | ------------- | ------------------------------------- |
| `id`          | AutoField     | PK                                    |
| `timestamp`   | DateTimeField | auto_now_add, indexed                 |
| `driver_type` | CharField(50) | "rfid", "led", etc. — indexed         |
| `event_type`  | CharField(50) | "card_read", "touch", "command", etc. |
| `payload`     | JSONField     | Dados do evento                       |
| `expires_at`  | DateTimeField | Timestamp de expiração — indexed      |

**Escrita**: Buffer in-memory, flush a cada 2 segundos (batch insert) — não escrever 1 evento de cada vez.

**Limpeza**: Tarefa async a cada 5 minutos apaga registos com `expires_at < now()`.

---

## 8. Fluxo Detalhado — Exemplo RFID

```
Browser                   Server (Django + Socket.IO)              Hardware (RC522)
   │                              │                                      │
   │── connect ──────────────────>│                                      │
   │<──── connected ──────────────│                                      │
   │                              │                                      │
   │── subscribe ────────────────>│                                      │
   │   {type:"rfid",              │                                      │
   │    config:{pin_rst:25}}      │── registry.subscribe() ─────────────>│
   │                              │   init() → SPI setup                 │
   │                              │   start() → polling loop             │
   │<──── subscribed ─────────────│                                      │
   │   {type:"rfid",status:"ok"}  │                                      │
   │                              │                                      │
   │                              │         ┌── poll every 100ms ──┐     │
   │                              │         │  uid = read_card()   │     │
   │                              │         │  if uid: emit event  │     │
   │                              │         └──────────────────────┘     │
   │                              │                                      │
   │                              │<──── card detected: AB:CD:EF:12 ─────│
   │<──── event ──────────────────│                                      │
   │   {type:"rfid",              │── log to EventLog ──>│               │
   │    event:"card_read",        │                      │ (SQLite)      │
   │    data:{uid:"AB:CD:EF:12"}} │                                      │
   │                              │                                      │
   │── disconnect ───────────────>│                                      │
   │                              │── registry.unsubscribe_all(sid) ───>│
   │                              │   (grace period 5s)                  │
   │                              │   stop() → cleanup SPI               │
```

---

## 9. Padrões e Boas Práticas a Seguir

### Para o Junior

1. **Nunca bloquear o event loop**: operações hardware (I2C, SPI, GPIO) são blocking → usar `asyncio.to_thread()` para as envolver
2. **Um ficheiro por driver**: mantém o código organizado e permite trabalhar num sem afectar os outros
3. **Validar SEMPRE os payloads do cliente**: usar Pydantic antes de tocar no hardware
4. **Logging generoso**: usar `logger.info()` para operações normais, `logger.error()` para falhas — vai ajudar muito no debugging com hardware
5. **try/except obrigatório** em toda a interacção com hardware — nunca deixar uma excepção I2C/SPI crashar o servidor
6. **Cleanup é obrigatório**: sempre libertar GPIO/I2C/SPI no `stop()` e `cleanup()` — senão os pins ficam "bloqueados" até reboot
7. **Commits atómicos**: um commit por tarefa (ex: "feat: add LED driver", "feat: add RFID driver") — não misturar tudo num commit gigante

### Convenções de Código

- **Docstrings**: todas as classes e métodos públicos
- **Type hints**: obrigatórias em parâmetros e returns
- **Nomes**: snake_case para funções/variáveis, PascalCase para classes
- **Imports**: stdlib → third-party → local (separados por linha em branco)
- **Constantes**: UPPER_CASE no topo do ficheiro

---

## 10. Configuração do RPi (One-time Setup)

```bash
# 1. Activar interfaces
sudo raspi-config
#   → Interface Options → I2C → Enable
#   → Interface Options → SPI → Enable
#   → Interface Options → Camera → Enable (se aplicável)
sudo reboot

# 2. Verificar hardware
sudo i2cdetect -y 1          # Deve mostrar 5a, 5b (MPR121)
ls /dev/spidev*              # Deve mostrar spidev0.0 (RC522)

# 3. WiFi Hotspot (se necessário)
sudo nmcli device wifi hotspot ssid "Kiosk-Net" password "museum123" ifname wlan0

# 4. Instalar dependências do sistema
sudo apt-get install -y python3-dev python3-venv libgpiod-dev libopencv-dev

# 5. Pré-download do modelo YOLO (para funcionar offline)
source /home/pi/kiosk/venv/bin/activate
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"  # ~6MB download
```

---

## 11. Como Correr

```bash
# Desenvolvimento
cd django-rpi-hub
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000    # HTTP only (sem Socket.IO)

# Com Socket.IO (obrigatório para funcionar)
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload
```

---

## 12. Riscos e Mitigações

| #   | Risco                                  | Impacto                        | Mitigação                                                     |
| --- | -------------------------------------- | ------------------------------ | ------------------------------------------------------------- |
| 1   | **Client envia pin inválido**          | GPIO crash ou conflito         | Whitelist de pins permitidos em cada driver                   |
| 2   | **I2C bus lockup**                     | Sensor para de responder       | Re-init do bus com try/except + retry                         |
| 3   | **Cliente desliga sem unsubscribe**    | Driver fica activo eternamente | Handler `disconnect` faz `unsubscribe_all(sid)`               |
| 4   | **Dois clientes pedem o mesmo LED**    | Conflito de comandos           | Registry partilha a instância — último comando ganha          |
| 5   | **SQLite lento sob escrita**           | Latência nos eventos           | WAL mode + batch writes + TTL agressivo                       |
| 6   | **SD card corruption**                 | Sistema não arranca            | Overlay FS em produção via `raspi-config`                     |
| 7   | **Picos de corrente nos GPIO**         | Dano no RPi                    | Resistências de protecção + documentar limites (max 16mA/pin) |
| 8   | **Driver crash afecta outros**         | Sistema instável               | Cada driver no seu asyncio.Task isolado com try/except        |
| 9   | **YOLO consome CPU inteiro**           | Outros drivers ficam lentos    | `asyncio.to_thread` + throttle adaptativo + skip sob pressão  |
| 10  | **RAM esgota com YOLO**                | OOM kill do processo           | Monitor `psutil` + limite de modelos (só nano) + NCNN         |
| 11  | **Câmara partilhada entre drivers**    | Conflito de acesso             | `CameraProvider` singleton com ref counting + asyncio.Lock    |
| 12  | **Modelo YOLO não disponível offline** | Falha na init                  | Pré-download durante setup; validar existência no `init()`    |

---

## 13. Glossário

| Termo          | Definição                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------ |
| **ASGI**       | Asynchronous Server Gateway Interface — protocolo que permite Django servir WebSockets e conexões long-lived |
| **Socket.IO**  | Protocolo de comunicação bidirecional sobre WebSocket com fallbacks automáticos                              |
| **I2C**        | Inter-Integrated Circuit — protocolo de comunicação série para ligar sensores ao RPi (2 fios: SDA + SCL)     |
| **SPI**        | Serial Peripheral Interface — protocolo série mais rápido que I2C, usado pelo RC522 RFID                     |
| **GPIO**       | General Purpose Input/Output — pinos do RPi que podem ser configurados como input ou output digital          |
| **Room**       | Conceito Socket.IO — canal lógico para enviar eventos apenas a clientes específicos                          |
| **Lazy init**  | Inicialização preguiçosa — o recurso só é criado quando é pedido pela primeira vez                           |
| **WAL mode**   | Write-Ahead Logging — modo do SQLite que melhora performance de escrita concorrente                          |
| **Overlay FS** | Sistema de ficheiros read-only que protege contra corrupção por falta de energia                             |
| **Debounce**   | Filtrar sinais repetidos/bounce de um botão ou sensor para evitar falsos positivos                           |
| **Pydantic**   | Biblioteca Python para validação de dados usando type hints                                                  |
| **ArUco**      | Marcadores fiduciais (imagens quadradas com padrões binários) usados para tracking visual — leves e rápidos  |
| **YOLO**       | You Only Look Once — família de modelos de detecção de objectos em tempo real; v8n = versão nano (mais leve) |
| **NCNN**       | Framework de inferência optimizado para dispositivos ARM (Tencent) — alternativa leve ao PyTorch             |
| **Inferência** | Processo de passar uma imagem pelo modelo ML para obter previsões (bounding boxes, classes, confiança)       |
| **Throttle**   | Limitar a taxa de execução de uma operação para evitar sobrecarregar o sistema                               |
