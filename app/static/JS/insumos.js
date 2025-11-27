document.addEventListener("DOMContentLoaded", function () {
    const categoriaSelect = $("#id_categoria");
    const variedadSelect = $("#id_variedad");

    // Datos JSON inyectados por Flask
    const ALL_VARIEDADES = JSON.parse(document.getElementById("all-variedades-data").textContent);
    const CURRENT_VARIEDAD_ID = JSON.parse(document.getElementById("current-variedad-data").textContent);

    // ==========================
    // 🔹 Inicializar select2 (categoría y variedad)
    // ==========================
    initSelect2("#id_categoria", "/insumos/buscar_categoria");

    // La variedad inicialmente sin datos
    variedadSelect.select2({
        placeholder: "-- Ninguna --",
        allowClear: true,
        width: "100%",
        data: []
    }).prop("disabled", true);

    // ==========================
    // 🔹 Función: Renderizar variedades según categoría
    // ==========================
    function renderVariedades(catId) {
        // Limpiar select
        variedadSelect.empty();

        if (!catId) {
            variedadSelect.select2({
                placeholder: "-- Selecciona una categoría primero --",
                allowClear: true,
                width: "100%"
            }).prop("disabled", true);
            return;
        }

        const matches = ALL_VARIEDADES.filter(v => String(v.id_categoria) === String(catId));

        if (matches.length === 0) {
            variedadSelect.select2({
                placeholder: "-- Sin variedades disponibles --",
                allowClear: true,
                width: "100%"
            }).prop("disabled", true);
            return;
        }

        // Habilitar y cargar variedades
        const options = matches.map(v => ({
            id: v.id_variedad,
            text: v.nombre_variedad
        }));

        variedadSelect.select2({
            data: options,
            placeholder: "-- Selecciona una variedad --",
            allowClear: true,
            width: "100%"
        }).prop("disabled", false);

        // Preseleccionar si corresponde (modo edición)
        if (CURRENT_VARIEDAD_ID) {
            variedadSelect.val(String(CURRENT_VARIEDAD_ID)).trigger("change");
        }
    }

    // ==========================
    // 🔹 Evento: cambio de categoría
    // ==========================
    categoriaSelect.on("change", function () {
        const selectedId = $(this).val();
        renderVariedades(selectedId);
    });

    // ==========================
    // 🔹 Render inicial (modo edición)
    // ==========================
    const initialCatId = categoriaSelect.val();
    if (initialCatId) {
        renderVariedades(initialCatId);
    }
});
