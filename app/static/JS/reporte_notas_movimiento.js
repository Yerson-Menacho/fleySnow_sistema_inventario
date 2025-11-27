$(document).ready(function() {
    var tabla = $('#tabla-notas').DataTable({
        ajax: {
            url: "/reportes/movimientos/data",
            type: "GET",
            data: function(d) {
                var obj = {};

                // ✅ Serializamos los campos del formulario de filtros
                $('#form-filtros').serializeArray().forEach(function(item) {
                    let name = item.name;
                    let value = item.value;

                    // 🗓️ Si es un campo de fecha, normalizamos formato
                    if (name.includes("fecha") && value) {
                        // Intenta crear una fecha válida
                        let fecha = new Date(value);
                        if (!isNaN(fecha)) {
                            value = fecha.toISOString().split('T')[0]; // YYYY-MM-DD
                        }
                    }

                    obj[name] = value.trim();
                });

                // 🔍 Incluye búsqueda general si existe
                const q = $('#buscarMovimiento').val();
                if (q) obj.q = q;

                return obj;
            },
            dataSrc: ''
        },
        columns: [
            { data: 'id_nota' },
            { data: 'codigo_nota' },
            { data: 'tipo_movimiento' },
            { 
                data: 'fecha',
                render: function(data) {
                    if (!data) return '—';
                    // Formatear fecha si viene tipo ISO
                    const fecha = new Date(data);
                    if (!isNaN(fecha)) {
                        return fecha.toLocaleDateString('es-PE', { year: 'numeric', month: '2-digit', day: '2-digit' });
                    }
                    return data;
                }
            },
            { data: 'referencia' },
            { data: 'usuario' },
            { data: 'origen_destino' },
            { data: 'observacion' },
            {
                data: 'estado',
                render: function(data) {
                    if (!data) return '—';
                    let estado = data.toLowerCase();
                    if (estado === 'aprobado') {
                        return '<span class="badge bg-success">Aprobado</span>';
                    } else if (estado === 'pendiente') {
                        return '<span class="badge bg-warning text-dark">Pendiente</span>';
                    } else if (estado === 'anulado') {
                        return '<span class="badge bg-danger">Anulado</span>';
                    } else {
                        return `<span class="badge bg-secondary">${data}</span>`;
                    }
                }
            }
        ],
        order: [[3, 'desc']],
        responsive: true,
        lengthMenu: [10, 25, 50, 100],
        language: {
            processing: "Procesando...",
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ registros",
            info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
            infoEmpty: "Mostrando 0 a 0 de 0 registros",
            infoFiltered: "(filtrado de _MAX_ registros totales)",
            loadingRecords: "Cargando...",
            zeroRecords: "No se encontraron resultados",
            emptyTable: "No hay datos disponibles en la tabla",
            paginate: {
                first: "Primero",
                previous: "Anterior",
                next: "Siguiente",
                last: "Último"
            }
        }
    });

    // 🔍 Botón buscar
    $('#btn-buscar').on('click', function() {
        tabla.ajax.reload();
    });

    // 🔍 Buscar con Enter en campo texto
    $('#q').on('keypress', function(e) {
        if (e.which == 13) {
            tabla.ajax.reload();
            return false;
        }
    });

    // 📄 Exportar PDF
    $('#btn-pdf').on('click', function() {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/movimientos/pdf?' + params, '_blank');
    });

    // 📊 Exportar Excel
    $('#btn-excel').on('click', function() {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/movimientos/excel?' + params, '_blank');
    });

    // 🔍 Búsqueda global desde el campo en index
    $('#buscarMovimiento').on('keyup', function(e) {
        var q = $(this).val();
        if ($('#q').length === 0) {
            $('#form-filtros').append('<input type="hidden" name="q" id="q">');
        }
        $('#q').val(q);
        if (e.which === 13 || q.length === 0) {
            $('#btn-buscar').click();
        }
    });
});
