document.addEventListener('DOMContentLoaded', () => {
    (function ($) {
        function formSetDay() {
            var lastday = formSetLastDay($('.js-changeYear').val(), $('.js-changeMonth').val());
            var option = '<option value="日" selected="selected">日</option>\n';
            for (var i = 1; i <= lastday; i++) {
                if (i === $('.js-changeDay').val()) {
                    option += '<option value="' + i + '" selected="selected">' + i + '</option>\n';
                } else {
                    option += '<option value="' + i + '">' + i + '</option>\n';
                }
            }
            $('.js-changeDay').html(option);
        }

        function formSetLastDay(year, month) {
            var lastday = new Array('', 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
            if ((year % 4 === 0 && year % 100 !== 0) || year % 400 === 0) {
                lastday[2] = 29;
            }
            return lastday[month];
        }

        $('.js-changeYear, .js-changeMonth').change(function () {
            formSetDay();
        });
    })(jQuery);


    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {

        // Add a click event on each of them
        $navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {

                // Get the target from the "data-target" attribute
                const target = el.dataset.target;
                const $target = document.getElementById(target);

                // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');

            });
        });
    }

    

});