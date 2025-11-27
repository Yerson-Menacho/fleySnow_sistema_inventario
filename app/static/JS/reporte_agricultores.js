$(document).ready(function() {
    // Inicializar Select2
    $('.select2').select2({
        placeholder: "Seleccione una opción",
        allowClear: true,
        width: '100%'
    });

    // Inicializar DataTable
    var tabla = $('#tabla-agricultores').DataTable({
        ajax: {
            url: "/reportes/agricultores/data",
            type: "GET",
            data: function(d) {
                var obj = {};
                $('#form-filtros').serializeArray().forEach(function(item){
                    obj[item.name] = item.value;
                });
                return obj;
            },
            dataSrc: ''
        },
        columns: [
            { data: 'id_agricultor', title: 'ID' },
            { data: 'codigo_agricultor', title: 'Código' },
            { data: 'nombre_completo', title: 'Nombre completo' },
            { data: 'dni', title: 'DNI' },
            { data: 'telefono', title: 'Teléfono', defaultContent: '—' },
            { data: 'correo', title: 'Correo', defaultContent: '—' },
            { data: 'direccion', title: 'Dirección', defaultContent: '—' },
            { data: 'zona', title: 'Zona', defaultContent: '—' },
            { data: 'cultivo_principal', title: 'Cultivo principal', defaultContent: '—' },
            { data: 'fecha_registro', title: 'Fecha registro',
                render: function(d){ return d ? new Date(d).toLocaleDateString('es-PE') : '—'; }
            },
            { data: 'estado', title: 'Estado' }
        ],
        order: [[9, 'desc']], // Orden por fecha_registro
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

    // Botón buscar
    $('#btn-buscar').on('click', function() {
        tabla.ajax.reload();
    });

    // Exportar PDF / Excel
    $('#btn-pdf').on('click', function() {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/agricultores/pdf?' + params, '_blank');
    });

    $('#btn-excel').on('click', function() {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/agricultores/excel?' + params, '_blank');
    });
});