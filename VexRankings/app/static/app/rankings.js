$(document).ready(function() {
    $("#rankings-table").DataTable({
        ajax : "/api/get_rankings",
        columns : [
            { data : "name" },
            { 
                data : "elo",
                render : $.fn.dataTable.render.number( ',', '.', 0)
            },
            { 
                data : "elo_change",
                render : $.fn.dataTable.render.number( ',', '.', 0)
            },
        ]
    });
});