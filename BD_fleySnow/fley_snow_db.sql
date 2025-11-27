-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3320
-- Tiempo de generación: 27-11-2025 a las 18:07:33
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `fley_snow_db`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_activar_agricultor` (IN `p_id_agricultor` INT)   BEGIN
    UPDATE agricultores
    SET estado = 1
    WHERE id_agricultor = p_id_agricultor;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_agricultor` (IN `p_id_agricultor` INT, IN `p_codigo_agricultor` VARCHAR(5), IN `p_dni` VARCHAR(8), IN `p_nombres` VARCHAR(100), IN `p_apellidos` VARCHAR(100), IN `p_telefono` VARCHAR(9), IN `p_direccion` VARCHAR(150), IN `p_correo` VARCHAR(100), IN `p_zona` VARCHAR(100), IN `p_cultivo_principal` VARCHAR(100), IN `p_estado` TINYINT)   BEGIN
    UPDATE agricultores
    SET codigo_agricultor = p_codigo_agricultor,
        dni = p_dni,
        nombres = p_nombres,
        apellidos = p_apellidos,
        telefono = p_telefono,
        direccion = p_direccion,
        correo = p_correo,
        zona = p_zona,
        cultivo_principal = p_cultivo_principal,
        estado = p_estado
    WHERE id_agricultor = p_id_agricultor;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_categoria` (IN `p_id` INT, IN `p_codigo` VARCHAR(5), IN `p_nombre` VARCHAR(100))   BEGIN
    UPDATE categorias 
    SET codigo_categoria = p_codigo,
        nombre_categoria = p_nombre
    WHERE id_categoria = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_detalle_recepcion` (IN `p_id_detalle` INT, IN `p_id_variedad` INT, IN `p_lote` VARCHAR(50), IN `p_peso_bruto` DECIMAL(10,2), IN `p_cantidad_jabas` INT, IN `p_peso_neto` DECIMAL(10,2), IN `p_unidad_medida` VARCHAR(20))   BEGIN
    UPDATE detalle_recepcion_materia_prima
    SET 
        id_variedad = p_id_variedad,
        lote = p_lote,
        peso_bruto = p_peso_bruto,
        cantidad_jabas = p_cantidad_jabas,
        peso_neto = p_peso_neto,
        unidad_medida = p_unidad_medida
    WHERE id_detalle = p_id_detalle;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_estado_nota` (IN `p_id_nota` INT, IN `p_estado` ENUM('pendiente','aprobado','anulado'))   BEGIN
    UPDATE nota_movimiento
    SET estado = p_estado
    WHERE id_nota = p_id_nota;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_estado_recepcion` (IN `p_id_recepcion` INT, IN `p_estado` ENUM('pendiente','aprobado','anulado'))   BEGIN
    UPDATE recepcion_materia_prima
    SET estado = p_estado
    WHERE id_recepcion = p_id_recepcion;

    -- Si la recepción se finaliza, se devuelven las jabas al stock
    IF p_estado = 'aprobado' THEN
        UPDATE jabas_stock js
        INNER JOIN recepcion_materia_prima r ON js.id_agricultor = r.id_agricultor
        SET js.cantidad = js.cantidad + (
            SELECT IFNULL(SUM(dr.cantidad_jabas), 0)
            FROM detalle_recepcion_materia_prima dr
            WHERE dr.id_recepcion = p_id_recepcion
        )
        WHERE r.id_recepcion = p_id_recepcion;
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_insumo` (IN `p_id` INT, IN `p_codigo` VARCHAR(50), IN `p_nombre` VARCHAR(255), IN `p_categoria` INT, IN `p_variedad` INT, IN `p_stock` INT, IN `p_unidad` VARCHAR(50), IN `p_vencimiento` DATE, IN `p_descripcion` TEXT)   BEGIN
    UPDATE insumos
    SET codigo_insumo = p_codigo,
        nombre_insumo = p_nombre,
        id_categoria = p_categoria,
        id_variedad = p_variedad,
        stock_actual = p_stock,
        unidad_medida = p_unidad,
        fecha_vencimiento = p_vencimiento,
        descripcion = p_descripcion
    WHERE id_insumo = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_nota_movimiento` (IN `p_id_nota` INT, IN `p_id_tipo` INT, IN `p_referencia` VARCHAR(100), IN `p_id_usuario` INT, IN `p_id_origen` INT, IN `p_observacion` TEXT, IN `p_fecha` DATETIME)   BEGIN
    UPDATE nota_movimiento
    SET id_tipo = p_id_tipo,
        referencia = p_referencia,
        id_usuario = p_id_usuario,
        id_origen = p_id_origen,
        observacion = p_observacion,
        fecha = p_fecha
    WHERE id_nota = p_id_nota;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_recepcion` (IN `p_id_recepcion` INT, IN `p_id_agricultor` INT, IN `p_observaciones` TEXT, IN `p_id_responsable` INT, IN `p_estado` ENUM('pendiente','aprobado','anulado'))   BEGIN
    UPDATE recepcion_materia_prima
    SET 
        id_agricultor = p_id_agricultor,
        observaciones = p_observaciones,
        id_responsable = p_id_responsable,
        estado = p_estado
    WHERE id_recepcion = p_id_recepcion;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_ultimo_login` (IN `p_id_usuario` INT)   BEGIN
    UPDATE usuarios 
    SET ultimo_login = NOW()
    WHERE id_usuario = p_id_usuario;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_usuario` (IN `p_id_usuario` INT, IN `p_nombre_completo` VARCHAR(100), IN `p_dni` CHAR(8), IN `p_email` VARCHAR(100), IN `p_telefono` CHAR(9), IN `p_id_rol` INT, IN `p_estado` TINYINT)   BEGIN
    UPDATE usuarios
    SET nombre_completo = p_nombre_completo,
        dni = p_dni,
        email = p_email,
        telefono = p_telefono,
        id_rol = p_id_rol,
        estado = p_estado
    WHERE id_usuario = p_id_usuario;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_variedad` (IN `p_id` INT, IN `p_codigo` VARCHAR(5), IN `p_nombre` VARCHAR(100), IN `p_id_categoria` INT)   BEGIN
    UPDATE variedades 
    SET codigo_variedad = p_codigo,
        nombre_variedad = p_nombre, 
        id_categoria = p_id_categoria
    WHERE id_variedad = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_agregar_detalle_movimiento` (IN `p_id_nota` INT, IN `p_id_insumo` INT, IN `p_id_tipo` INT, IN `p_cantidad` DECIMAL(10,2), IN `p_unidad_medida` VARCHAR(20))   BEGIN
    INSERT INTO movimientos_inventario(
        id_nota, id_insumo, id_tipo, cantidad, unidad_medida, fecha_movimiento, estado
    )
    VALUES(p_id_nota, p_id_insumo, p_id_tipo, p_cantidad, p_unidad_medida, NOW(), 'activo');

    -- Retornar el ID generado
    SELECT LAST_INSERT_ID() AS id_movimiento;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_agregar_detalle_recepcion` (IN `p_id_recepcion` INT, IN `p_id_variedad` INT, IN `p_lote` VARCHAR(50), IN `p_peso_bruto` DECIMAL(10,2), IN `p_cantidad_jabas` INT, IN `p_peso_neto` DECIMAL(10,2), IN `p_unidad_medida` VARCHAR(20))   BEGIN
    INSERT INTO detalle_recepcion_materia_prima(
        id_recepcion,
        id_variedad,
        lote,
        peso_bruto,
        cantidad_jabas,
        peso_neto,
        unidad_medida,
        estado,
        fecha_registro
    ) VALUES (
        p_id_recepcion,
        p_id_variedad,
        p_lote,
        p_peso_bruto,
        p_cantidad_jabas,
        p_peso_neto,
        p_unidad_medida,
        'activo',
        NOW()
    );
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_aprobar_nota_movimiento` (IN `p_id_nota` INT)   BEGIN
    DECLARE v_count INT DEFAULT 0;

    -- Empezar transacción
    START TRANSACTION;

    -- Crear tabla temporal con el delta por insumo (positivo = sumar, negativo = restar)
    CREATE TEMPORARY TABLE tmp_delta
    ENGINE = MEMORY
    AS
    SELECT 
        m.id_insumo,
        SUM(
            CASE
                WHEN m.id_tipo IN (1,3,5) THEN m.cantidad  -- Entrada, Ajuste, Devolución
                WHEN m.id_tipo IN (2,4) THEN -m.cantidad  -- Salida, Baja
                ELSE 0
            END
        ) AS delta
    FROM movimientos_inventario m
    WHERE m.id_nota = p_id_nota
      AND m.estado = 'activo'
    GROUP BY m.id_insumo;

    -- Validar que ninguna actualización vaya a dejar stock negativo
    SELECT COUNT(*) INTO v_count
    FROM insumos i
    JOIN tmp_delta t ON i.id_insumo = t.id_insumo
    WHERE i.stock_actual + t.delta < 0;

    IF v_count > 0 THEN
        DROP TEMPORARY TABLE IF EXISTS tmp_delta;
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stock insuficiente para aprobar la nota. Revisa cantidades.';
    END IF;

    -- Aplicar los cambios de stock
    UPDATE insumos i
    JOIN tmp_delta t ON i.id_insumo = t.id_insumo
    SET i.stock_actual = i.stock_actual + t.delta;

    -- Generar alertas para los insumos que quedaron por debajo del mínimo
    INSERT INTO alertas (id_insumo, mensaje, fecha_alerta, visto)
    SELECT i.id_insumo,
           CONCAT('⚠️ El stock del insumo ', i.nombre_insumo, ' quedó en ', i.stock_actual, 
                  ' (mínimo: ', i.stock_minimo, ').'),
           NOW(),
           0
    FROM insumos i
    JOIN tmp_delta t ON i.id_insumo = t.id_insumo
    WHERE i.stock_actual < i.stock_minimo;

    -- Marcar nota como aprobada
    UPDATE nota_movimiento
    SET estado = 'aprobado'
    WHERE id_nota = p_id_nota;

    COMMIT;

    DROP TEMPORARY TABLE IF EXISTS tmp_delta;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_aprobar_recepcion` (IN `p_id_recepcion` INT)   BEGIN
    UPDATE recepcion_materia_prima
    SET estado = 'aprobado'
    WHERE id_recepcion = p_id_recepcion;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_cambiar_contrasena` (IN `p_id_usuario` INT, IN `p_contrasena` VARCHAR(255))   BEGIN
    UPDATE usuarios
    SET contrasena = p_contrasena
    WHERE id_usuario = p_id_usuario;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_cambiar_estado_insumo` (IN `p_id` INT, IN `p_estado` BOOLEAN)   BEGIN
    UPDATE insumos
    SET estado = p_estado
    WHERE id_insumo = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_control_jabas_agricultor` (IN `p_id_agricultor` INT)   BEGIN

    SELECT 
        ns.id_nota,
        ns.codigo_nota,
        ns.fecha,
        ns.estado,
        COALESCE(SUM(mi.cantidad), 0) AS cantidad_salida,

        -- 🔹 Total de jabas recepcionadas (en notas aprobadas)
        COALESCE((
            SELECT SUM(drmp.cantidad_jabas)
            FROM recepcion_materia_prima rmp
            INNER JOIN detalle_recepcion_materia_prima drmp 
                ON rmp.id_recepcion = drmp.id_recepcion
            WHERE rmp.id_nota_salida = ns.id_nota
              AND rmp.estado = 'aprobado'
        ), 0) AS cantidad_recepcionada,

        -- 🔹 Saldo pendiente de jabas
        (
            COALESCE(SUM(mi.cantidad), 0) -
            COALESCE((
                SELECT SUM(drmp.cantidad_jabas)
                FROM recepcion_materia_prima rmp
                INNER JOIN detalle_recepcion_materia_prima drmp 
                    ON rmp.id_recepcion = drmp.id_recepcion
                WHERE rmp.id_nota_salida = ns.id_nota
                  AND rmp.estado = 'aprobado'
            ), 0)
        ) AS saldo_jabas

    FROM nota_movimiento ns
    INNER JOIN movimientos_inventario mi ON ns.id_nota = mi.id_nota
    INNER JOIN insumos i ON mi.id_insumo = i.id_insumo

    WHERE ns.id_origen = p_id_agricultor
      AND i.nombre_insumo LIKE '%jaba%'
      AND ns.estado = 'aprobado'
      AND ns.codigo_nota LIKE 'NS-%'

    GROUP BY ns.id_nota, ns.codigo_nota, ns.fecha, ns.estado
    HAVING saldo_jabas > 0
    ORDER BY ns.fecha DESC;

END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_crear_nota_movimiento` (IN `p_id_tipo` INT, IN `p_referencia` VARCHAR(100), IN `p_id_usuario` INT, IN `p_id_origen` INT, IN `p_observacion` VARCHAR(150))   BEGIN
  DECLARE v_prefijo VARCHAR(2);
  DECLARE v_num INT;
  DECLARE v_codigo VARCHAR(10);
  DECLARE v_nombre_tipo VARCHAR(50);

  -- Obtener el nombre del tipo desde la tabla tipo_movimiento
  SELECT nombre INTO v_nombre_tipo
  FROM tipo_movimiento
  WHERE id_tipo = p_id_tipo
  LIMIT 1;

  -- Determinar prefijo según el nombre (no según el ID)
  IF LOWER(v_nombre_tipo) = 'salida' THEN
    SET v_prefijo = 'NS';
  ELSEIF LOWER(v_nombre_tipo) = 'entrada' THEN
    SET v_prefijo = 'NE';
  ELSEIF LOWER(v_nombre_tipo) = 'ajuste' THEN
    SET v_prefijo = 'NA';
  ELSEIF LOWER(v_nombre_tipo) IN ('devolución','devolucion') THEN
    SET v_prefijo = 'ND';
  ELSEIF LOWER(v_nombre_tipo) = 'baja' THEN
    SET v_prefijo = 'NB';
  ELSE
    SET v_prefijo = 'NM'; -- fallback si hace falta
  END IF;

  -- Obtener último número para ese prefijo
  SELECT IFNULL(MAX(CAST(SUBSTRING(codigo_nota, 4) AS UNSIGNED)), 0) + 1
    INTO v_num
  FROM nota_movimiento
  WHERE codigo_nota LIKE CONCAT(v_prefijo, '-%');

  SET v_codigo = CONCAT(v_prefijo, '-', LPAD(v_num, 5, '0'));

  -- Insertar la nota de movimiento
  INSERT INTO nota_movimiento (
    codigo_nota, id_tipo, referencia, id_usuario, id_origen, observacion, estado
  ) VALUES (
    v_codigo, p_id_tipo, p_referencia, p_id_usuario, p_id_origen, p_observacion, 'pendiente'
  );

  -- Retornar código generado e id insertado
  SELECT v_codigo AS codigo_generado, LAST_INSERT_ID() AS id_nota;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_crear_recepcion` (IN `p_id_agricultor` INT, IN `p_id_variedad` INT, IN `p_lote` VARCHAR(50), IN `p_peso_bruto` DECIMAL(10,2), IN `p_cantidad_jabas` INT, IN `p_peso_neto` DECIMAL(10,2), IN `p_observaciones` TEXT, IN `p_id_responsable` INT)   BEGIN
    DECLARE v_num INT;
    DECLARE v_codigo VARCHAR(10);

    -- Obtener último número de recepción
    SELECT IFNULL(MAX(CAST(SUBSTRING(codigo_recepcion,4) AS UNSIGNED)),0) + 1
    INTO v_num
    FROM recepcion_materia_prima
    WHERE codigo_recepcion LIKE 'NR-%';

    SET v_codigo = CONCAT('NR-',LPAD(v_num,5,'0'));

    -- Insertar la recepción
    INSERT INTO recepcion_materia_prima(
        codigo_recepcion, id_agricultor, id_variedad, lote,
        peso_bruto, cantidad_jabas, peso_neto, observaciones,
        id_responsable, fecha_recepcion, hora_recepcion, estado
    )
    VALUES(
        v_codigo, p_id_agricultor, p_id_variedad, p_lote,
        p_peso_bruto, p_cantidad_jabas, p_peso_neto, p_observaciones,
        p_id_responsable, CURDATE(), CURTIME(), 'pendiente'
    );
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_crear_recepcion_materia_prima` (IN `p_id_nota_salida` INT, IN `p_id_agricultor` INT, IN `p_fecha_recepcion` DATE, IN `p_observaciones` TEXT, IN `p_id_responsable` INT)   BEGIN
    DECLARE nuevo_codigo VARCHAR(10);
    DECLARE ultimo_codigo VARCHAR(10);
    DECLARE nuevo_numero INT;

    -- Generar código tipo NR-00001
    SELECT codigo_recepcion INTO ultimo_codigo
    FROM recepcion_materia_prima
    ORDER BY id_recepcion DESC
    LIMIT 1;

    IF ultimo_codigo IS NULL THEN
        SET nuevo_codigo = 'NR-00001';
    ELSE
        SET nuevo_numero = CAST(SUBSTRING(ultimo_codigo, 4) AS UNSIGNED) + 1;
        SET nuevo_codigo = CONCAT('NR-', LPAD(nuevo_numero, 5, '0'));
    END IF;

    -- Insertar cabecera
    INSERT INTO recepcion_materia_prima(
        codigo_recepcion, id_nota_salida, id_agricultor,
        fecha_recepcion, hora_recepcion,
        observaciones, id_responsable, estado, fecha_registro
    )
    VALUES (
        nuevo_codigo, p_id_nota_salida, p_id_agricultor,
        p_fecha_recepcion, NOW(),
        p_observaciones, p_id_responsable, 'pendiente', NOW()
    );

    SELECT LAST_INSERT_ID() AS id_recepcion, nuevo_codigo AS codigo_recepcion;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_desactivar_agricultor` (IN `p_id_agricultor` INT)   BEGIN
    UPDATE agricultores
    SET estado = 0
    WHERE id_agricultor = p_id_agricultor;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_detalle_recepcion` (IN `p_id_recepcion` INT)   BEGIN
    SELECT 
        d.id_detalle,
        v.nombre_variedad,
        d.lote,
        d.peso_bruto,
        d.cantidad_jabas,
        d.peso_neto,
        d.unidad_medida,
        d.estado,
        d.fecha_registro
    FROM detalle_recepcion_materia_prima d
    INNER JOIN variedades v ON d.id_variedad = v.id_variedad
    WHERE d.id_recepcion = p_id_recepcion;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_eliminar_categoria` (IN `p_id` INT)   BEGIN
    DELETE FROM categorias WHERE id_categoria = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_eliminar_detalles_movimiento` (IN `p_id_nota` INT)   BEGIN
    DELETE FROM movimientos_inventario
    WHERE id_nota = p_id_nota;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_eliminar_detalles_recepcion` (IN `p_id_recepcion` INT)   BEGIN
    UPDATE detalle_recepcion_materia_prima
    SET estado = 'anulado'
    WHERE id_recepcion = p_id_recepcion;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_eliminar_detalle_recepcion` (IN `p_id_detalle` INT)   BEGIN
    DELETE FROM detalle_recepcion_materia_prima
    WHERE id_detalle = p_id_detalle;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_eliminar_variedad` (IN `p_id` INT)   BEGIN
    DELETE FROM variedades WHERE id_variedad = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_guardar_permisos_usuario` (IN `p_id_usuario` INT, IN `p_codigos` TEXT)   BEGIN
    -- Manejo de errores para transacción
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    -- 1) Eliminar permisos previos del usuario
    DELETE FROM permisos WHERE id_usuario = p_id_usuario;

    -- 2) Insertar nuevos permisos usando los códigos separados por coma
    IF p_codigos IS NOT NULL AND p_codigos <> '' THEN
        -- Opcional: quitar espacios por si te llegan "USU_VER, USU_NEW"
        SET p_codigos = REPLACE(p_codigos, ' ', '');

        SET @sql = CONCAT(
            'INSERT INTO permisos (id_usuario, id_accion, permitido) ',
            'SELECT ', p_id_usuario, ', a.id_accion, 1 ',
            'FROM acciones a ',
            'WHERE a.codigo IN (''', REPLACE(p_codigos, ',', ''','''), ''')'
        );

        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;

    COMMIT;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insertar_categoria` (IN `p_codigo` VARCHAR(5), IN `p_nombre` VARCHAR(100))   BEGIN
    INSERT INTO categorias(codigo_categoria, nombre_categoria) 
    VALUES (p_codigo, p_nombre);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insertar_insumo` (IN `p_codigo` VARCHAR(50), IN `p_nombre` VARCHAR(255), IN `p_categoria` INT, IN `p_variedad` INT, IN `p_stock` INT, IN `p_unidad` VARCHAR(50), IN `p_vencimiento` DATE, IN `p_descripcion` TEXT, IN `p_estado` BOOLEAN)   BEGIN
    INSERT INTO insumos (codigo_insumo, nombre_insumo, id_categoria, id_variedad, 
                         stock_actual, unidad_medida, fecha_vencimiento, descripcion, estado)
    VALUES (p_codigo, p_nombre, p_categoria, p_variedad, p_stock, p_unidad, 
            p_vencimiento, p_descripcion, p_estado);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insertar_rol` (IN `p_nombre_rol` VARCHAR(50), IN `p_descripcion` TEXT)   BEGIN
    IF EXISTS (SELECT 1 FROM roles WHERE nombre_rol = p_nombre_rol) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El rol ya existe';
    END IF;

    INSERT INTO roles (nombre_rol, descripcion, fecha_creacion)
    VALUES (p_nombre_rol, p_descripcion, NOW());
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insertar_usuario` (IN `p_nombre_completo` VARCHAR(100), IN `p_dni` CHAR(8), IN `p_contrasena` VARCHAR(255), IN `p_email` VARCHAR(100), IN `p_telefono` CHAR(9), IN `p_id_rol` INT)   BEGIN
    INSERT INTO usuarios (nombre_completo, dni, contrasena, email, telefono, id_rol, estado, fecha_creacion)
    VALUES (p_nombre_completo, p_dni, p_contrasena, p_email, p_telefono, p_id_rol, 1, NOW());
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insertar_variedad` (IN `p_codigo` VARCHAR(5), IN `p_nombre` VARCHAR(100), IN `p_id_categoria` INT)   BEGIN
    INSERT INTO variedades(codigo_variedad, nombre_variedad, id_categoria) 
    VALUES (p_codigo, p_nombre, p_id_categoria);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insumos_stock_bajo` ()   BEGIN
    SELECT 
        id_insumo,
        codigo_insumo,
        nombre_insumo,
        stock_actual,
        stock_minimo
    FROM insumos
    WHERE stock_actual < stock_minimo
    ORDER BY stock_actual ASC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_kardex_insumo` (IN `p_id_insumo` INT)   BEGIN
    SET @saldo := 0;

    SELECT 
        m.id_movimiento,
        m.fecha_movimiento,
        t.id_tipo,
        t.nombre AS tipo_movimiento,
        m.cantidad,
        m.unidad_medida,
        n.referencia,  -- ahora viene de nota_movimiento
        @saldo := CASE
            WHEN LOWER(t.nombre) IN ('entrada', 'devolución', 'devolucion') 
                THEN @saldo + m.cantidad
            WHEN LOWER(t.nombre) IN ('salida', 'baja') 
                THEN @saldo - m.cantidad
            WHEN LOWER(t.nombre) = 'ajuste'
                THEN @saldo + m.cantidad
            ELSE @saldo
        END AS saldo
    FROM movimientos_inventario m
    INNER JOIN tipo_movimiento t ON m.id_tipo = t.id_tipo
    INNER JOIN nota_movimiento n ON m.id_nota = n.id_nota
    JOIN (SELECT @saldo := 0) init
    WHERE m.id_insumo = p_id_insumo
    ORDER BY m.fecha_movimiento ASC, m.id_movimiento ASC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_listar_acciones` ()   BEGIN
    SELECT 
        modulo,
        id_accion,
        nombre_accion,
        descripcion,
        codigo
    FROM acciones
    ORDER BY modulo, id_accion;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_listar_agricultores` (IN `p_q` VARCHAR(100), IN `p_estado` VARCHAR(20), IN `p_fecha_inicio` DATE, IN `p_fecha_fin` DATE)   BEGIN
    SELECT 
        a.id_agricultor,
        a.codigo_agricultor,
        a.dni,
        CONCAT(a.nombres, ' ', a.apellidos) AS nombre_completo,
        a.telefono,
        a.direccion,
        a.correo,
        a.zona,
        a.cultivo_principal,
        a.fecha_registro,
        CASE 
            WHEN a.estado = 1 THEN 'Activo'
            ELSE 'Inactivo'
        END AS estado
    FROM agricultores a
    WHERE 1=1
        -- 🔍 Búsqueda general (nombre, DNI o código)
        AND (
            p_q IS NULL 
            OR LOWER(CONCAT(a.nombres, ' ', a.apellidos)) COLLATE utf8mb4_general_ci LIKE CONCAT('%', LOWER(p_q), '%')
            OR a.dni COLLATE utf8mb4_general_ci LIKE CONCAT('%', p_q, '%')
            OR a.codigo_agricultor COLLATE utf8mb4_general_ci LIKE CONCAT('%', p_q, '%')
        )

        -- ⚙️ Filtro por estado (Activo / Inactivo)
        AND (
            p_estado IS NULL 
            OR (p_estado = 'Activo' AND a.estado = 1)
            OR (p_estado = 'Inactivo' AND a.estado = 0)
        )

        -- 📆 Filtro por rango de fechas
        AND (
            (p_fecha_inicio IS NULL AND p_fecha_fin IS NULL)
            OR (p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NOT NULL AND DATE(a.fecha_registro) BETWEEN p_fecha_inicio AND p_fecha_fin)
            OR (p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NULL AND DATE(a.fecha_registro) >= p_fecha_inicio)
            OR (p_fecha_fin IS NOT NULL AND p_fecha_inicio IS NULL AND DATE(a.fecha_registro) <= p_fecha_fin)
        )

    ORDER BY a.fecha_registro DESC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_listar_categorias` ()   BEGIN
    SELECT 
        c.id_categoria, 
        c.codigo_categoria, 
        c.nombre_categoria,
        CASE 
            WHEN EXISTS (
                SELECT 1 
                FROM variedades v 
                WHERE v.id_categoria = c.id_categoria
            ) 
            THEN TRUE 
            ELSE FALSE 
        END AS tiene_variedades
    FROM categorias c;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_listar_insumos` (IN `p_q` VARCHAR(100), IN `p_id_categoria` INT, IN `p_id_variedad` INT, IN `p_estado` VARCHAR(10), IN `p_fecha_inicio` DATE, IN `p_fecha_fin` DATE)   BEGIN
    SELECT 
        i.id_insumo,
        i.codigo_insumo,
        i.nombre_insumo,
        c.nombre_categoria AS categoria,
        v.nombre_variedad AS variedad,
        i.stock_actual,
        i.stock_minimo,
        i.unidad_medida,
        i.fecha_ingreso,
        i.fecha_vencimiento,
        i.descripcion,
        i.estado
    FROM insumos i
    LEFT JOIN categorias c ON i.id_categoria = c.id_categoria
    LEFT JOIN variedades v ON i.id_variedad = v.id_variedad
    WHERE 1=1
        -- Filtro búsqueda general
        AND (
            p_q IS NULL OR
            LOWER(i.nombre_insumo) LIKE CONCAT('%', LOWER(p_q), '%')
            OR LOWER(i.codigo_insumo) LIKE CONCAT('%', LOWER(p_q), '%')
            OR LOWER(c.nombre_categoria) LIKE CONCAT('%', LOWER(p_q), '%')
        )
        -- Filtro categoría
        AND (p_id_categoria IS NULL OR i.id_categoria = p_id_categoria)
        -- Filtro variedad
        AND (p_id_variedad IS NULL OR i.id_variedad = p_id_variedad)
        -- Filtro estado
        AND (p_estado IS NULL OR 
             (p_estado = '1' AND i.estado = 1) OR 
             (p_estado = '0' AND i.estado = 0))
        -- Filtro por rango de fechas (fecha_ingreso)
        AND (
            (p_fecha_inicio IS NULL AND p_fecha_fin IS NULL)
            OR (p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NOT NULL AND DATE(i.fecha_ingreso) BETWEEN p_fecha_inicio AND p_fecha_fin)
            OR (p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NULL AND DATE(i.fecha_ingreso) >= p_fecha_inicio)
            OR (p_fecha_fin IS NOT NULL AND p_fecha_inicio IS NULL AND DATE(i.fecha_ingreso) <= p_fecha_fin)
        )
    ORDER BY i.fecha_ingreso DESC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_listar_notas_movimiento` (IN `p_q` VARCHAR(100), IN `p_id_tipo` INT, IN `p_estado` VARCHAR(20), IN `p_fecha_inicio` DATE, IN `p_fecha_fin` DATE)   BEGIN
    SELECT 
        nm.id_nota, 
        nm.codigo_nota, 
        tm.nombre AS tipo_movimiento,
        nm.fecha, 
        nm.referencia, 
        u.nombre_completo AS usuario, 
        o.nombre AS origen_destino, 
        nm.observacion, 
        nm.estado
    FROM nota_movimiento nm
    INNER JOIN tipo_movimiento tm ON nm.id_tipo = tm.id_tipo
    LEFT JOIN usuarios u ON nm.id_usuario = u.id_usuario
    LEFT JOIN origen_destino o ON nm.id_origen = o.id_origen
    WHERE 1=1
        -- 🔍 Búsqueda general (ignora mayúsculas/minúsculas)
        AND (
            p_q IS NULL OR p_q = '' OR
            LOWER(nm.codigo_nota) LIKE CONCAT('%', LOWER(p_q), '%') OR
            LOWER(tm.nombre) LIKE CONCAT('%', LOWER(p_q), '%') OR
            LOWER(nm.referencia) LIKE CONCAT('%', LOWER(p_q), '%') OR
            LOWER(u.nombre_completo) LIKE CONCAT('%', LOWER(p_q), '%') OR
            LOWER(o.nombre) LIKE CONCAT('%', LOWER(p_q), '%') OR
            LOWER(nm.observacion) LIKE CONCAT('%', LOWER(p_q), '%')
        )
        -- 🎯 Filtro por tipo
        AND (p_id_tipo IS NULL OR nm.id_tipo = p_id_tipo)
        -- 📋 Filtro por estado
        AND (p_estado IS NULL OR nm.estado = p_estado)
        -- 🗓️ Filtro por rango de fechas
        AND (
            (p_fecha_inicio IS NULL AND p_fecha_fin IS NULL)
            OR (p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NOT NULL AND DATE(nm.fecha) BETWEEN p_fecha_inicio AND p_fecha_fin)
            OR (p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NULL AND DATE(nm.fecha) >= p_fecha_inicio)
            OR (p_fecha_fin IS NOT NULL AND p_fecha_inicio IS NULL AND DATE(nm.fecha) <= p_fecha_fin)
        )
    ORDER BY nm.fecha DESC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_listar_origenes` ()   BEGIN
    SELECT 
        o.id_origen,
        o.tipo,
        o.codigo,
        o.dni,
        o.nombre
    FROM origen_destino o

    UNION ALL

    SELECT 
        a.id_agricultor AS id_origen,
        'agricultor' AS tipo,
        a.codigo_agricultor,
        a.dni,
        CONCAT(a.nombres, ' ', IFNULL(a.apellidos, '')) AS nombre
    FROM agricultores a
    WHERE a.estado = 1
    ORDER BY tipo, nombre;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_listar_recepciones_detalle` (IN `p_q` VARCHAR(100), IN `p_estado` VARCHAR(20), IN `p_fecha_inicio` DATE, IN `p_fecha_fin` DATE, IN `p_id_agricultor` INT)   BEGIN
    SELECT 
        r.id_recepcion,
        r.codigo_recepcion,
        CONCAT(a.nombres, ' ', a.apellidos) AS agricultor,
        r.fecha_recepcion,

        -- 🔹 Peso bruto total
        COALESCE(SUM(d.peso_bruto), 0) AS peso_bruto_total,

        -- 🔹 Jabas entregadas (para estados aprobados o finalizados)
        COALESCE(SUM(
            CASE WHEN r.estado IN ('aprobado', 'finalizado') 
                THEN d.cantidad_jabas ELSE 0 END
        ), 0) AS jabas_entregadas,

        -- 🔹 Peso neto total (peso_bruto - (jabas*2))
        COALESCE(SUM(
            CASE WHEN r.estado IN ('aprobado', 'finalizado') 
                THEN (d.peso_bruto - (d.cantidad_jabas * 2)) ELSE 0 END
        ), 0) AS peso_neto_total,

        -- 🔹 Total de jabas enviadas según la nota de salida
        COALESCE(mi.total_jabas, 0) AS jabas_enviadas,

        -- 🔹 Saldo pendiente = enviadas - recibidas
        COALESCE(mi.total_jabas, 0)
        - COALESCE(SUM(
            CASE WHEN r.estado IN ('aprobado', 'finalizado') 
                THEN d.cantidad_jabas ELSE 0 END
        ), 0) AS saldo_jabas,

        r.estado

    FROM recepcion_materia_prima r
    LEFT JOIN detalle_recepcion_materia_prima d ON r.id_recepcion = d.id_recepcion
    INNER JOIN agricultores a ON r.id_agricultor = a.id_agricultor

    -- 🔹 Jabas enviadas según nota de salida aprobada
    LEFT JOIN (
        SELECT 
            nm.id_nota, 
            SUM(mi.cantidad) AS total_jabas
        FROM nota_movimiento nm
        INNER JOIN movimientos_inventario mi ON nm.id_nota = mi.id_nota
        INNER JOIN insumos i ON mi.id_insumo = i.id_insumo
        WHERE nm.codigo_nota LIKE 'NS-%'
          AND nm.estado = 'aprobado'
          AND i.nombre_insumo LIKE '%jaba%'
        GROUP BY nm.id_nota
    ) mi ON r.id_nota_salida = mi.id_nota

    WHERE 1=1
        -- 🔍 Filtro búsqueda general (código, agricultor, observaciones)
        AND (
            p_q IS NULL OR p_q = '' OR
            LOWER(r.codigo_recepcion) LIKE CONCAT('%', LOWER(p_q), '%') OR
            LOWER(a.nombres) LIKE CONCAT('%', LOWER(p_q), '%') OR
            LOWER(a.apellidos) LIKE CONCAT('%', LOWER(p_q), '%')
        )
        -- 🎯 Filtro específico por agricultor
        AND (
            p_id_agricultor IS NULL OR p_id_agricultor = '' OR
            r.id_agricultor = p_id_agricultor
        )
        -- 📋 Filtro por estado
        AND (p_estado IS NULL OR p_estado = '' OR r.estado = p_estado)
        -- 🗓️ Filtro por rango de fechas
        AND (
            (p_fecha_inicio IS NULL AND p_fecha_fin IS NULL)
            OR (p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NOT NULL AND DATE(r.fecha_recepcion) BETWEEN p_fecha_inicio AND p_fecha_fin)
            OR (p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NULL AND DATE(r.fecha_recepcion) >= p_fecha_inicio)
            OR (p_fecha_fin IS NOT NULL AND p_fecha_inicio IS NULL AND DATE(r.fecha_recepcion) <= p_fecha_fin)
        )

    GROUP BY 
        r.id_recepcion, r.codigo_recepcion, a.nombres, a.apellidos,
        r.fecha_recepcion, mi.total_jabas, r.estado

    ORDER BY r.fecha_recepcion DESC, r.id_recepcion DESC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_listar_roles` ()   BEGIN
    SELECT id_rol, nombre_rol, descripcion, fecha_creacion
    FROM roles
    ORDER BY nombre_rol;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_listar_salidas_jabas` (IN `p_id_agricultor` INT)   BEGIN
    SELECT mi.id_movimiento, nm.codigo_nota, mi.cantidad, mi.unidad_medida,
           nm.fecha, nm.estado
    FROM movimientos_inventario mi
    INNER JOIN nota_movimiento nm ON mi.id_nota = nm.id_nota
    WHERE nm.id_agricultor = p_id_agricultor
      AND nm.id_tipo = (SELECT id_tipo FROM tipo_movimiento WHERE nombre='Salida')
      AND mi.id_insumo = (SELECT id_insumo FROM insumos WHERE nombre='Jaba') -- solo jabas
      AND mi.estado = 'activo';
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_listar_usuarios` (IN `p_q` VARCHAR(100), IN `p_id_rol` INT, IN `p_estado` VARCHAR(20), IN `p_fecha_inicio` DATE, IN `p_fecha_fin` DATE)   BEGIN
    SELECT 
        u.id_usuario, u.nombre_completo, u.dni, u.email, 
        u.telefono,
        r.nombre_rol AS nombre_rol,
        u.estado,
        u.ultimo_login,
        u.fecha_creacion
    FROM usuarios u
    LEFT JOIN roles r ON r.id_rol = u.id_rol
    WHERE 1=1
        AND (p_q IS NULL OR LOWER(u.nombre_completo) COLLATE utf8mb4_general_ci LIKE CONCAT('%', p_q, '%') COLLATE utf8mb4_general_ci
                        OR u.dni COLLATE utf8mb4_general_ci LIKE CONCAT('%', p_q, '%') COLLATE utf8mb4_general_ci
                        OR CAST(u.id_usuario AS CHAR) COLLATE utf8mb4_general_ci LIKE CONCAT('%', p_q, '%') COLLATE utf8mb4_general_ci)
        AND (p_id_rol IS NULL OR u.id_rol = p_id_rol)
        AND (p_estado IS NULL OR u.estado = p_estado)
        AND (
            (p_fecha_inicio IS NULL AND p_fecha_fin IS NULL)
            OR (p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NOT NULL AND DATE(u.fecha_creacion) BETWEEN p_fecha_inicio AND p_fecha_fin)
            OR (p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NULL AND DATE(u.fecha_creacion) >= p_fecha_inicio)
            OR (p_fecha_fin IS NOT NULL AND p_fecha_inicio IS NULL AND DATE(u.fecha_creacion) <= p_fecha_fin)
        )
    ORDER BY u.fecha_creacion DESC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_listar_variedades` ()   BEGIN
    SELECT 
        v.id_variedad, 
        v.codigo_variedad, 
        v.nombre_variedad, 
        v.id_categoria,         -- 👈 agregar esto
        c.nombre_categoria
    FROM variedades v
    INNER JOIN categorias c ON v.id_categoria = c.id_categoria;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_login_usuario` (IN `p_dni` CHAR(8), IN `p_contrasena` VARCHAR(255))   BEGIN
    DECLARE v_id INT;

    SELECT id_usuario INTO v_id
    FROM usuarios
    WHERE dni = p_dni
      AND contrasena = p_contrasena
      AND estado = 1
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE usuarios
        SET ultimo_login = NOW()
        WHERE id_usuario = v_id;

        SELECT * FROM usuarios WHERE id_usuario = v_id;
    ELSE
        SELECT NULL AS error, 'Credenciales inválidas o usuario inactivo' AS mensaje;
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_obtener_agricultor` (IN `p_id_agricultor` INT)   BEGIN
    SELECT 
        a.id_agricultor,
        a.codigo_agricultor,
        a.dni,
        a.nombres,
        a.apellidos,
        CONCAT(a.nombres, ' ', a.apellidos) AS nombre_completo,
        a.telefono,
        a.direccion,
        a.correo,
        a.zona,
        a.cultivo_principal,
        a.fecha_registro,
        a.estado
    FROM agricultores a
    WHERE a.id_agricultor = p_id_agricultor;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_obtener_detalles_por_nota` (IN `p_id_nota` INT)   BEGIN
    SELECT 
        d.id_movimiento,  
        d.id_insumo,
        i.nombre_insumo,
        d.cantidad,
        d.unidad_medida
    FROM movimientos_inventario d
    INNER JOIN insumos i ON d.id_insumo = i.id_insumo
    WHERE d.id_nota = p_id_nota;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_obtener_insumo` (IN `p_id` INT)   BEGIN
    SELECT * FROM insumos WHERE id_insumo = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_obtener_nota_por_id` (IN `p_id_nota` INT)   BEGIN
    SELECT 
        n.id_nota,
        n.id_tipo,
        n.id_origen,
        n.codigo_nota,
        n.fecha,
        n.referencia,
        n.observacion,
        n.estado,
        t.nombre AS tipo_movimiento,
        u.nombre_completo AS usuario,
        o.nombre AS origen_destino
    FROM nota_movimiento n
    INNER JOIN tipo_movimiento t ON n.id_tipo = t.id_tipo
    INNER JOIN usuarios u ON n.id_usuario = u.id_usuario
    LEFT JOIN origen_destino o ON n.id_origen = o.id_origen
    WHERE n.id_nota = p_id_nota;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_obtener_permisos_usuario` (IN `p_id_usuario` INT)   BEGIN
    SELECT 
        a.id_accion,
        a.codigo,
        a.nombre_accion,
        a.modulo,
        a.descripcion,
        COALESCE(p.permitido, 0) AS permitido
    FROM acciones a
    LEFT JOIN permisos p 
        ON a.id_accion = p.id_accion 
       AND p.id_usuario = p_id_usuario
    ORDER BY a.modulo, a.nombre_accion;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_obtener_recepcion_por_id` (IN `p_id_recepcion` INT)   BEGIN
    -- 📋 Cabecera
    SELECT 
        r.id_recepcion,
        r.codigo_recepcion,
        r.id_nota_salida,
        n.codigo_nota AS codigo_nota,
        r.id_agricultor,
        CONCAT(a.nombres, ' ', a.apellidos) AS agricultor,
        r.fecha_recepcion,
        r.hora_recepcion,
        r.observaciones,
        r.id_responsable,
        u.nombre_completo AS responsable,
        r.estado,
        r.fecha_registro
    FROM recepcion_materia_prima r
    INNER JOIN agricultores a ON a.id_agricultor = r.id_agricultor
    INNER JOIN usuarios u ON u.id_usuario = r.id_responsable
    INNER JOIN nota_movimiento n ON n.id_nota = r.id_nota_salida
    WHERE r.id_recepcion = p_id_recepcion;

    -- 📦 Detalles
    SELECT 
        d.id_detalle,
        d.id_variedad,
        v.nombre_variedad,
        d.lote,
        d.peso_bruto,
        d.cantidad_jabas,
        d.peso_neto,
        d.unidad_medida,
        d.estado
    FROM detalle_recepcion_materia_prima d
    INNER JOIN variedades v ON v.id_variedad = d.id_variedad
    WHERE d.id_recepcion = p_id_recepcion
      AND d.estado = 'activo';
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_obtener_usuario` (IN `p_id_usuario` INT)   BEGIN
    SELECT u.*, r.nombre_rol
    FROM usuarios u
    INNER JOIN roles r ON u.id_rol = r.id_rol
    WHERE u.id_usuario = p_id_usuario;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_registrar_devolucion_jabas` (IN `p_id_recepcion` INT, IN `p_id_agricultor` INT, IN `p_cantidad_devuelta` INT)   BEGIN
    DECLARE v_id_nota INT;
    DECLARE v_id_tipo INT;

    -- Obtener tipo de movimiento devolución
    SELECT id_tipo INTO v_id_tipo
    FROM tipo_movimiento
    WHERE nombre = 'Devolución'
    LIMIT 1;

    -- Crear nueva nota de movimiento de devolución
    CALL sp_crear_nota_movimiento(v_id_tipo, 'Devolución de jabas en recepción', 1, p_id_agricultor, 'Devolución vinculada a recepción');

    -- Obtener id_nota recién creada
    SET v_id_nota = LAST_INSERT_ID();

    -- Insertar detalle (solo jabas)
    INSERT INTO movimientos_inventario(id_nota, id_insumo, id_tipo, cantidad, unidad_medida, fecha_movimiento, estado)
    VALUES(v_id_nota, (SELECT id_insumo FROM insumos WHERE nombre='Jaba' LIMIT 1), v_id_tipo, p_cantidad_devuelta, 'unidad', NOW(), 'activo');

    -- Opcional: vincular recepción con nota de devolución (si agregamos un campo en recepcion_materia_prima)
    UPDATE recepcion_materia_prima
    SET observaciones = CONCAT(IFNULL(observaciones,''), '\nDevolvió ', p_cantidad_devuelta, ' jabas en recepción ', p_id_recepcion)
    WHERE id_recepcion = p_id_recepcion;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `acciones`
--

CREATE TABLE `acciones` (
  `id_accion` int(11) NOT NULL,
  `nombre_accion` varchar(100) NOT NULL,
  `modulo` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `codigo` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `acciones`
--

INSERT INTO `acciones` (`id_accion`, `nombre_accion`, `modulo`, `descripcion`, `codigo`) VALUES
(17, 'Ver lista de usuario', 'usuarios', 'Permite ver la lista de usuarios', 'usuarios.ver'),
(18, 'Nuevo usuario', 'usuarios', 'Permite registrar un nuevo usuario', 'usuarios.crear'),
(19, 'Editar usuario', 'usuarios', 'Permite editar los datos de un usuario', 'usuarios.editar'),
(20, 'Cambiar contraseña', 'usuarios', 'Permite cambiar la contraseña de un usuario', 'usuarios.cambiar_pass'),
(21, 'Ver permisos', 'permisos', 'Permite ver la lista de permisos', 'permisos.ver'),
(22, 'Asignar permisos', 'permisos', 'Permite asignar permisos a los usuarios', 'permisos.asignar'),
(23, 'Ver lista de insumos', 'insumos', 'Permite ver la lista de insumos', 'insumos.ver'),
(24, 'Nuevo insumo', 'insumos', 'Permite registrar un nuevo insumo', 'insumos.crear'),
(25, 'Nueva categoría', 'insumos', 'Permite registrar una nueva categoría de insumos', 'insumos.cat_crear'),
(26, 'Editar categoría', 'insumos', 'Permite editar una categoría de insumos', 'insumos.cat_editar'),
(27, 'Eliminar categoría', 'insumos', 'Permite eliminar una categoría de insumos', 'insumos.cat_eliminar'),
(28, 'Nueva variedad', 'insumos', 'Permite registrar una nueva variedad de insumos', 'insumos.var_crear'),
(29, 'Editar variedad', 'insumos', 'Permite editar una variedad de insumos', 'insumos.var_editar'),
(30, 'Eliminar variedad', 'insumos', 'Permite eliminar una variedad de insumos', 'insumos.var_eliminar'),
(31, 'Editar insumo', 'insumos', 'Permite editar los datos de un insumo', 'insumos.editar'),
(32, 'Desactivar insumo', 'insumos', 'Permite desactivar un insumo del sistema', 'insumos.desactivar'),
(33, 'Ver lista de movimientos', 'movimientos', 'Permite ver la lista de movimientos', 'movimientos.ver'),
(34, 'Nuevo movimiento', 'movimientos', 'Permite registrar un nuevo movimiento', 'movimientos.crear'),
(35, 'Editar movimiento', 'movimientos', 'Permite editar un movimiento registrado', 'movimientos.editar'),
(36, 'Ver kardex', 'movimientos', 'Permite consultar el kardex de un insumo', 'movimientos.kardex'),
(37, 'Ver stock bajo', 'stock', 'Permite ver el reporte de insumos con stock bajo', 'stock.ver'),
(38, 'Ver lista categorias', 'insumos', 'Permite ver la lista de categorias', 'categoria.ver'),
(39, 'Ver lista variedades', 'insumos', 'Permite ver la lista de variedades', 'variedad.ver'),
(40, 'Activar Insumo', 'insumos', 'Permite activar un insumo del sistema', 'insumos.activar'),
(41, 'Ver Lista De agricultores', 'agricultores', 'Permite ver la lista de agricultores', 'agricultores.ver'),
(42, 'Crear nuevo agricultor', 'agricultores', 'Permite registrar un nuevo agricultor', 'agricultores.crear'),
(43, 'Editar agricultores', 'agricultores', 'Permite editar los datos de un agricultor', 'agricultores.editar'),
(44, 'Cambir estado agricultores', 'agricultores', 'Permite cambiar el estado de un agricultor', 'agricultores.estado'),
(45, 'Ver lista de recepcion', 'recepcion', 'Permite ver la lista de recepcion', 'recepcion.ver'),
(46, 'Crea nueva recepcion', 'recepcion', 'Permite registrar una nueva recepcion', 'recepcion.crear'),
(47, 'Edita la recepcion', 'recepcion', 'Permite editar los datos de resepcion', 'recepcion.editar'),
(48, 'Anula recepcion', 'recepcion', 'Permite cambiar el estado de una recepcionista', 'recepcion.anular');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `agricultores`
--

CREATE TABLE `agricultores` (
  `id_agricultor` int(11) NOT NULL,
  `codigo_agricultor` varchar(5) NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) DEFAULT NULL,
  `dni` varchar(8) NOT NULL,
  `telefono` varchar(9) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `zona` varchar(100) DEFAULT NULL,
  `fecha_registro` date DEFAULT curdate(),
  `cultivo_principal` varchar(100) DEFAULT NULL,
  `estado` tinyint(1) DEFAULT 1,
  `direccion` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `agricultores`
--

INSERT INTO `agricultores` (`id_agricultor`, `codigo_agricultor`, `nombres`, `apellidos`, `dni`, `telefono`, `correo`, `zona`, `fecha_registro`, `cultivo_principal`, `estado`, `direccion`) VALUES
(1, 'AG001', 'Juan Carlos', 'Mendez Pajuelo', '12345678', '987654321', 'prueba@gmail.com', 'huandoy', '2025-09-05', 'Holantao', 1, 'Av. Central 789 sn'),
(2, 'AG002', 'Pedro Raul', 'Gonzáles Moreno', '12345678', '999963336', 'prueba2@gmail.com', 'Huandoy', '2025-10-14', 'Holantao', 1, 'Av. Central 789 sn');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alertas`
--

CREATE TABLE `alertas` (
  `id_alerta` int(11) NOT NULL,
  `id_insumo` int(11) NOT NULL,
  `mensaje` varchar(255) NOT NULL,
  `fecha_alerta` datetime DEFAULT current_timestamp(),
  `visto` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alertas`
--

INSERT INTO `alertas` (`id_alerta`, `id_insumo`, `mensaje`, `fecha_alerta`, `visto`) VALUES
(1, 2, '⚠️ El stock del insumo Semilla Suprema quedó en 0 (mínimo: 5.00).', '2025-09-18 15:10:31', 0),
(2, 4, '⚠️ El stock del insumo Rafia plana quedó en 0 (mínimo: 5.00).', '2025-09-18 15:10:31', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `codigo_categoria` varchar(5) NOT NULL,
  `nombre_categoria` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `codigo_categoria`, `nombre_categoria`) VALUES
(1, 'SEM01', 'Semilla'),
(2, 'RAF01', 'Rafia'),
(3, 'JAB01', 'JABAS'),
(5, 'VEN01', 'Venemos'),
(15, 'RE001', 'Otros'),
(16, 'MP', 'Materia prima');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `control_jabas_agricultor`
--

CREATE TABLE `control_jabas_agricultor` (
  `id_control` int(11) NOT NULL,
  `id_agricultor` int(11) NOT NULL,
  `id_nota` int(11) DEFAULT NULL,
  `id_recepcion` int(11) DEFAULT NULL,
  `tipo_movimiento` enum('entrega','devolucion') NOT NULL,
  `cantidad_jabas` int(11) NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `estado` enum('activo','anulado') DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `control_jabas_agricultor`
--

INSERT INTO `control_jabas_agricultor` (`id_control`, `id_agricultor`, `id_nota`, `id_recepcion`, `tipo_movimiento`, `cantidad_jabas`, `fecha`, `estado`) VALUES
(5, 1, 6, 2, 'devolucion', 2, '2025-10-22 21:26:42', 'activo'),
(6, 1, 8, NULL, 'entrega', 100, '2025-10-23 11:11:14', 'activo'),
(7, 1, 8, NULL, 'entrega', 100, '2025-10-23 11:11:14', 'activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_recepcion_materia_prima`
--

CREATE TABLE `detalle_recepcion_materia_prima` (
  `id_detalle` int(11) NOT NULL,
  `id_recepcion` int(11) NOT NULL,
  `id_variedad` int(11) NOT NULL,
  `lote` varchar(50) DEFAULT NULL,
  `peso_bruto` decimal(10,2) DEFAULT 0.00,
  `cantidad_jabas` int(11) DEFAULT 0,
  `peso_neto` decimal(10,2) GENERATED ALWAYS AS (`peso_bruto` - `cantidad_jabas` * 2) STORED,
  `unidad_medida` varchar(20) DEFAULT 'kg',
  `estado` enum('activo','anulado') DEFAULT 'activo',
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_recepcion_materia_prima`
--

INSERT INTO `detalle_recepcion_materia_prima` (`id_detalle`, `id_recepcion`, `id_variedad`, `lote`, `peso_bruto`, `cantidad_jabas`, `unidad_medida`, `estado`, `fecha_registro`) VALUES
(7, 1, 9, 'L02', 150.60, 10, 'kg', 'activo', '2025-10-22 14:26:47'),
(9, 2, 9, 'L03', 30.50, 2, 'kg', 'activo', '2025-10-22 21:00:27');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `insumos`
--

CREATE TABLE `insumos` (
  `id_insumo` int(11) NOT NULL,
  `codigo_insumo` varchar(5) NOT NULL,
  `nombre_insumo` varchar(100) DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `id_variedad` int(11) DEFAULT NULL,
  `stock_actual` int(11) DEFAULT 0,
  `stock_minimo` decimal(10,2) NOT NULL DEFAULT 5.00,
  `unidad_medida` varchar(20) DEFAULT NULL,
  `fecha_ingreso` date NOT NULL DEFAULT current_timestamp(),
  `fecha_vencimiento` date DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `insumos`
--

INSERT INTO `insumos` (`id_insumo`, `codigo_insumo`, `nombre_insumo`, `id_categoria`, `id_variedad`, `stock_actual`, `stock_minimo`, `unidad_medida`, `fecha_ingreso`, `fecha_vencimiento`, `descripcion`, `estado`) VALUES
(1, 'JAB02', 'Jaba de color rojo', 3, NULL, 43, 5.00, 'und', '2025-08-28', NULL, 'Jaba para recolectar materiales primas', 1),
(2, 'Sem02', 'Semilla Suprema', 1, 1, 5, 5.00, 'KL', '2025-08-28', NULL, 'Semilla para la siemba', 1),
(3, 'SEMSL', 'Semilla SL', 1, 3, 10, 5.00, 'KL', '2025-08-29', NULL, 'semilla de shugar sl', 1),
(4, 'RAFPA', 'Rafia plana', 2, 2, 0, 5.00, 'und', '2025-08-29', NULL, 'Rafia para guiar o tener ', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `log_actividad`
--

CREATE TABLE `log_actividad` (
  `id_log` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `accion` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos_inventario`
--

CREATE TABLE `movimientos_inventario` (
  `id_movimiento` int(11) NOT NULL,
  `id_nota` int(11) NOT NULL,
  `id_insumo` int(11) NOT NULL,
  `id_tipo` int(11) NOT NULL,
  `cantidad` decimal(10,2) DEFAULT NULL,
  `unidad_medida` varchar(20) DEFAULT NULL,
  `fecha_movimiento` datetime DEFAULT current_timestamp(),
  `estado` enum('activo','anulado') DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `movimientos_inventario`
--

INSERT INTO `movimientos_inventario` (`id_movimiento`, `id_nota`, `id_insumo`, `id_tipo`, `cantidad`, `unidad_medida`, `fecha_movimiento`, `estado`) VALUES
(4, 1, 1, 1, 100.00, 'und', '2025-09-16 14:13:28', 'activo'),
(5, 2, 1, 2, 10.00, 'und', '2025-09-16 14:13:54', 'activo'),
(6, 3, 1, 1, 50.00, 'und', '2025-09-18 14:26:38', 'activo'),
(7, 4, 3, 1, 10.00, 'kg', '2025-09-18 14:32:10', 'activo'),
(9, 5, 1, 2, 30.00, 'und', '2025-09-18 14:57:58', 'activo'),
(10, 5, 1, 2, 20.00, 'und', '2025-09-18 14:57:58', 'activo'),
(11, 6, 1, 2, 50.00, 'und', '2025-09-18 15:12:05', 'activo'),
(12, 7, 1, 2, 10.00, 'und', '2025-10-02 13:45:11', 'activo'),
(20, 8, 1, 2, 100.00, 'und', '2025-10-23 11:10:23', 'activo'),
(22, 9, 2, 1, 100.00, 'kg', '2025-10-27 14:52:58', 'activo');

--
-- Disparadores `movimientos_inventario`
--
DELIMITER $$
CREATE TRIGGER `trg_movimiento_delete` BEFORE DELETE ON `movimientos_inventario` FOR EACH ROW BEGIN
    DECLARE v_estado VARCHAR(20);

    SELECT estado INTO v_estado FROM nota_movimiento WHERE id_nota = OLD.id_nota;

    -- Si la nota estaba aprobada, revertimos el efecto del movimiento eliminado
    IF v_estado = 'aprobado' THEN
        IF OLD.id_tipo IN (1,3,5) THEN
            UPDATE insumos SET stock_actual = stock_actual - OLD.cantidad WHERE id_insumo = OLD.id_insumo;
        ELSEIF OLD.id_tipo IN (2,4) THEN
            UPDATE insumos SET stock_actual = stock_actual + OLD.cantidad WHERE id_insumo = OLD.id_insumo;
        END IF;
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_movimiento_insert` BEFORE INSERT ON `movimientos_inventario` FOR EACH ROW BEGIN
    DECLARE v_estado VARCHAR(20);
    DECLARE v_stock_actual INT;
    DECLARE v_stock_minimo INT;

    SELECT estado INTO v_estado FROM nota_movimiento WHERE id_nota = NEW.id_nota;

    -- Si la nota ya está aprobada, aplicamos el movimiento inmediatamente
    IF v_estado = 'aprobado' THEN
        SELECT stock_actual, stock_minimo INTO v_stock_actual, v_stock_minimo
        FROM insumos WHERE id_insumo = NEW.id_insumo;

        IF NEW.id_tipo IN (1,3,5) THEN
            UPDATE insumos SET stock_actual = stock_actual + NEW.cantidad WHERE id_insumo = NEW.id_insumo;
        ELSEIF NEW.id_tipo IN (2,4) THEN
            IF v_stock_actual - NEW.cantidad < 0 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '❌ Stock insuficiente. No se permite stock negativo.';
            ELSE
                UPDATE insumos SET stock_actual = stock_actual - NEW.cantidad WHERE id_insumo = NEW.id_insumo;

                IF (v_stock_actual - NEW.cantidad) < v_stock_minimo THEN
                    INSERT INTO alertas (id_insumo, mensaje, fecha_alerta, visto)
                    VALUES (NEW.id_insumo,
                            CONCAT('⚠️ El stock del insumo bajó a ', v_stock_actual - NEW.cantidad, ' (mínimo: ', v_stock_minimo, ').'),
                            NOW(), 0);
                END IF;
            END IF;
        END IF;
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_movimiento_update` BEFORE UPDATE ON `movimientos_inventario` FOR EACH ROW BEGIN
    DECLARE v_estado_old VARCHAR(20);
    DECLARE v_estado_new VARCHAR(20);
    DECLARE v_stock_actual INT;
    DECLARE v_stock_minimo INT;

    SELECT estado INTO v_estado_old FROM nota_movimiento WHERE id_nota = OLD.id_nota;
    SELECT estado INTO v_estado_new FROM nota_movimiento WHERE id_nota = NEW.id_nota;

    -- Si la nota estaba aprobada, revertimos el efecto del OLD
    IF v_estado_old = 'aprobado' THEN
        IF OLD.id_tipo IN (1,3,5) THEN
            UPDATE insumos SET stock_actual = stock_actual - OLD.cantidad WHERE id_insumo = OLD.id_insumo;
        ELSEIF OLD.id_tipo IN (2,4) THEN
            UPDATE insumos SET stock_actual = stock_actual + OLD.cantidad WHERE id_insumo = OLD.id_insumo;
        END IF;
    END IF;

    -- Si la nota está aprobada ahora (NEW), aplicamos el NEW
    IF v_estado_new = 'aprobado' THEN
        SELECT stock_actual, stock_minimo INTO v_stock_actual, v_stock_minimo
        FROM insumos WHERE id_insumo = NEW.id_insumo;

        IF NEW.id_tipo IN (1,3,5) THEN
            UPDATE insumos SET stock_actual = stock_actual + NEW.cantidad WHERE id_insumo = NEW.id_insumo;
        ELSEIF NEW.id_tipo IN (2,4) THEN
            IF v_stock_actual - NEW.cantidad < 0 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '❌ Stock insuficiente en actualización.';
            ELSE
                UPDATE insumos SET stock_actual = stock_actual - NEW.cantidad WHERE id_insumo = NEW.id_insumo;
                IF (v_stock_actual - NEW.cantidad) < v_stock_minimo THEN
                    INSERT INTO alertas (id_insumo, mensaje, fecha_alerta, visto)
                    VALUES (NEW.id_insumo,
                            CONCAT('⚠️ El stock del insumo bajó a ', v_stock_actual - NEW.cantidad, ' (mínimo: ', v_stock_minimo, ').'),
                            NOW(), 0);
                END IF;
            END IF;
        END IF;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `nota_movimiento`
--

CREATE TABLE `nota_movimiento` (
  `id_nota` int(11) NOT NULL,
  `codigo_nota` varchar(10) NOT NULL,
  `id_tipo` int(11) NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `referencia` varchar(100) DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `observacion` varchar(150) NOT NULL,
  `estado` enum('pendiente','aprobado','anulado') DEFAULT 'pendiente',
  `id_origen` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `nota_movimiento`
--

INSERT INTO `nota_movimiento` (`id_nota`, `codigo_nota`, `id_tipo`, `fecha`, `referencia`, `id_usuario`, `observacion`, `estado`, `id_origen`) VALUES
(1, 'NE-00001', 1, '2025-09-16 14:13:28', NULL, 3, 'Entrada de jabas al almacen principal ', 'aprobado', 2),
(2, 'NS-00001', 2, '2025-09-16 14:13:53', NULL, 3, 'Salida de jabas para el agricultor', 'anulado', 1),
(3, 'NE-00002', 1, '2025-09-18 14:26:38', NULL, 3, 'Entrada de jabas al almacen principal ', 'aprobado', 2),
(4, 'NE-00003', 1, '2025-09-18 14:32:10', NULL, 3, 'Entrada de semilla', 'aprobado', 2),
(5, 'NS-00002', 2, '2025-09-18 00:00:00', NULL, 3, 'Salida de jabas para el agricultor', 'anulado', 1),
(6, 'NS-00003', 2, '2025-09-18 15:12:05', NULL, 3, 'Salida de jabas para el agricultor', 'aprobado', 1),
(7, 'NS-00004', 2, '2025-10-02 13:45:11', NULL, 3, 'Salida de jabas para el agricultor', 'aprobado', 1),
(8, 'NS-00005', 2, '2025-10-22 00:00:00', NULL, 3, 'Salida de jabas ', 'pendiente', 1),
(9, 'NE-00004', 1, '2025-10-27 00:00:00', 'F0001', 3, 'semilla Suprema', 'pendiente', 2);

--
-- Disparadores `nota_movimiento`
--
DELIMITER $$
CREATE TRIGGER `tr_entrega_jabas` AFTER UPDATE ON `nota_movimiento` FOR EACH ROW BEGIN
    -- Solo actúa si la nota cambia de pendiente a aprobado
    IF OLD.estado = 'pendiente' AND NEW.estado = 'aprobado' THEN

        -- Registrar entrega en control_jabas_agricultor directamente
        INSERT INTO control_jabas_agricultor (id_agricultor, id_nota, tipo_movimiento, cantidad_jabas, fecha, estado)
        SELECT 
            o.id_origen AS id_agricultor,
            NEW.id_nota,
            'entrega',
            IFNULL(SUM(mi.cantidad), 0) AS cantidad_jabas,
            NOW(),
            'activo'
        FROM origen_destino o
        JOIN nota_movimiento n ON n.id_origen = o.id_origen
        JOIN movimientos_inventario mi ON mi.id_nota = n.id_nota
        WHERE n.id_nota = NEW.id_nota
          AND o.tipo = 'agricultor'
          AND mi.estado = 'activo'
        GROUP BY o.id_origen;

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `tr_nota_movimiento_aprobado` AFTER UPDATE ON `nota_movimiento` FOR EACH ROW BEGIN
    -- Solo ejecutar si pasa a aprobado y es una nota de salida
    IF NEW.estado = 'aprobado' AND LEFT(NEW.codigo_nota, 3) = 'NS-' THEN
        INSERT INTO control_jabas_agricultor (
            id_agricultor,
            id_nota,
            id_recepcion,
            tipo_movimiento,
            cantidad_jabas,
            fecha,
            estado
        )
        SELECT 
            NEW.id_origen,
            NEW.id_nota,
            NULL,
            'entrega',
            COALESCE(SUM(mi.cantidad), 0),
            NOW(),
            'activo'
        FROM movimientos_inventario mi
        INNER JOIN insumos i ON mi.id_insumo = i.id_insumo
        WHERE mi.id_nota = NEW.id_nota
          AND i.nombre_insumo LIKE '%jaba%';
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `origen_destino`
--

CREATE TABLE `origen_destino` (
  `id_origen` int(11) NOT NULL,
  `tipo` enum('agricultor','almacen') NOT NULL,
  `codigo` varchar(20) DEFAULT NULL,
  `dni` varchar(15) DEFAULT NULL,
  `nombre` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `origen_destino`
--

INSERT INTO `origen_destino` (`id_origen`, `tipo`, `codigo`, `dni`, `nombre`) VALUES
(1, 'agricultor', 'AG001', '12345678', 'Juan Carlos Mendez Pajuelo'),
(2, 'almacen', 'ALM-001', NULL, 'Almacén Principal'),
(3, 'almacen', 'ALM-002', NULL, 'Almacén Secundario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id_permiso` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `permitido` tinyint(1) NOT NULL DEFAULT 0,
  `id_accion` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`id_permiso`, `id_usuario`, `permitido`, `id_accion`) VALUES
(135, 2, 1, 42),
(136, 2, 1, 41),
(137, 2, 1, 38),
(138, 2, 1, 24),
(139, 2, 1, 23),
(140, 2, 1, 33),
(141, 2, 1, 45),
(142, 2, 1, 37),
(143, 2, 1, 17),
(144, 2, 1, 39);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recepcion_materia_prima`
--

CREATE TABLE `recepcion_materia_prima` (
  `id_recepcion` int(11) NOT NULL,
  `codigo_recepcion` varchar(10) NOT NULL,
  `id_agricultor` int(11) NOT NULL,
  `id_nota_salida` int(11) DEFAULT NULL,
  `fecha_recepcion` date NOT NULL,
  `hora_recepcion` time NOT NULL,
  `observaciones` text DEFAULT NULL,
  `id_responsable` int(11) NOT NULL,
  `estado` enum('pendiente','aprobado','anulado') DEFAULT 'pendiente',
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `recepcion_materia_prima`
--

INSERT INTO `recepcion_materia_prima` (`id_recepcion`, `codigo_recepcion`, `id_agricultor`, `id_nota_salida`, `fecha_recepcion`, `hora_recepcion`, `observaciones`, `id_responsable`, `estado`, `fecha_registro`) VALUES
(1, 'NR-00001', 1, 7, '2025-10-21', '18:39:13', 'entrega de SL', 3, 'pendiente', '2025-10-21 18:39:13'),
(2, 'NR-00002', 1, 6, '2025-10-22', '21:00:27', NULL, 3, 'aprobado', '2025-10-22 21:00:27');

--
-- Disparadores `recepcion_materia_prima`
--
DELIMITER $$
CREATE TRIGGER `tr_actualizar_saldo_jabas_despues_aprobar` AFTER UPDATE ON `recepcion_materia_prima` FOR EACH ROW BEGIN
    -- Solo actuar si el estado cambia
    IF OLD.estado <> NEW.estado THEN

        -- ✅ Si pasa a aprobado: marcar las entregas como vinculadas
        IF NEW.estado = 'aprobado' THEN
            UPDATE control_jabas_agricultor
            SET estado = 'vinculado'
            WHERE tipo_movimiento = 'entrega'
              AND id_agricultor = NEW.id_agricultor
              AND id_nota = NEW.id_nota_salida
              AND estado = 'activo';

        -- ???? Si pasa a anulado: revertir
        ELSEIF NEW.estado = 'anulado' THEN
            UPDATE control_jabas_agricultor
            SET estado = 'activo'
            WHERE tipo_movimiento = 'entrega'
              AND id_agricultor = NEW.id_agricultor
              AND id_nota = NEW.id_nota_salida
              AND estado = 'vinculado';
        END IF;

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `tr_devolucion_jabas` AFTER UPDATE ON `recepcion_materia_prima` FOR EACH ROW BEGIN
    -- Solo si cambia de pendiente → aprobado
    IF OLD.estado = 'pendiente' AND NEW.estado = 'aprobado' THEN

        INSERT INTO control_jabas_agricultor (
            id_agricultor,
            id_nota,
            id_recepcion,
            tipo_movimiento,
            cantidad_jabas,
            fecha,
            estado
        )
        SELECT 
            NEW.id_agricultor,
            NEW.id_nota_salida,   -- ✅ usa la columna correcta de recepcion
            NEW.id_recepcion,
            'devolucion',
            IFNULL(SUM(drm.cantidad_jabas), 0),
            NOW(),
            'activo'
        FROM detalle_recepcion_materia_prima drm
        WHERE drm.id_recepcion = NEW.id_recepcion
          AND drm.estado = 'activo'
        GROUP BY drm.id_recepcion;

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `nombre_rol` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `nombre_rol`, `descripcion`, `fecha_creacion`) VALUES
(1, 'Administrador', 'Acceso total al sistema', '2025-09-01 17:23:31'),
(2, 'Usuario', 'Acceso limitado a funciones', '2025-09-01 17:23:31'),
(3, 'Invitado', 'Acceso de solo lectura', '2025-09-01 17:23:31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_movimiento`
--

CREATE TABLE `tipo_movimiento` (
  `id_tipo` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_movimiento`
--

INSERT INTO `tipo_movimiento` (`id_tipo`, `nombre`) VALUES
(3, 'Ajuste'),
(4, 'Baja'),
(5, 'Devolución'),
(1, 'Entrada'),
(2, 'Salida');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre_completo` varchar(100) DEFAULT NULL,
  `dni` char(8) NOT NULL,
  `contrasena` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefono` char(9) DEFAULT NULL,
  `id_rol` int(11) DEFAULT NULL,
  `estado` tinyint(1) DEFAULT 1,
  `ultimo_login` datetime DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre_completo`, `dni`, `contrasena`, `email`, `telefono`, `id_rol`, `estado`, `ultimo_login`, `fecha_creacion`) VALUES
(1, 'Admin', '12345678', 'scrypt:32768:8:1$VFkyWjNsCqzDpBSf$70e7e0bcbc144eb0bed90a28126bd20505e0d29a6a0436a491eca98694331d53e2f4fbba90b98ba3b4a3ff18845541624b0b33b3ef86cbde119f4b045d8b4812', 'admin@miapp.com', '987654300', 1, 1, NULL, '2025-09-02 14:20:34'),
(2, 'Usuairo de Prueba', '87654321', 'scrypt:32768:8:1$996VJnQh79W3dOml$f7e8aeb7facb639a6d9a5c713a5f61ffe3ed34875e9c361c283ffc10f352bde7ba0be291fc2acae80512398d98c7b46d612771694bb4f4bcbf614e018a66ce3a', 'Usuario01@gmail.com', '987654321', 2, 1, NULL, '2025-09-02 14:46:16'),
(3, 'Admin 22', '10101010', 'scrypt:32768:8:1$WbYokxvxLJMVYx47$5d91536636553150d44425d2c8c16e713f7efc3a7e0e79602aaebabddac7f0953683d7626e6a36c123cb4327e68c325abce39cd0cd9cc4eba9bdb35c15ebfe0e', 'admin2@miapp.com', '987654351', 1, 1, '2025-11-26 17:05:08', '2025-09-03 15:49:02');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `variedades`
--

CREATE TABLE `variedades` (
  `id_variedad` int(11) NOT NULL,
  `codigo_variedad` varchar(5) NOT NULL,
  `nombre_variedad` varchar(100) DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `variedades`
--

INSERT INTO `variedades` (`id_variedad`, `codigo_variedad`, `nombre_variedad`, `id_categoria`) VALUES
(1, 'SUP01', 'Semilla Suprema', 1),
(2, 'PLA01', 'Rafia plana', 2),
(3, 'SL001', 'Semilla SL', 1),
(4, 'VEN02', 'Absolute', 5),
(8, 'MP0SL', 'SL', 16),
(9, 'MP0SP', 'Suprema', 16);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vw_entregables_agricultor`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vw_entregables_agricultor` (
`id_agricultor` int(11)
,`variedad` varchar(100)
,`jabas_entregadas` decimal(56,2)
,`jabas_devueltas` decimal(56,2)
,`saldo_jabas` decimal(57,2)
,`total_kilos_bruto` decimal(54,2)
,`total_kilos_neto` decimal(54,2)
,`ultima_fecha` datetime
,`estado` varchar(8)
);

-- --------------------------------------------------------

--
-- Estructura para la vista `vw_entregables_agricultor`
--
DROP TABLE IF EXISTS `vw_entregables_agricultor`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_entregables_agricultor`  AS SELECT `t`.`id_agricultor` AS `id_agricultor`, coalesce(`v`.`nombre_variedad`,'Sin definir') AS `variedad`, ifnull(sum(case when `t`.`tipo` = 'entrega' then `t`.`jabas` else 0 end),0) AS `jabas_entregadas`, ifnull(sum(case when `t`.`tipo` = 'devolucion' then `t`.`jabas` else 0 end),0) AS `jabas_devueltas`, ifnull(sum(case when `t`.`tipo` = 'entrega' then `t`.`jabas` else 0 end),0) - ifnull(sum(case when `t`.`tipo` = 'devolucion' then `t`.`jabas` else 0 end),0) AS `saldo_jabas`, ifnull(sum(`t`.`kilos_bruto`),0) AS `total_kilos_bruto`, ifnull(sum(`t`.`kilos_neto`),0) AS `total_kilos_neto`, max(`t`.`fecha`) AS `ultima_fecha`, CASE WHEN ifnull(sum(case when `t`.`tipo` = 'entrega' then `t`.`jabas` else 0 end),0) - ifnull(sum(case when `t`.`tipo` = 'devolucion' then `t`.`jabas` else 0 end),0) > 0 THEN 'Activo' ELSE 'Inactivo' END AS `estado` FROM ((select `o`.`id_origen` AS `id_agricultor`,NULL AS `id_variedad`,'entrega' AS `tipo`,ifnull(sum(`mi`.`cantidad`),0) AS `jabas`,0 AS `kilos_bruto`,0 AS `kilos_neto`,`nm`.`fecha` AS `fecha` from ((`nota_movimiento` `nm` join `origen_destino` `o` on(`o`.`id_origen` = `nm`.`id_origen` and `o`.`tipo` = 'agricultor')) join `movimientos_inventario` `mi` on(`mi`.`id_nota` = `nm`.`id_nota`)) where `nm`.`estado` <> 'anulado' group by `o`.`id_origen`,`nm`.`fecha` union all select `rmp`.`id_agricultor` AS `id_agricultor`,`drp`.`id_variedad` AS `id_variedad`,'devolucion' AS `tipo`,ifnull(sum(`drp`.`cantidad_jabas`),0) AS `jabas`,ifnull(sum(`drp`.`peso_bruto`),0) AS `kilos_bruto`,ifnull(sum(`drp`.`peso_neto`),0) AS `kilos_neto`,`rmp`.`fecha_recepcion` AS `fecha` from (`recepcion_materia_prima` `rmp` join `detalle_recepcion_materia_prima` `drp` on(`drp`.`id_recepcion` = `rmp`.`id_recepcion`)) where `rmp`.`estado` <> 'anulado' group by `rmp`.`id_agricultor`,`drp`.`id_variedad`,`rmp`.`fecha_recepcion`) `t` left join `variedades` `v` on(`v`.`id_variedad` = `t`.`id_variedad`)) GROUP BY `t`.`id_agricultor`, coalesce(`v`.`nombre_variedad`,'Sin definir') ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `acciones`
--
ALTER TABLE `acciones`
  ADD PRIMARY KEY (`id_accion`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `agricultores`
--
ALTER TABLE `agricultores`
  ADD PRIMARY KEY (`id_agricultor`),
  ADD UNIQUE KEY `codigo_agricultor` (`codigo_agricultor`),
  ADD UNIQUE KEY `codigo_agricultor_2` (`codigo_agricultor`);

--
-- Indices de la tabla `alertas`
--
ALTER TABLE `alertas`
  ADD PRIMARY KEY (`id_alerta`),
  ADD KEY `id_insumo` (`id_insumo`);

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`),
  ADD UNIQUE KEY `codigo_categoria` (`codigo_categoria`);

--
-- Indices de la tabla `control_jabas_agricultor`
--
ALTER TABLE `control_jabas_agricultor`
  ADD PRIMARY KEY (`id_control`),
  ADD KEY `id_agricultor` (`id_agricultor`),
  ADD KEY `id_nota` (`id_nota`),
  ADD KEY `id_recepcion` (`id_recepcion`);

--
-- Indices de la tabla `detalle_recepcion_materia_prima`
--
ALTER TABLE `detalle_recepcion_materia_prima`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `fk_det_recep_recep` (`id_recepcion`),
  ADD KEY `fk_det_recep_variedad` (`id_variedad`);

--
-- Indices de la tabla `insumos`
--
ALTER TABLE `insumos`
  ADD PRIMARY KEY (`id_insumo`),
  ADD UNIQUE KEY `codigo_insumo` (`codigo_insumo`),
  ADD KEY `id_categoria` (`id_categoria`),
  ADD KEY `id_variedad` (`id_variedad`);

--
-- Indices de la tabla `log_actividad`
--
ALTER TABLE `log_actividad`
  ADD PRIMARY KEY (`id_log`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `movimientos_inventario`
--
ALTER TABLE `movimientos_inventario`
  ADD PRIMARY KEY (`id_movimiento`),
  ADD KEY `id_nota` (`id_nota`),
  ADD KEY `id_insumo` (`id_insumo`),
  ADD KEY `id_tipo` (`id_tipo`);

--
-- Indices de la tabla `nota_movimiento`
--
ALTER TABLE `nota_movimiento`
  ADD PRIMARY KEY (`id_nota`),
  ADD UNIQUE KEY `codigo_nota` (`codigo_nota`),
  ADD KEY `id_tipo` (`id_tipo`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_origen` (`id_origen`);

--
-- Indices de la tabla `origen_destino`
--
ALTER TABLE `origen_destino`
  ADD PRIMARY KEY (`id_origen`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id_permiso`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_permisos_acciones` (`id_accion`);

--
-- Indices de la tabla `recepcion_materia_prima`
--
ALTER TABLE `recepcion_materia_prima`
  ADD PRIMARY KEY (`id_recepcion`),
  ADD KEY `fk_recep_nota_salida` (`id_nota_salida`),
  ADD KEY `fk_recep_agricultor` (`id_agricultor`),
  ADD KEY `fk_recep_responsable` (`id_responsable`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`),
  ADD UNIQUE KEY `nombre_rol` (`nombre_rol`);

--
-- Indices de la tabla `tipo_movimiento`
--
ALTER TABLE `tipo_movimiento`
  ADD PRIMARY KEY (`id_tipo`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `dni` (`dni`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `email_2` (`email`),
  ADD KEY `id_rol` (`id_rol`);

--
-- Indices de la tabla `variedades`
--
ALTER TABLE `variedades`
  ADD PRIMARY KEY (`id_variedad`),
  ADD UNIQUE KEY `codigo_variedad` (`codigo_variedad`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `acciones`
--
ALTER TABLE `acciones`
  MODIFY `id_accion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT de la tabla `agricultores`
--
ALTER TABLE `agricultores`
  MODIFY `id_agricultor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `alertas`
--
ALTER TABLE `alertas`
  MODIFY `id_alerta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `control_jabas_agricultor`
--
ALTER TABLE `control_jabas_agricultor`
  MODIFY `id_control` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `detalle_recepcion_materia_prima`
--
ALTER TABLE `detalle_recepcion_materia_prima`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `insumos`
--
ALTER TABLE `insumos`
  MODIFY `id_insumo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `log_actividad`
--
ALTER TABLE `log_actividad`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `movimientos_inventario`
--
ALTER TABLE `movimientos_inventario`
  MODIFY `id_movimiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `nota_movimiento`
--
ALTER TABLE `nota_movimiento`
  MODIFY `id_nota` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `origen_destino`
--
ALTER TABLE `origen_destino`
  MODIFY `id_origen` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id_permiso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=145;

--
-- AUTO_INCREMENT de la tabla `recepcion_materia_prima`
--
ALTER TABLE `recepcion_materia_prima`
  MODIFY `id_recepcion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `tipo_movimiento`
--
ALTER TABLE `tipo_movimiento`
  MODIFY `id_tipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `variedades`
--
ALTER TABLE `variedades`
  MODIFY `id_variedad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alertas`
--
ALTER TABLE `alertas`
  ADD CONSTRAINT `alertas_ibfk_1` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`);

--
-- Filtros para la tabla `control_jabas_agricultor`
--
ALTER TABLE `control_jabas_agricultor`
  ADD CONSTRAINT `control_jabas_agricultor_ibfk_1` FOREIGN KEY (`id_agricultor`) REFERENCES `agricultores` (`id_agricultor`),
  ADD CONSTRAINT `control_jabas_agricultor_ibfk_2` FOREIGN KEY (`id_nota`) REFERENCES `nota_movimiento` (`id_nota`),
  ADD CONSTRAINT `control_jabas_agricultor_ibfk_3` FOREIGN KEY (`id_recepcion`) REFERENCES `recepcion_materia_prima` (`id_recepcion`);

--
-- Filtros para la tabla `detalle_recepcion_materia_prima`
--
ALTER TABLE `detalle_recepcion_materia_prima`
  ADD CONSTRAINT `fk_det_recep_recep` FOREIGN KEY (`id_recepcion`) REFERENCES `recepcion_materia_prima` (`id_recepcion`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_det_recep_variedad` FOREIGN KEY (`id_variedad`) REFERENCES `variedades` (`id_variedad`);

--
-- Filtros para la tabla `insumos`
--
ALTER TABLE `insumos`
  ADD CONSTRAINT `insumos_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`),
  ADD CONSTRAINT `insumos_ibfk_2` FOREIGN KEY (`id_variedad`) REFERENCES `variedades` (`id_variedad`);

--
-- Filtros para la tabla `log_actividad`
--
ALTER TABLE `log_actividad`
  ADD CONSTRAINT `log_actividad_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `movimientos_inventario`
--
ALTER TABLE `movimientos_inventario`
  ADD CONSTRAINT `movimientos_inventario_ibfk_1` FOREIGN KEY (`id_nota`) REFERENCES `nota_movimiento` (`id_nota`),
  ADD CONSTRAINT `movimientos_inventario_ibfk_2` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`),
  ADD CONSTRAINT `movimientos_inventario_ibfk_3` FOREIGN KEY (`id_tipo`) REFERENCES `tipo_movimiento` (`id_tipo`);

--
-- Filtros para la tabla `nota_movimiento`
--
ALTER TABLE `nota_movimiento`
  ADD CONSTRAINT `fk_origen` FOREIGN KEY (`id_origen`) REFERENCES `origen_destino` (`id_origen`),
  ADD CONSTRAINT `nota_movimiento_ibfk_1` FOREIGN KEY (`id_tipo`) REFERENCES `tipo_movimiento` (`id_tipo`),
  ADD CONSTRAINT `nota_movimiento_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD CONSTRAINT `fk_permisos_acciones` FOREIGN KEY (`id_accion`) REFERENCES `acciones` (`id_accion`),
  ADD CONSTRAINT `permisos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `recepcion_materia_prima`
--
ALTER TABLE `recepcion_materia_prima`
  ADD CONSTRAINT `fk_recep_agricultor` FOREIGN KEY (`id_agricultor`) REFERENCES `agricultores` (`id_agricultor`),
  ADD CONSTRAINT `fk_recep_nota_salida` FOREIGN KEY (`id_nota_salida`) REFERENCES `nota_movimiento` (`id_nota`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_recep_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);

--
-- Filtros para la tabla `variedades`
--
ALTER TABLE `variedades`
  ADD CONSTRAINT `variedades_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
