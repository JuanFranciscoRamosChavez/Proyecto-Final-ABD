#  DataMask ETL

> Sistema automatizado de Extracción, Transformación y Carga (ETL) diseñado para la migración segura de datos sensibles desde entornos de Producción a QA, aplicando técnicas de enmascaramiento en tiempo real.

![React](https://img.shields.io/badge/Frontend-React%20%7C%20Vite-blue)
![Python](https://img.shields.io/badge/Backend-Python%20%7C%20Flask-yellow)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Security](https://img.shields.io/badge/Security-Fernet%20Encryption-green)

##  Visión General

DataMask ETL resuelve el problema de probar software con datos reales sin comprometer la privacidad de los usuarios. Permite sincronizar bases de datos aplicando reglas de ofuscación (hashing, nombres falsos, redacción) y cuenta con mecanismos de seguridad robustos para evitar la corrupción de datos en producción.

##  Características Principales

- **Enmascaramiento Dinámico:** Reglas configurables (Hash de emails, Faker para nombres, censura de textos).
- **Seguridad de Entornos:** Validación de huella digital (`_db_meta`) para impedir escrituras accidentales en Producción.
- **Backups Cifrados:** Generación de respaldos SQL encriptados con AES-256 (Fernet) para almacenamiento seguro.
- **Control de Roles (RBAC):**
  - **DBA:** Acceso total (Crear, Editar, Ejecutar, Respaldar, Sembrar).
  - **Desarrollador/Tester:** Solo lectura y monitoreo.
- **Data Seeding:** Generador de datos de prueba masivos utilizando `Faker`.
- **Dashboard Interactivo:** Métricas en tiempo real, historial de ejecuciones y cálculo de duración.
- **Muestreo de Datos:** Capacidad de migrar solo un porcentaje (%) de la base de datos para pruebas ligeras.

##  Tecnologías

### Frontend
- **React + Vite**: Framework principal.
- **Tailwind CSS**: Estilizado.
- **Shadcn/ui**: Componentes de interfaz modernos.
- **Lucide React**: Iconografía.

### Backend
- **Python 3.13+**: Lenguaje base.
- **Flask**: API REST.
- **SQLAlchemy + Pandas**: Manipulación y carga eficiente de datos.
- **Cryptography**: Cifrado de backups.
- **APScheduler**: Programación de tareas automáticas.

## Diagrama de arquitectura
```mermaid
graph TD
    %% DEFINICIÓN DE NODOS Y ESTILOS
    
    classDef actor fill:#2d3436,stroke:#000,stroke-width:2px,color:#fff;
    classDef frontend fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1;
    classDef backend fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20;
    classDef database fill:#fff3e0,stroke:#ef6c00,stroke-width:2px,color:#e65100;
    classDef storage fill:#f5f5f5,stroke:#616161,stroke-width:2px,color:#212121;
    classDef security fill:#fce4ec,stroke:#c2185b,stroke-width:2px,color:#880e4f;

    %% ACTORES
    User((Usuario / DBA)):::actor

    %% CAPA CLIENTE
    subgraph ClientLayer [ Capa de Presentación]
        direction TB
        UI[Frontend SPA<br/>React + Vite + Tailwind]:::frontend
    end

    %% CAPA SERVIDOR
    subgraph ServerLayer [ Capa de Aplicación - Backend]
        direction TB
        
        API[API Gateway<br/>Flask / app.py]:::backend
        Scheduler[Planificador<br/>APScheduler]:::backend
        
        subgraph ETLBox [Motor de Procesamiento]
            direction TB
            ETL[ETL Engine<br/>etl_core.py]:::backend
            Masking[Módulo de Enmascaramiento<br/>Faker + HashLib]:::backend
            Security[Validación de Entornos<br/>Check _db_meta]:::security
            Backup[Servicio de Respaldo<br/>Cifrado Fernet]:::security
        end

        ConfigFiles[Configuración<br/>config.yaml / .env]:::storage
        LocalFiles[Almacenamiento Local<br/>.sql.enc / .json]:::storage
    end

    %% CAPA DE DATOS
    subgraph DataLayer [ Capa de Datos]
        direction LR
        ProdDB[(Base de Datos<br/>PRODUCCIÓN)]:::database
        QADB[(Base de Datos<br/>QA / TEST)]:::database
    end

    %% RELACIONES Y FLUJOS
    %% Interacción Usuario
    User -->|HTTPS / Navegador| UI

    %% Comunicación Front-Back
    UI <-->|JSON / REST API| API

    %% Flujo de Control Backend
    API -->|Inicia Procesos| ETL
    Scheduler -->|Ejecución Automática| ETL
    ETL -->|Carga Reglas| ConfigFiles
    API -->|Lee/Escribe| ConfigFiles

    %% Lógica del ETL
    ETL -- 1. Valida Identidad --> Security
    Security -.->|Verifica Metadatos| ProdDB
    Security -.->|Verifica Metadatos| QADB
    
    ETL -- 2. Extrae Datos (Solo Lectura) --> ProdDB
    ETL -- 3. Transforma en Memoria --> Masking
    ETL -- 4. Carga Datos Seguros --> QADB
    
    %% Logs y Auditoría
    ETL -- 5. Registra Auditoría --> QADB
    
    %% Flujo de Respaldo
    API -->|Solicita Backup| Backup
    Backup -->|Extrae SQL| ProdDB
    Backup -->|Extrae SQL| QADB
    Backup -->|Guarda Archivo Cifrado| LocalFiles

    %% Inicialización
    InitScript[Script Inicialización<br/>init_db.py]:::backend
    API -.->|Seed Data| InitScript
    InitScript -.->|Crea Tablas + Datos| ProdDB
    InitScript -.->|Crea Estructura Vacía| QADB
```


##  Instalación y Configuración para su Ejecución Local

### 1. Backend (API Python)

1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/JuanFranciscoRamosChavez/Proyecto-Final-ABD.git
    cd Proyecto-Final-ABD
    ```

2. **Creamos y activamos un entorno virtual**
   ```bash
   # Crear el entorno en Windows 
   python -m venv venv

   # Crear el entorno en macOS/Linux
   python3 -m venv .venv
   
   # Activar en Windows
   venv\Scripts\activate
   
   # Activar en macOS/Linux
   source venv/bin/activate
   ```
   
3.  **Instalar las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Configurar variables de entorno**  
   - El archivo `.env` está en `.gitignore` y viene vacío intencionadamente.  
   - Copia la información que te proporcionaremos en la documentación anteriormente entregada y coloca todo en el archivo `.env` en tu entorno de ejecución local.
   Sin esto, la aplicación no podrá conectarse correctamente.

5. **Inicializamos el servidor**
    ```bash
    python backend/app.py
    ```

### 2. Frontend (React + Vite + Tailwind)

1. **Abrimos una nueva terminal en Proyecto-Final-ABD para cargar el frontend**
   - Instalamos las dependencias:
   ```bash
    npm install
   ```
   - Iniciamos el servidor de desarrollo:
   ```bash
    npm run dev
   ```
   - Abre tu navegador en http://localhost:8080

### 3. Como decifrar el `.sql.enc`:

1. **Usamos el código creado para decifrar nuestras copias de seguridad:**

   ```bash
    python backend/restore_util.py
   ```

### Uso y Guía de Roles
Explicamos cómo entrar y qué hacer.

#### Primeros Pasos

1. **Inicializar Entornos:** Al iniciar por primera vez, ingresa como DBA y ve a *Pipelines*. Haz clic en **"Generar Datos Fuente"**. Esto creará las tablas en Producción y etiquetará las bases de datos para seguridad.
2. **Sincronizar:** Usa el botón **"Sincronizar"** para que el sistema detecte automáticamente las tablas existentes y cree los pipelines.
3. **Ejecutar:** Puedes ejecutar una migración completa o definir un porcentaje de muestreo (ej. 20%).
4. **Respaldos:** Antes de operaciones críticas, usa el botón **"Crear Respaldo"**. Se generará un archivo `.sql.enc` cifrado.
