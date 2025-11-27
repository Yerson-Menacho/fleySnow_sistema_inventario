$(document).ready(function() {
    // ⚙️ DataTable
    var tabla = $('#tabla-recepciones').DataTable({
        ajax: {
            url: "/reportes/recepciones/data",
            type: "GET",
            data: function(d) {
                var obj = {};

                $('#form-filtros').serializeArray().forEach(function(item) {
                    let name = item.name;
                    let value = item.value;

                    if (name.includes("fecha") && value) {
                        let fecha = new Date(value);
                        if (!isNaN(fecha)) {
                            value = fecha.toISOString().split('T')[0];
                        }
                    }
                    obj[name] = value.trim();
                });

                const q = $('#buscarRecepcion').val();
                if (q) obj.q = q;
                obj.id_agricultor = $('#id_agricultor').val() || '';
                return obj;
            },
            dataSrc: ''
        },
        columns: [
            { data: 'id_recepcion' },
            { data: 'codigo_recepcion' },
            { data: 'agricultor' },
            { 
                data: 'fecha_recepcion',
                render: function(data) {
                    if (!data) return '—';
                    const fecha = new Date(data);
                    return !isNaN(fecha)
                        ? fecha.toLocaleDateString('es-PE', { year: 'numeric', month: '2-digit', day: '2-digit' })
                        : data;
                }
            },
            { data: 'peso_bruto_total' },
            { data: 'peso_neto_total' },
            { data: 'jabas_entregadas' },
            { data: 'jabas_enviadas' },
            { data: 'saldo_jabas' },
            {
                data: 'estado',
                render: function(data) {
                    if (!data) return '—';
                    let e = data.toLowerCase();
                    if (e === 'aprobado') return '<span class="badge bg-success">Aprobado</span>';
                    if (e === 'pendiente') return '<span class="badge bg-warning text-dark">Pendiente</span>';
                    if (e === 'finalizado') return '<span class="badge bg-info text-dark">Finalizado</span>';
                    return `<span class="badge bg-secondary">${data}</span>`;
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

    // 🔁 Recargar tabla al cambiar agricultor
    $('#id_agricultor').on('change', function() {
        tabla.ajax.reload();
    });

    // 🔍 Botón buscar
    $('#btn-buscar').on('click', function() {
        tabla.ajax.reload();
    });

    // 🔍 Buscar con Enter
    $('#q').on('keypress', function(e) {
        if (e.which == 13) {
            tabla.ajax.reload();
            return false;
        }
    });

    // 📄 Exportar PDF
    $('#btn-pdf').on('click', function() {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/recepciones/pdf?' + params, '_blank');
    });

    // 📊 Exportar Excel
    $('#btn-excel').on('click', function() {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/recepciones/excel?' + params, '_blank');
    });

    // 🔍 Búsqueda global
    $('#buscarRecepcion').on('keyup', function(e) {
        var q = $(this).val();
        if ($('#q').length === 0) {
            $('#form-filtros').append('<input type="hidden" name="q" id="q">');
        }
        $('#q').val(q);
        if (e.which === 13 || q.length === 0) {
            $('#btn-buscar').click();
        }
    });

    // 🧩 SELECT2 Agricultor
    $('#id_agricultor').prepend('<option value="">Todos</option>'); // ✅ añadir opción fija

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
});

