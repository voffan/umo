$(document).ready( function () {
    $('#my_table').DataTable( {
        "dom": 'rtipS',
        "info": false,
        "paging": false
    });
} );
$(document).ready( function () {
    $('#my_table2').DataTable( {
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Russian.json"
        }
    } );
} );
$(document).ready( function () {
    var table = $('#students_list').DataTable({
        "columnDefs": [
            {
                "targets": [ 0 ],
                "searchable": false,
                "orderable": false
            }
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Russian.json"
        },
        "order": [[ 1, 'asc' ]],
        "info": false,
        "paging": true,
        "pageLength": 50,
        "bFilter": true,
        initComplete: function () {
           var column = this.api().column(2);
           var select = $('<select class="filter"><option value=""></option></select>')
               .appendTo('#student_list_filter')
               .on('change', function () {
                  var val = $(this).val();
                  column.search(val ? '^' + $(this).val() + '$' : val, true, false).draw();
               });

           column.data().unique().sort().each(function (d, j) {
               select.append('<option value="' + d + '">' + d + '</option>');
           });
        }
    });
    table.on( 'order.dt search.dt', function () {
        table.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
} );
$(document).ready( function () {
    var table = $('#disciplines_list').DataTable({
        "columnDefs": [
            {
                "targets": [ 0 ],
                "searchable": false,
                "orderable": false
            }
        ],
        "order": [[ 1, 'asc' ]],
        "dom": 'rtipS',
        "info": false,
        "paging": false,
        initComplete: function () {
           var column = this.api().column(3);
           var select = $('<select class="filter"><option value=""></option></select>')
               .appendTo('#disciplines_list_filter')
               .on('change', function () {
                  var val = $(this).val();
                  column.search(val ? '^' + $(this).val() + '$' : val, true, false).draw();
               });

           column.data().unique().sort().each(function (d, j) {
               select.append('<option value="' + d + '">' + d + '</option>');
           });
        }
    });
    table.on( 'order.dt search.dt', function () {
        table.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
} );
$(document).ready( function () {
    var table = $('#brs_list').DataTable({
        "columnDefs": [
            {
                "targets": [ 1 ],
                "visible": false
            },
            {
                "targets": [ 0 ],
                "searchable": false,
                "orderable": false
            }
        ],
        "order": [[ 1, 'asc' ]],
        "dom": 'rtipS',
        "info": false,
        "paging": false,
        initComplete: function () {
           var column = this.api().column(1);
           var select = $('<select class="filter" name="selected_group"></select>')
               .appendTo('#brs_list_filter')
               .on('change', function () {
                  var val = $(this).val();
                  column.search(val ? '^' + $(this).val() + '$' : val, true, false).draw();
               });
           column.data().unique().sort().each(function (d, j) {
               select.append('<option value="' + d + '">' + d + '</option>');
           });
           column.search(select.val ? '^' + select.val() + '$' : select.val, true, false).draw();
        }
    });
    table.on( 'order.dt search.dt', function () {
        table.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
} );
$(document).ready( function () {
    var table = $('#ekran').DataTable( {
        "columnDefs": [
            {
                "targets": [ 0 ],
                "searchable": false,
                "orderable": false
            }
        ],
        "order": [[ 1, 'asc' ]],
        "dom": 'rtipS',
        "info": false,
        "paging": false,
        "fixedHeader": true
    });
    table.on( 'order.dt search.dt', function () {
        table.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
} );
$(document).ready( function () {
    var table = $('#teacher_list').DataTable({
        "columnDefs": [
            {
                "targets": [ 0 ],
                "searchable": false,
                "orderable": false
            }
        ],
        "order": [[ 1, 'asc' ]],
        "dom": 'rtipS',
        "info": false,
        "paging": false,
        initComplete: function () {
           var column = this.api().column(4);
           var select = $('<select class="filter"><option value=""></option></select>')
               .appendTo('#teacher_list_filter')
               .on('change', function () {
                  var val = $(this).val();
                  column.search(val ? '^' + $(this).val() + '$' : val, true, false).draw();
               });

           column.data().unique().sort().each(function (d, j) {
               select.append('<option value="' + d + '">' + d + '</option>');
           });
        }
    });
    table.on( 'order.dt search.dt', function () {
        table.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
} );