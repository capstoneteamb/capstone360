$('#review-select').css('cursor', 'pointer');
$('#review-select').on("click", function () {
    window.location.href = '/review/' + $('#options').val()
})

