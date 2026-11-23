-- =============================================================
--  TimeFlies · Datos de ejemplo
--  Un usuario de demostración SIN contraseña (no puede iniciar sesión):
--  solo sirve para que el muro no salga vacío.
-- =============================================================
SET NAMES utf8mb4;
USE timeflies;

INSERT INTO usuarios (id, nombre, email, password_hash, creado_en) VALUES
 (1, 'Viajera del tiempo', 'demo@timeflies.local', NULL, NOW() - INTERVAL 20 DAY);

-- Cápsulas ya abiertas y públicas (salen en el muro)
INSERT INTO capsulas (usuario_id, titulo, mensaje, emocion, fecha_apertura, publica, abierta, abierta_en, creado_en) VALUES
 (1, 'Para mi yo de primero de DAW',
  'Si estás leyendo esto, sobreviviste a tus primeros contenedores Docker. Cuando algo no arranque, mira primero los logs.',
  'humor', NOW() - INTERVAL 2 DAY, 1, 1, NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 19 DAY),
 (1, 'Antes del primer despliegue',
  'Hoy he subido mi primera web a un servidor de verdad. Ojalá dentro de un año esto te parezca facilísimo.',
  'ilusion', NOW() - INTERVAL 5 DAY, 1, 1, NOW() - INTERVAL 5 DAY, NOW() - INTERVAL 15 DAY),
 (1, 'Gracias',
  'Gracias a quienes me ayudaron cuando me atasqué con los puertos. Devuelve el favor siempre que puedas.',
  'gratitud', NOW() - INTERVAL 1 DAY, 1, 1, NOW() - INTERVAL 1 DAY, NOW() - INTERVAL 10 DAY);

-- Cápsula todavía sellada (se abre dentro de 200 días)
INSERT INTO capsulas (usuario_id, titulo, mensaje, emocion, fecha_apertura, publica, creado_en) VALUES
 (1, 'Fin de curso', 'Mensaje sellado de ejemplo.', 'reto', NOW() + INTERVAL 200 DAY, 1, NOW() - INTERVAL 3 DAY);