$(document).ready( function () {
    $('#my_table').DataTable( {
        "dom": 'rtipS',
        "info": false,
        "paging": false
    });
} );
var init_function = function () {
   var column = this.api().column(5);
   var select = $('<select class="filter" style="width:150px"></select>')
       .appendTo('#course_state_filter')
       .on('change', function () {
          var val = $(this).val();
          column.search(val ? '^' + $(this).val() + '$' : val, true, false).draw();
       });
   column.search('Не окончен', true, false).draw();
   column.data().unique().sort().each(function (d, j) {
       select.append('<option value="' + d + '">' + d + '</option>');
   });
}
$(document).ready( function () {
    $('#my_table2').DataTable( {
        "language": {
            "url": "/static/Russian.json"
        },
        initComplete: init_function
    } );
} );
$(document).ready( function () {
    $('#awards_list').DataTable( {
        "language": {
            "url": "/static/Russian.json"
        }
    } );
} );

$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var min = parseInt( $('#min').val(), 10 );
        var max = parseInt( $('#max').val(), 10 );
        var age = parseFloat( data[2] ) || 0;

        if ( ( isNaN( min ) && isNaN( max ) ) ||
             ( isNaN( min ) && age <= max ) ||
             ( min <= age   && isNaN( max ) ) ||
             ( min <= age   && age <= max ) )
        {
            return true;
        }
        return false;
    }
);

$(document).ready( function () {
    var table = $('#employee_awards_list').DataTable( {
        "language": {
            "url": "/static/Russian.json"
        }
    } )

    $('#min, #max').keyup( function() {
        table.draw();
    } );
} );
$(document).ready( function () {
    $('#issuers_list').DataTable( {
        "language": {
            "url": "/static/Russian.json"
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
            "url": "/static/Russian.json"
        },
        "order": [[ 1, 'asc' ]],
        "info": false,
        "paging": true,
        "pageLength": 100,
        "lengthChange": false,
        "bFilter": true,
        initComplete: function () {
           var column = this.api().column(2);
           var select = $('<select class="filter"><option value="">-----</option></select>')
               .appendTo('#student_list_filter')
               .on('change', function () {
                  var val = $(this).val();
                  column.search(val ? '^' + $(this).val() + '$' : val, true, false).draw();
               });

           column.data().unique().sort().each(function (d, j) {
               select.append('<option value="' + d + '">' + d + '</option>');
           });
        },
        "fnDrawCallback": function(oSettings) {
        if (oSettings._iDisplayLength > oSettings.fnRecordsDisplay()) {
            $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
        }
        else {
            $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
        }
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
        "language": {
            "url": "/static/Russian.json"
        },
        "order": [[ 1, 'asc' ]],
        "info": true,
        "paging": true,
        "pageLength": 10,
        "lengthChange": true,
        "bFilter": true,
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
                "targets": [ 1, 2 ],
                "visible": false
            },
            {
                "targets": [ 0 ],
                "searchable": false,
                "orderable": false
            }
        ],
        "order": [[ 3, 'asc' ]],
        "dom": 'rtipS',
        "info": false,
        "paging": false,
        initComplete: function () {
            var column1 = this.api().column(2);
            var select1 = $('<select class="filter" name="selected_semester"></select>')
               .appendTo('#brs_list_filter1')
               .on('change', function () {
                  var val = $(this).val();
                  column1.search(val ? '^' + $(this).val() + '$' : val, true, false).draw();
               });
            column1.data().unique().sort().each(function (d, j) {
               select1.append('<option value="' + d + '">' + d + '</option>');
            });
            
            var column2 = this.api().column(1);
            var select2 = $('<select class="filter" name="selected_group"></select>')
               .appendTo('#brs_list_filter2')
               .on('change', function () {
                  var val = $(this).val();
                  column2.search(val ? '^' + $(this).val() + '$' : val, true, false).draw();
               });
            column2.data().unique().sort().each(function (d, j) {
               select2.append('<option value="' + d + '">' + d + '</option>');
            });

            column1.search(select1.val ? '^' + select1.val() + '$' : select1.val, true, false).draw();
            column2.search(select2.val ? '^' + select2.val() + '$' : select2.val, true, false).draw();
        }
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
        "language": {
            "url": "/static/Russian.json"
        },
        "order": [[ 1, 'asc' ]],
        "info": true,
        "paging": true,
        "pageLength": 10,
        "lengthChange": true,
        "bFilter": true,
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
$(document).ready( function () {
    var table = $('#nomenclature_dis').DataTable({
        "columnDefs": [
            {
                "targets": [ 1, 2 ],
                "visible": false
            },
            {
                "targets": [ 0 ],
                "searchable": false,
                "orderable": false
            }
        ],
        "language": {
            "url": "/static/Russian.json"
        },
        "order": [[ 3, 'asc' ]],
        "dom": 'rtipS',
        "info": false,
        "paging": false,
        initComplete: function () {
            var column1 = this.api().column(1);
            var select1 = $('<select class="filter"></select>')
               .appendTo('#nomenclature_dis_filter1')
               .on('change', function () {
                  var val = $(this).val();
                  column1.search(val ? '^' + $(this).val() + '$' : val, true, false).draw();
               });

            column1.data().unique().sort().each(function (d, j) {
               select1.append('<option value="' + d + '">' + d + '</option>');
            });

            var column2 = this.api().column(2);
            var select2 = $('<select class="filter"></select>')
               .appendTo('#nomenclature_dis_filter2')
               .on('change', function () {
                  var val = $(this).val();
                  column2.search(val ? '^' + $(this).val() + '$' : val, true, false).draw();
               });

            column2.data().unique().sort().each(function (d, j) {
               select2.append('<option value="' + d + '">' + d + '</option>');
            });

           column1.search(select1.val ? '^' + select1.val() + '$' : select1.val, true, false).draw();
           column2.search(select2.val ? '^' + select2.val() + '$' : select2.val, true, false).draw();
        }
    });
    table.on( 'order.dt search.dt', function () {
        table.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
} );