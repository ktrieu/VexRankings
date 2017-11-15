$(document).ready(function() {
    var rankings_table = $("#rankings-table").DataTable({
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

    $("#week-select").change(function () {
        rankings_table.ajax.url("/api/get_rankings?week_idx=" + $("#week-select").val()).load();
    });

    $("#predict-form").submit(function (e) {
        e.preventDefault();
        week_idx = $("#week-select").val();
        $.get("/api/predict_match?" + $("#predict-form").serialize() + "&week_idx=" + week_idx, function (data) {
            $(".red-chance").text(data.red_chance);
            $(".blue-chance").text(data.blue_chance);
        });
    });
});