function initSelect2(selector, url) {
    $(selector).select2({
        placeholder: "Seleccione una opción",
        dropdownParent: $(selector).closest('.modal-window').length ? $(selector).closest('.modal-window') : $(document.body),
        ajax: {
            url: url,
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return { q: params.term };
            },
            processResults: function (data) {
                return { results: data };
            },
            cache: true
        },
        templateResult: function (data) {
            return data.text;
        },
        templateSelection: function (data) {
            if (!data.id) return data.text;

            return data.text
                .replace(/\s-\sDNI:\s\d+/, '')  // quita " - DNI: 12345678"
                .replace(/\s\([^)]*\)/, '')     // quita "(AG001)"
                .trim();
        }
    });
}

// 🔹 Inicializar select2 globales
$(document).ready(function() {
    initSelect2("#insumo", "/movimientos/buscar_insumos");
    initSelect2("#id_origen", "/movimientos/buscar_origenes");
    initSelect2("#id_agricultor", "/recepcion/buscar_agricultor");
    initSelect2("#id_variedad", "/recepcion/buscar_variedades");
    initSelect2("#id_categoria", "/insumos/buscar_categoria");
    initSelect2("#id_usuario", "/usuarios/buscar_usuario");
    initSelect2("#rol", "/usuarios/buscar_roles");

    // ✅ Cuando seleccionas un agricultor → carga sus notas de salida
    $('#id_agricultor').on('select2:select', function (e) {
        const agricultorId = e.params.data.id;
        const $notaSelect = $("#id_nota_salida");

        $notaSelect.prop("disabled", true).html(`<option>Cargando...</option>`);

        $.ajax({
            url: `/recepcion/get_notas_salida/${agricultorId}`,
            method: "GET",
            dataType: "json",
            success: function (data) {
                $notaSelect.empty();

                if (data.length > 0) {
                    $notaSelect.append(`<option value="">-- Selecciona nota --</option>`);
                    data.forEach(nota => {
                        $notaSelect.append(
                            `<option value="${nota.id_nota}">${nota.codigo_nota} - ${nota.cantidad_jabas} jabas</option>`
                        );
                    });
                    $notaSelect.prop("disabled", false);
                } else {
                    $notaSelect.append(`<option value="">No hay notas disponibles</option>`);
                }
            },
            error: function () {
                $notaSelect.html(`<option>Error al cargar notas</option>`);
                alert("❌ Error al cargar notas de salida del agricultor.");
            }
        });
    });
});

$(document).ready(function() {
    // Inicializar Select2
    initSelect2("#id_agricultor", "/recepcion/buscar_agricultor");

    const agricultorId = $("#id_agricultor").val();
    const notaSeleccionada = "{{ recepcion.id_nota_salida }}"; 
    const $notaSelect = $("#id_nota_salida");

    // 🔹 contenedor para mostrar saldo pendiente
    const $saldoLabel = $('<div id="saldo_pendiente" style="margin-top:5px; font-weight:bold; color:#007bff;"></div>');
    $notaSelect.after($saldoLabel);

    // ---------------------------
    // 🔸 CARGA INICIAL (si hay agricultor al entrar)
    // ---------------------------
    if (agricultorId) {
        cargarNotasSalida(agricultorId, notaSeleccionada);
    }

    // ---------------------------
    // 🔸 Cambia agricultor → recargar notas
    // ---------------------------
    $('#id_agricultor').on('select2:select', function (e) {
        const newAgricultorId = e.params.data.id;
        cargarNotasSalida(newAgricultorId);
    });

    // ---------------------------
    // 🔸 Mostrar saldo al seleccionar una nota
    // ---------------------------
    $('#id_nota_salida').on('change', function () {
        const saldo = $(this).find(':selected').data('saldo');
        if (saldo !== undefined) {
            $('#saldo_pendiente').text(`Saldo pendiente: ${saldo} jabas`);
        } else {
            $('#saldo_pendiente').text('');
        }
    });

    // ---------------------------
    // 🔸 Función reutilizable
    // ---------------------------
    function cargarNotasSalida(agricultorId, notaSeleccionada = null) {
        $notaSelect.prop("disabled", true).html(`<option>Cargando...</option>`);

        $.ajax({
            url: `/recepcion/get_notas_salida/${agricultorId}`,
            method: "GET",
            dataType: "json",
            success: function (data) {
                console.log("✅ Datos recibidos:", data);
                $notaSelect.empty();

                if (data && data.length > 0) {
                    data.forEach(nota => {
                        const id = nota.id_nota ?? 0;
                        const codigo = nota.codigo_nota ?? "(sin código)";
                        const saldo = nota.saldo_jabas ?? 0;

                        const option = `
                            <option value="${id}" data-saldo="${saldo}" 
                                ${id == notaSeleccionada ? "selected" : ""}>
                                ${codigo} - 🧺 ${saldo} jabas disponibles
                            </option>
                        `;
                        $notaSelect.append(option);
                    });

                    $notaSelect.prop("disabled", false);

                    // Si hay nota seleccionada al cargar → mostrar saldo de inmediato
                    const selectedSaldo = $notaSelect.find(':selected').data('saldo');
                    if (selectedSaldo !== undefined) {
                        $('#saldo_pendiente').text(`Saldo pendiente: ${selectedSaldo} jabas`);
                    }
                } else {
                    $notaSelect.append(`<option value="">No hay notas disponibles</option>`);
                    $notaSelect.prop("disabled", true);
                    $('#saldo_pendiente').text('');
                }
            },
            error: function (xhr, status, error) {
                console.error("❌ Error al cargar las notas de salida:", error);
                $notaSelect.empty().append(`<option value="">Error al obtener notas</option>`);
                $('#saldo_pendiente').text('');
            }
        });
    }
});
