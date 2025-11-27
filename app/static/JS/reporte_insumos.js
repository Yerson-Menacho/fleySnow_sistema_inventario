$(document).ready(function() {
    var tabla = $('#tabla-insumos').DataTable({
        ajax: {
            url: "/reportes/insumos/data",
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
            { data: 'id' },
            { data: 'codigo' },
            { data: 'nombre' },
            { data: 'categoria' },
            { data: 'variedad' },
            { data: 'stock' },
            { data: 'unidad' },
            { data: 'estado' },
            { data: 'fecha_creacion' }
        ],
        order: [[8, 'desc']],
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

    $('#btn-buscar').on('click', function() {
        tabla.ajax.reload();
    });

    $('#q').on('keypress', function(e){
        if(e.which == 13){
            tabla.ajax.reload();
            return false;
        }
    });

    $('#btn-pdf').on('click', function() {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/insumos/pdf?' + params, '_blank');
    });

    $('#btn-excel').on('click', function() {
        var params = $('#form-filtros').serialize();
        window.open('/reportes/insumos/excel?' + params, '_blank');
    });
});
