{% include 'base1.html' %}

$(function() {
    $('#search').click(function(evt){
    evt.preventDefault();
        $.ajax({
            type: "GET",
            url: "/search/",
            data: {
                'search_text' : $('#search').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR)
{
    $('#search_results').html(data)
}
{% endblock  %}
