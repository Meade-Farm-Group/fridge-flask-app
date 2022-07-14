// used to instantiate the datatables
$(document).ready( function () {
    if ( $.fn.dataTable.isDataTable('#table_id') ) {
        table = $('#table_id').DataTable();
    }
    else {
        table = $('#table_id').DataTable( {
            responsive: true,
            "initComplete": function( settings, json ) {
                $(this).show()
            },
        } );
    }
} );