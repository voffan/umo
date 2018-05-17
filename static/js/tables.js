$(document).ready( function () {
            $('#my_table').DataTable( {
                "dom": 'rtipS',
                "info": false,
                "paging": false
            });
            var s = $('#students_list').DataTable({
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
            var t = $('#brs_list').DataTable({
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
                   var select = $('<select class="filter" name="selected_group"><option value=""></option></select>')
                       .appendTo('#brs_list_filter')
                       .on('change', function () {
                          var val = $(this).val();
                          column.search(val ? '^' + $(this).val() + '$' : val, true, false).draw();
                       });

                   column.data().unique().sort().each(function (d, j) {
                       select.append('<option value="' + d + '">' + d + '</option>');
                   });
                }
            });
            s.on( 'order.dt search.dt', function () {
                s.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
                    cell.innerHTML = i+1;
                } );
            } ).draw();
            t.on( 'order.dt search.dt', function () {
                t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
                    cell.innerHTML = i+1;
                } );
            } ).draw();
        } );