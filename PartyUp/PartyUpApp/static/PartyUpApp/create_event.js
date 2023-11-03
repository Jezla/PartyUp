nextButton = document.querySelector('.submit-btn')

form = document.getElementById('create_event_form');
form_date_error = document.querySelector('.form-errors');

form_name = document.getElementById('id_name');
form_name_error = document.getElementById('name-error');

form_description = document.getElementById('id_description');
form_description_error = document.getElementById('description-error');

form_start_date = document.getElementById('id_start_date');
form_start_date_error = document.getElementById('start-date-error');

form_end_date = document.getElementById('id_end_date');
form_end_date_error = document.getElementById('end-date-error');

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

nextButton.addEventListener("click", function() {
    fetch('/partyup/create_event/', {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest', 
            'X-CSRFToken': csrftoken,
        },
        body: new URLSearchParams({
            'name': form_name.value,
            'description': form_description.value,
            'start_date': form_start_date.value,
            'end_date': form_end_date.value
        })
    }).then((response) => {
        return response.json()
    }).then((data) => {
        if (data['form_errors']) {
            //display errors
            errors = JSON.parse(data['form_errors'])
            if (errors['name']) {
                form_name_error.style.display = 'block'
                form_name_error.innerHTML = errors['name'][0]['message']
            }
            else {
                form_name_error.style.display = 'none'
                form_name_error.innerHTML = ''
            }
            if (errors['description']) {
                form_description_error.style.display = 'block'
                form_description_error.innerHTML = errors['description'][0]['message']
            }
            else {
                form_description_error.style.display = 'none'
                form_description_error.innerHTML = ''
            }
            if (errors['start_date']) {
                form_start_date_error.style.display = 'block'
                form_start_date_error.innerHTML = errors['start_date'][0]['message']
            }
            else {
                form_start_date_error.style.display = 'none'
                form_start_date_error.innerHTML = ''
            }
            if (errors['end_date']) {
                form_end_date_error.style.display = 'block'
                form_end_date_error.innerHTML = errors['end_date'][0]['message']
            }
            else {
                form_end_date_error.style.display = 'none'
                form_end_date_error.innerHTML = ''
            }
            if (errors['__all__']) {
                form_date_error.style.display = 'block'
                form_date_error.innerHTML = errors['__all__'][0]['message']
            }
            else {
                form_date_error.style.display = 'none'
                form_date_error.innerHTML = ''
            }
        }
        else {
            form.submit();
        }
    })
})


