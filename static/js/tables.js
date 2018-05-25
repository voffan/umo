            $(document).ready( function () {
                $('#my_table').DataTable( {
                    "dom": 'rtipS',
                    "info": false,
                    "paging": false
            });
            $(document).ready( function () {
                $('#my_table2').DataTable( {
                    "language": {
                        "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Russian.json"
                    }
                } );
            } );
            $(document).ready( function () {
                var a = $('#students_list').DataTable({
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
                a.on( 'order.dt search.dt', function () {
                    a.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
                        cell.innerHTML = i+1;
                    } );
                } ).draw();
            } );
            var b = $('#disciplines_list').DataTable({
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
            var c = $('#brs_list').DataTable({
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
            var d = $('#ekran').DataTable( {
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
            var e = $('#teacher_list').DataTable({
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
            b.on( 'order.dt search.dt', function () {
                b.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
                    cell.innerHTML = i+1;
                } );
            } ).draw();
            c.on( 'order.dt search.dt', function () {
                c.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
                    cell.innerHTML = i+1;
                } );
            } ).draw();
            d.on( 'order.dt search.dt', function () {
                d.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
                    cell.innerHTML = i+1;
                } );
            } ).draw();
            e.on( 'order.dt search.dt', function () {
                e.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
                    cell.innerHTML = i+1;
                } );
            } ).draw();
        } );