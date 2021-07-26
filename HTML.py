# Write formatted HTML for data

fid = open('df.html', 'r')
table = fid.read()
fid.close()

fid = open('upd.txt', 'r')
last_upd = fid.read()
fid.close()

HEADER='''<head>
<link rel='stylesheet' href='https://cdn.datatables.net/1.10.25/css/jquery.dataTables.min.css'>
<script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.5.1.js"></script>
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.25/js/jquery.dataTables.min.js"></script>

<script>

$(document).ready(function() {
    $('#sampleTable').DataTable( {
        initComplete: function () {
            this.api().columns([1]).every( function () {
                var column = this;
                var select = $('<select><option value=""></option></select>')
                    .appendTo( $(column.header()) )
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );

                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );

                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option value="'+d+'">'+d+'</option>' )
                } );
            } );
        }
    } );
} );
</script>
<h4>ETFs listed in ASX</h4> '''

HEADER2 = '''
<h4>{lst_upd} </h4>
</head>
'''.format(lst_upd=last_upd)

fid = open('ASX_ETFS.html','w')
fid.write(HEADER+HEADER2+table)
fid.close()
