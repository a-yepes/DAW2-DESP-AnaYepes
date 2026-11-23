-- =============================================================
--  TimeFlies · Estructura de la base de datos
--  MariaDB lo ejecuta automáticamente la PRIMERA vez que arranca
--  (cuando el volumen timeflies_data está vacío).
-- =============================================================
SET NAMES utf8mb4;     -- para que tildes, ñ y emojis se guarden bien
USE timeflies;

-- Cuentas de usuario
CREATE TABLE IF NOT EXISTS usuarios (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    email         VARCHAR(150) NOT NULL UNIQUE,              -- no puede haber dos cuentas con el mismo email
    password_hash VARCHAR(255) NULL,                         -- NULL si la cuenta es de Google
    proveedor     VARCHAR(10)  NOT NULL DEFAULT 'local',     -- 'local' (email) o 'google'
    es_admin      TINYINT(1)   NOT NULL DEFAULT 0,           -- 1 = administrador
    creado_en     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) DEFAULT CHARSET=utf8mb4;

-- Cápsulas del tiempo
CREATE TABLE IF NOT EXISTS capsulas (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id     INT NOT NULL,
    titulo         VARCHAR(120) NOT NULL,
    mensaje        TEXT NOT NULL,
    emocion        VARCHAR(20)  NOT NULL DEFAULT 'ilusion',
    fecha_apertura DATETIME     NOT NULL,                    -- hasta esta fecha está sellada
    publica        TINYINT(1)   NOT NULL DEFAULT 0,          -- 1 = se muestra en el muro al abrirse
    abierta        TINYINT(1)   NOT NULL DEFAULT 0,
    abierta_en     DATETIME     NULL,
    oculta         TINYINT(1)   NOT NULL DEFAULT 0,          -- el admin puede ocultarla del muro
    creado_en      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) DEFAULT CHARSET=utf8mb4;

-- Conversaciones con el Oráculo (IA)
CREATE TABLE IF NOT EXISTS mensajes_ia (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    pregunta   TEXT NOT NULL,
    respuesta  TEXT NOT NULL,
    creado_en  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) DEFAULT CHARSET=utf8mb4;