/**
 * Content tabs
 */
$.fn.form_tabs = function () {

    var $tabs = $(this);
    var tab_prefix = $tabs.data('tab-prefix');
    if (!tab_prefix)
        return;

    var $tab_links = $tabs.find('a'),
        $tab_select = $tabs.prev('.fieldset--tab-switch').find('select');

    function tab_contents($link) {
        return $('.' + tab_prefix + '--' + $link.attr('href').replace('#', ''));
    }

    function activate_tabs() {
        // Init tab by error, by url hash or init first tab
        if (window.location.hash) {
            $($tabs).find('a[href="' + window.location.hash + '"]').click();
        } else {
            $tab_links.first().trigger('click');
        }
    }

    function activate_pane(pane, select) {
        var $link = $('.tab__link[href="' + pane + '"]');
        $link.parent().parent().find('.active').removeClass('active');
        $link.parent().addClass('active');
        $('.' + tab_prefix).removeClass('active');
        tab_contents($link).addClass('active');

        if(!select) {
            $tab_select.val(pane);
        }
    }

    $tab_links.on('click', function () {
        var pane = $(this).attr('href');
        activate_pane(pane);
    });

    $tab_select.on('change', function () {
        var pane = $(this).val();
        activate_pane(pane, true);
    });

    $(window).on('hashchange', function() {
        activate_tabs();
    });

    activate_tabs();
};

$(document).ready( function() {
    /* Activate tabs */
    $('.tabs__list').form_tabs();
});
