$(document).ready(function () {
    //this plug-in is taken from http://blog.insicdesigns.com/2010/02/creating-a-fancy-menu-using-css3-and-jquery/
    //however, it has some bugs which this fixes.
    var active = "active",
        lavalamp = "lavalamp";

    $('.floatr').each(function () {
        var $this = $(this),
            $parent, $active;
        $parent = $(this).closest('.' + lavalamp);
        $active = $parent.find('li.' + active);

        $this.css({
            "left":$active.offset().left - $parent.offset().left + "px",
            "width":$active.width() + "px"
        });
    });

    $('.' + lavalamp).delegate('li', 'mouseenter mouseleave click', function (e) {
        var type = e.type,
            $this = $(this),
            left, width;

        if (type === 'mouseenter') {
            left = $this.offset().left - ($this.closest('.' + lavalamp).offset().left);
            width = $this.width() + "px";

            $this.closest('ul').next('div.floatr').css({
                "width":width,
                "left":left + "px"
            });

        } else if (type === 'mouseleave') {

            left = $this.siblings('li.active').offset().left - ($this.closest('.' + lavalamp).offset().left);
            width = $this.siblings('li.active').width();

            $this.closest('ul').next('div.floatr').css({
                "width":width + "px",
                "left":left + "px"

            });

        } else if (type === 'click') {
            $this.addClass(active).siblings('li').removeClass(active);

            //you probably do not want to return false.  This prevents the links from working.
//            return false;
        }

    });
});