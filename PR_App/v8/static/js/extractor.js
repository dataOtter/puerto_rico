$(document).ready(function(){

    $(document).ajaxStart( function() { $.LoadingOverlay("show") } );
    $(document).ajaxStop( function(){ $.LoadingOverlay("hide") } );

    $.post("/send_available_cols", init_cols_selector);

    $('.flex-container').on('click', "#generate_download_button", make_zip_download);

    $('.flex-container').on('click', ".cols-button", add_rem_all_cols);

    $('.flex-container').on('click', ".list-group-item", add_rem_one_col);


    function make_zip_download() {
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: get_selected_cols(),  // send selected columns as dict of phases to dict of tables to array of columns
            url: '/receive_selected_cols',
            success: function(zip_folder) {  //use the data returned by the REST service
                console.log("success!! " + zip_folder);
                make_download_link(zip_folder);
            },
            error: function(error) {
                console.log("failure!! " + error)
            }
        });

    }


    function make_download_link(zip_folder) {
        $('#download_link').attr('href', 'outputs/' + zip_folder.zip_folder_name).show();
        $('#generate_download_button').attr("disabled", true);
    }


    function get_selected_cols() {
    // Returns dictionary of phases to dictionary of tables to array of columns, as Json object
        var phase_tbl_cols_dict = {};

        $(".cols-flex").each( function() {  // for each .cols-flex,

            var temp_phase_name = $(this).prev('h2').text();  // get the preceding h2 as the current phase
            //alert(temp_phase_name);
            var temp_tbl_dict = {};
            // walk down to the .cols-scroll section whose id contains selected - here it is hard coded to be the second
            var selected_section_id = $(this).find('.cols-scroll').eq(1).attr('id');

            if ( selected_section_id.includes('selected') ) {  // just to double check that this is the selected section
                $("#" + selected_section_id + ' .panel-group').each( function() {  // for each .panel-group,

                    var temp_table_name = $(this).find("a").text();  // get the text of 'a' as the table name
                    //alert(temp_table_name);
                    var temp_collapse_id = $(this).find("a").attr('href').slice(1);
                    var temp_col_labels = [];

                    $("#" + temp_collapse_id + ' li').each( function() {  // for each li,
                        temp_col_labels.push($(this).text());  // get its text as the column label and put in array
                    })
                    //alert(temp_col_labels);
                    temp_tbl_dict[temp_table_name] = temp_col_labels;  // key: table name, value: array of its columns
                })
            }
            phase_tbl_cols_dict[temp_phase_name] = temp_tbl_dict;  // key: phase name, value: table dict
        })
        /*for ( var phase in phase_tbl_cols_dict) {
            for ( var tbl in phase_tbl_cols_dict[phase]) {
                for ( var i = 0; i < phase_tbl_cols_dict[phase][tbl].length; i++ ) {
                    alert(phase + ': ' + tbl + ': ' + phase_tbl_cols_dict[phase][tbl][i]);
                }
            }
        }*/
        return JSON.stringify(phase_tbl_cols_dict);  // return as Json object
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


    function add_rem_one_col() {
    // $(this) is assumed to be the column li element that was clicked on
        var cols_scroll_id = $(this).closest('.cols-scroll').attr('id');

        if ( cols_scroll_id.includes('avail') ) {  // to make sure the correct counter number is used
            var counter_orig = $(this).closest('div').attr('id').substr(-2);
            var counter_dest = counter_orig + 's';
            move_one_col($(this), 'avail', 'selected', counter_dest, counter_orig, cols_scroll_id);
        }
        else if ( cols_scroll_id.includes('selected') ) {
            var counter_orig = $(this).closest('div').attr('id').substr(-3);
            var counter_dest = counter_orig.slice(0,2);
            move_one_col($(this), 'selected', 'avail', counter_dest, counter_orig, cols_scroll_id);
        }
        enable_disable_generate_download_button();
    }


    function add_rem_all_cols() {
        // $(this) is assumed to be the add/rem all button that was clicked on
        var cols_scroll_id = $(this).closest('.cols-box').find('.cols-scroll').attr('id');

        if ( cols_scroll_id.includes('avail') ) {
            move_all_cols(cols_scroll_id, 'avail', 'selected');
        }
        else if ( cols_scroll_id.includes('selected') ) {
            move_all_cols(cols_scroll_id, 'selected', 'avail');
        }
        enable_disable_generate_download_button();
    }


    function move_one_col(this_col_li_element, move_from, move_to, counter_dest, counter_orig, cols_scroll_id) {
        var col_label = this_col_li_element.text();
        var tbl_name = this_col_li_element.closest('.panel').find('a').text();
        var move_to_cols_scroll_id = cols_scroll_id.replace(move_from, move_to);

        // if the table does not already exist, make the table
        if ($('#' + move_to_cols_scroll_id + ':contains("' + tbl_name + '")').length <= 0) {
            //alert('making ' + tbl_name);
            make_tbl_in_phase_html(tbl_name, counter_dest, move_to_cols_scroll_id);
        }
        // either way, add and remove the column
        make_col_in_tbl_html(counter_dest, col_label);
        remove_col_from_tbl_html(counter_orig, col_label);

        // if the origin table is now empty, remove it
        if ( $('#collapse' + counter_orig + ' ul').children().length <= 0 ) {
            remove_tbl_from_phase_html(cols_scroll_id, tbl_name);
        }
    }

    function move_all_cols(cols_scroll_id, move_from, move_to){
        while ( $('#' + cols_scroll_id).children().length > 0 ) {  // while there are columns left,
            // get the next column element
            var this_col_object = $('#' + cols_scroll_id).find('li').first();
            //alert(this_col_object.text());
            if ( move_from == 'avail' ) {  // to make sure the correct counter number is used
                var counter_orig = this_col_object.closest('div').attr('id').substr(-2);
                var counter_dest = counter_orig + 's';
                move_one_col(this_col_object, 'avail', 'selected', counter_dest, counter_orig, cols_scroll_id);
            }
            else if ( move_from == 'selected' ) {
                var counter_orig = this_col_object.closest('div').attr('id').substr(-3);
                var counter_dest = counter_orig.slice(0,2);
                move_one_col(this_col_object, 'selected', 'avail', counter_dest, counter_orig, cols_scroll_id);
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

    function enable_disable_generate_download_button() {
        $(".cols-scroll").each( function() {
            if ( $(this).attr('id').includes('selected') && $(this).children().length > 0 ) {
                $('#generate_download_button').attr("disabled", false);
                return false;  // must return false in order to break out of each - return true == continue
            } else {
                $('#generate_download_button').attr("disabled", true);
                $('#download_link').hide();
            }
        })
    }

})