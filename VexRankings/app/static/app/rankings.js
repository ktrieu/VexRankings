animate_chance = function(selector, num) {
    // how many decimal places allows
    var decimal_places = 2;
    var decimal_factor = decimal_places === 0 ? 1 : Math.pow(10, decimal_places);

    selector
      .animateNumber(
        {
          number: num * decimal_factor,

          numberStep: function(now, tween) {
            var floored_number = Math.floor(now) / decimal_factor,
                target = $(tween.elem);

            // force decimal places even if they are 0
            floored_number = floored_number.toFixed(decimal_places);

            target.text(floored_number + "%");
          }
        },
        1000
      );
}

suggest_team = function(query, callback) {
    results = $.get("/api/suggest_team?query=" + query, function(data) {
        callback(data);
    }); 
}

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
            animate_chance($(".red-chance"), data.red_chance);
            animate_chance($(".blue-chance"), data.blue_chance);
        });
    });

    $(".team-input").typeahead({
        source: suggest_team,
        autoSelect: false
    });

});