$(document).ready(function() {
    // Inicializar Select2
    $('.select2').select2({
        placeholder: "Seleccione una opción",
        allowClear: true,
        width: '100%'
    });

    // Inicializar DataTable
    var tabla = $('#tabla-usuarios').DataTable({
        ajax: {
            url: "/reportes/usuarios/data",
            type: "GET",
            data: function(d) {
                // Construir objeto con los filtros del formulario
                var obj = {};
                $('#form-filtros').serializeArray().forEach(function(item){
                    obj[item.name] = item.value;
                });
                return obj;
            },
            dataSrc: ''
        },
        columns: [
            { data: 'id_usuario', title: 'ID' },
            { data: 'nombre_completo', title: 'Nombre completo' },
            { data: 'dni', title: 'DNI' },
            { data: 'email', title: 'Email' },
            { data: 'telefono', defaultContent: '—', title: 'Teléfono' },
            { data: 'nombre_rol', title: 'Rol' },
            { 
                data: 'estado', 
                title: 'Estado',
                render: function(d){ 
                    return d == 1 ? 'Activo' : 'Inactivo'; 
                } 
            },
            { 
                data: 'ultimo_login', 
                title: 'Último login',
                render: function(d){ 
                    return d ? new Date(d).toLocaleString('es-PE') : '—'; 
                } 
            },
            { 
                data: 'fecha_creacion', 
                title: 'Fecha creación',
                render: function(d){ 
                    return d ? new Date(d).toLocaleDateString('es-PE') : '—'; 
                } 
            }
        ],
        order: [[8, 'desc']],
        responsive: true,
        lengthMenu: [10, 25, 50, 100],

        // 📘 Traducción completa al español
        language: {
            processing:     "Procesando...",
            search:         "Buscar:",
            lengthMenu:     "Mostrar _MENU_ registros",
            info:           "Mostrando _START_ a _END_ de _TOTAL_ registros",
            infoEmpty:      "Mostrando 0 a 0 de 0 registros",
            infoFiltered:   "(filtrado de _MAX_ registros totales)",
            infoPostFix:    "",
            loadingRecords: "Cargando...",
            zeroRecords:    "No se encontraron resultados",
            emptyTable:     "No hay datos disponibles en la tabla",
            paginate: {
                first:      "Primero",
                previous:   "Anterior",
                next:       "Siguiente",
                last:       "Último"
            },
            aria: {
                sortAscending:  ": activar para ordenar de forma ascendente",
                sortDescending: ": activar para ordenar de forma descendente"
            }
        }
    });

    // Botón buscar
    $('#btn-buscar').on('click', function() {
        tabla.ajax.reload();
    });

    // Buscar con Enter
    $('#q').on('keypress', function(e){
        if(e.which == 13){
            tabla.ajax.reload();
            return false;
        }
    });

    // Exportar PDF / Excel
    $('#btn-pdf').on('click', function() {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/usuarios/pdf?' + params, '_blank');
    });

    $('#btn-excel').on('click', function() {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/usuarios/excel?' + params, '_blank');
    });
});
