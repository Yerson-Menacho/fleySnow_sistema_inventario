$(document).ready(function () {
    console.log("📊 Reporte total de materia prima cargado.");

    // ⚙️ DataTable
    var tabla = $('#tabla-materia-prima').DataTable({
        ajax: {
            url: "/reportes/materia_prima/data",
            type: "GET",
            data: function (d) {
                return {
                    fecha_inicio: $('#fecha_inicio').val() || '',
                    fecha_fin: $('#fecha_fin').val() || '',
                    id_agricultor: $('#id_agricultor').val() || '',
                    id_variedad: $('#id_variedad').val() || '',
                    agrupacion: $('#agrupacion').val() || 'dia'
                };
            },
            dataSrc: '',
            error: function (xhr) {
                console.error("❌ Error al cargar datos:", xhr.responseText);
            }
        },
        columns: [
            { data: 'periodo' },
            { data: 'variedad' },
            {
                data: 'total_bruto',
                render: function (data) {
                    return parseFloat(data || 0).toLocaleString('es-PE', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    });
                }
            },
            {
                data: 'total_jabas',
                render: function (data) {
                    return parseInt(data || 0).toLocaleString('es-PE');
                }
            },
            {
                data: 'total_neto',
                render: function (data){
                    return parseFloat(data || 0).toLocaleString('es-PE',{
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    });
                }
            },
            
            {
                data: 'recepciones_count',
                render: function (data) {
                    return parseInt(data || 0).toLocaleString('es-PE');
                }
            }
        ],
        order: [[0, 'desc']],
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

    // 🔁 Recargar tabla al cambiar filtros
    $('#form-filtros').on('submit', function (e) {
        e.preventDefault();
        tabla.ajax.reload();
    });
    
    // 📄 Exportar PDF
    $('#btn-pdf').on('click', function () {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/materia_prima/pdf?' + params, '_blank');
    });

    // 📊 Exportar Excel
    $('#btn-excel').on('click', function () {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/materia_prima/excel?' + params, '_blank');
    });

    // 🔄 Cambiar encabezado al agrupar
    $('#agrupacion').on('change', function () {
        const texto = $(this).find('option:selected').text();
        $('#tabla-materia-prima thead th:first').text(
            texto === 'Variedad' ? 'Variedad' : 'Periodo'
        );
    });

    // 🧩 SELECT2 Agricultor
    $('#id_agricultor').select2({
        placeholder: 'Seleccione un agricultor',
        allowClear: true,
        ajax: {
            url: '/buscar_agricultores',
            dataType: 'json',
            delay: 250,
            data: function(params) {
                return { q: params.term || '' };
            },
            processResults: function(data) {
                return { results: data };
            },
            cache: true
        },
        templateResult: function(item) {
            return item.text;
        },
        templateSelection: function(item) {
            if (item.id === "") return "Todos";
            const match = (item.text || '').match(/- (.*?) \(DNI:/);
            return match ? match[1].trim() : item.text;
        },
        language: {
            noResults: function() {
                return "Sin resultados encontrados";
            },
            inputTooShort: function() {
                return "Escriba al menos 1 carácter...";
            }
        },
        minimumInputLength: 0,
        width: '100%'
    });

    // 🧩 SELECT2 Variedad
    $('#id_variedad').select2({
        placeholder: 'Seleccione una variedad',
        allowClear: true,
        ajax: {
            url: '/recepcion/buscar_variedades',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return { q: params.term || '' };
            },
            processResults: function (data) {
                return { results: data };
            },
            cache: true
        },
        language: {
            noResults: function () {
                return "Sin resultados encontrados";
            },
            inputTooShort: function () {
                return "Escriba al menos 1 carácter...";
            }
        },
        minimumInputLength: 0,
        width: '100%'
    });
});
