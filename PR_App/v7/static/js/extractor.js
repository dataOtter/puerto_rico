$(document).ready(function(){

    $(document).ajaxStart(function(){
        $.LoadingOverlay("show");
    });
    $(document).ajaxStop(function(){
        $.LoadingOverlay("hide");
    });

    $.post("/get_available_cols", init_cols_selector);

    $('.flex-container').on('click', ".cols-button", add_rem_all_cols);

    $('.flex-container').on('click', ".list-group-item", add_rem_one_col);


    function add_rem_one_col() {
        var cols_scroll_id = $(this).closest('.cols-scroll').attr('id');

        if ( cols_scroll_id.includes('avail') ) {
            var counter_orig = $(this).closest('div').attr('id').substr(-2);
            var counter_dest = counter_orig + 's';
            move_one_col($(this), 'avail', 'selected', counter_dest, counter_orig, cols_scroll_id);
        }
        else if ( cols_scroll_id.includes('selected') ) {
            var counter_orig = $(this).closest('div').attr('id').substr(-3);
            var counter_dest = counter_orig.slice(0,2);
            move_one_col($(this), 'selected', 'avail', counter_dest, counter_orig, cols_scroll_id);
        }
    }


    function add_rem_all_cols() {
        var box_id = $(this).closest('.cols-box').attr('id');

        if ( box_id.includes('avail') ) {
            move_all_cols(box_id, 'avail', 'selected');
        }
        else if ( box_id.includes('selected') ) {
            move_all_cols(box_id, 'selected', 'avail');
        }
    }


    function move_one_col(this_object, move_from, move_to, counter_dest, counter_orig, cols_scroll_id) {
        var col_label = this_object.text();
        var tbl_name = this_object.closest('.panel').find('a').text();
        var move_to_cols_scroll_id = cols_scroll_id.replace(move_from, move_to);

        // if the table does not already exist
        if ($('#' + move_to_cols_scroll_id + ':contains("' + tbl_name + '")').length <= 0) {
            //alert('making ' + tbl_name);
            make_tbl_in_phase_html(tbl_name, counter_dest, move_to_cols_scroll_id);  // make the table
        }
        // either way, add and remove the column
        make_col_in_tbl_html(counter_dest, col_label);
        remove_col_from_tbl_html(counter_orig, col_label);

        // if the origin table is now empty
        if ( $('#collapse' + counter_orig + ' ul').children().length <= 0 ) {
            remove_tbl_from_phase_html(cols_scroll_id, tbl_name);  // remove it
        }
    }

    function move_all_cols(box_id, move_from, move_to){
        var move_to_box_id = box_id.replace(move_from, move_to);
        var cols = $('#' + box_id).find('.cols-scroll').first().children();
        var clone_cols = cols.clone();
        $('#' + move_to_box_id).find('.cols-scroll').first().append(clone_cols);
        $(cols).remove();
    }

    function init_cols_selector(cols){
        var phase_dict = eval(cols.result);
        var counter = 10;

        for (var phase in phase_dict) {
            make_phase_html(phase);
            for (var tbl in phase_dict[phase]){
                counter += 1;
                make_tbl_in_phase_html(tbl, counter, phase + "_avail_cols_scroll");
                $(phase_dict[phase][tbl]).each(function(i, col){
                    make_col_in_tbl_html(counter, col);
                })
            }
        }

    }

    function make_phase_html(phase){
        var to_append = "<h2>" + phase + "</h2>" +
        "<div id='" + phase + "_flex' class='cols-flex'>" +
        "<div id='" + phase + "_avail_cols' class='cols-box'>" +
        "<div class='cols-header'><h3>Available Table Columns</h3><div id='add-button' class='cols-button'>Add All</div></div>" +
        "<div id='" + phase + "_avail_cols_scroll' class='cols-scroll'></div></div>" +
        "<div id='" + phase + "_selected_cols' class='cols-box'>" +
        "<div class='cols-header'><h3>Selected Table Columns</h3><div id='rem-button' class='cols-button'>Remove All</div></div>" +
        "<div id='" + phase + "_selected_cols_scroll' class='cols-scroll'></div></div></div>";

        $("#phase_flex").append(to_append);
    }

    function make_tbl_in_phase_html(tbl, counter, cols_scroll_id){
        var to_append = "<div class='panel-group'><div class='panel panel-default'><div class='panel-heading'>" +
        "<h4 class='panel-title'><a data-toggle='collapse' href='#collapse" + counter + "'>" + tbl + "</a></h4></div>" +
        "<div id='collapse" + counter + "' class='panel-collapse collapse'><ul class='list-group'></ul></div></div></div>";

        $("#" + cols_scroll_id).append(to_append);
    }

    function make_col_in_tbl_html(counter, col){
        var to_append = "<li class='list-group-item tbl-col-label'>" + col + "</li>";

        $("#collapse" + counter + " .list-group").append(to_append);
    }

    function remove_col_from_tbl_html(counter, col) {
        $('#collapse' + counter + ' li:contains("' + col + '")').filter(function() {
            return $(this).text() == col;  // to make sure only exact matches are removed
        }).remove();
    }

    function remove_tbl_from_phase_html(cols_scroll_id, tbl_name) {
        $('#' + cols_scroll_id + ' .panel-group:contains("' + tbl_name + '")').filter(function() {
            return $(this).text() == tbl_name;  // to make sure only exact matches are removed
        }).remove();
    }

})