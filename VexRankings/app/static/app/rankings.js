$(document).ready(function() {
    $("#rankings-table").DataTable({
        ajax : "/api/get_rankings",
        columns : [
            { data : "name" },
            { data : "elo" },
            { data : "elo_change" }
        ]
    });
});