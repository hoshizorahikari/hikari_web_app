function print(s) {
    let $show = $('#show');
    if ($show.length === 0) {
        $show = $('<div id="show"></div>');
        $('body').append($show);
    }
    let $p = $('<p></p>');
    $p.text(s);
    $show.append($p);
}