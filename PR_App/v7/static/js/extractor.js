$(document).ready(function(){

    $(document).ajaxStart(function(){
        $.LoadingOverlay("show");
    });
    $(document).ajaxStop(function(){
        $.LoadingOverlay("hide");
    });

    $.post("/get_available_cols", init_cols_selector);

    function init_cols_selector(cols){
        var phase_dict = eval(cols.result);

        for (var phase in phase_dict) {
            alert(phase);
            for (var tbl in phase_dict[phase]){
                alert(tbl);
                $(phase_dict[phase][tbl]).each(function(i, col){
                    alert(col);
                })
            }
        }

    }

})