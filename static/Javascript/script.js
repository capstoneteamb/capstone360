$(document).ready(function () {
    // Adding students/team dashboard
    $('.edit-btn').on('click', function () {
        $this = $('.sub-buttons')
        $add = $('.add-student-btn')
        if (($this).is(":hidden")) {
            $this.slideDown('slow', function () {
                $this.css('display','flex')
            });
            $add.css('display','block');
        } else {
            $this.slideUp('slow');
            $add.css('display','none');
        }
    })
    // Remove dashboard
    $('.remove-btn').on('click', function () {
        $remove = $('.remove-card')
        $display = $('.display-card')
        $lead = $('.lead-card')
        if ($remove.css('display') == "none") {
            $remove.css('display', 'block');
            $display.css('display', 'none');
            $lead.css('display', 'none');
        } else {
            $remove.css('display', 'none');
            $display.css('display', 'block')
        }
    })

    // Lead dashboard
    $('.lead-btn').on('click', function () {
        $lead = $('.lead-card')
        $display = $('.display-card')
        $remove = $('.remove-card')
        if ($lead.css('display') == "none") {
            $lead.css('display', 'block');
            $display.css('display', 'none');
            $remove.css('display', 'none')
        } else {
            $lead.css('display', 'none');
            $display.css('display', 'block')
        }
    })


    // session dropdowns
    $('.selected_session').change(function () {
        sessionStorage.setItem('count', this.value);
    });
    if (sessionStorage.getItem('count')) {
        $('.selected_session').val(sessionStorage.getItem('count'));
    }

    // checkbox for lead
    $('input[id="lead"]').on('change', function () {
        var form_num = $(this).parents("form").attr('class');
        $('.' + form_num + ' input[type="checkbox"]').not(this).prop('checked', false);
    });

    $('.lead-submit').on('click', function () {
        var checked_arr = [];
        var checked = document.querySelectorAll('input[name="is_lead"]:checked')
        for (i = 0; i < checked.length; i++) {
            checked_arr.push(checked[i].value);
        }
        sessionStorage.setItem('leads', JSON.stringify(checked_arr));
    });

    $('.lead-btn').on('click', function () {
        $('input[data-lead="1"]').prop('checked', true);
    });
})