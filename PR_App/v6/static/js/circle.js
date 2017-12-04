$(document).ready(function(){

    $.post("/show_num", circle);

    function circle(values) {

        var inner_radius = 200, outer_radius = 215;

        var total = values.total,
        selected = values.selected;

        var startPercent = 1, endPercent = selected/total;

        var twoPi = Math.PI * 2;
        var count = Math.round(Math.abs((endPercent - startPercent) / 0.01));
        var step = endPercent < startPercent ? -0.01 : 0.01;

        var arc = d3.svg.arc()
            .startAngle(0)
            .innerRadius(inner_radius)
            .outerRadius(outer_radius);

        d3.select('#meter').attr('d', arc.endAngle(twoPi));

        function updateProgress(progress) {
            d3.select('#foreground').attr('d', arc.endAngle(twoPi * progress));
            d3.select('#front').attr('d', arc.endAngle(twoPi * progress));
            d3.select('#text').text(selected + "/" + total);
        }

        var progress = startPercent;

        (function loops() {
            updateProgress(progress);

            if (count > 0) {
                count--;
                progress += step;
                setTimeout(loops, 10);
            }
        })();
    }
});