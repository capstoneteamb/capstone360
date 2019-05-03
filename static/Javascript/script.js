$(document).ready(function () {
    $('.edit-btn').on('click', function () {
        $this = $('.sub-buttons')
        $add = $('.add-student-btn')
        if($this.css('visibility') == "hidden"){
            $this.css('visibility', 'visible');
            $add.css('visibility', 'visible');
        }else{
            $this.css('visibility', 'hidden');
            $add.css('visibility', 'hidden');
        }
    })
    $('.remove-btn').on('click', function() {
        $remove = $('.remove-card')
        $display = $('.display-card')
        if($remove.css('display') == "none"){
            $remove.css('display', 'block');
            $display.css('display', 'none')
        }else{
            $remove.css('display', 'none');
            $display.css('display', 'block')
        }
    })
    var $session;
    $session = $('option');
    var sessionNum = $('form').text();
    sessionNum = sessionNum.charAt(0);
    console.log(sessionNum);
    $session[sessionNum].setAttribute('selected','sessionNum');
})