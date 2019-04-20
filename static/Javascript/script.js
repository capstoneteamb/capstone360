$(document).ready(function () {
    $('.edit-btn').on('click', function () {
        $this = $('.sub-buttons')
        if($this.css('visibility') == "hidden"){
            $this.css('visibility', 'visible');
        }else{
            $this.css('visibility', 'hidden');
        }
    })
})