submit_button = document.querySelector('.submit-btn')
rating_label = document.getElementById('rating-lab')

star_list = document.querySelectorAll('input[name="rating"]')

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const csrftoken = getCookie('csrftoken');

submit_button.addEventListener("click", function() {
    let star_value = 0;
    for (i = 0 ; i < star_list.length; i++) {
        if (star_list[i].checked == true) {
            star_value = star_list[i].value;
            break;
        }
    }
    url = window.location.href
    main_domain = '/partyup/vendor_profile/'
    url_split = url.split('/')
    vendor_id = url_split[url_split.length - 2]

    final_request = main_domain.concat(vendor_id, '/');
    fetch(final_request, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        body: new URLSearchParams({
            'vendor_user': vendor_id,
            'rating': star_value
        })
    }).then((response) => {
        return response.json()
    }).then((data) => {


        rating_label.innerText = data.rating;
    })
})
