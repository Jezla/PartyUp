nextButton = document.querySelector('.submit-btn')

form = document.getElementById('choose_venue_form');
form_errors = document.querySelector('.form-errors');

form_username = document.getElementById('id_venue_username')
form_venue_username_error = document.getElementById('username-error');

form_address = document.getElementById('id_address')
form_address_error = document.getElementById('address-error');


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
    if (form_username.value == "" & form_address.value == "") {
        form_errors.innerHTML = 'One of the two fields is required!'
        return;
    }
    if (form_username.value != "") {
        form_errors.innerHTML = ""
        fetch('/partyup/choose_venue/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            body: new URLSearchParams({
                'venue_username': form_username.value,
            })
        }).then((response) => {
            return response.json()
        }).then((data)=> {
            if (data['form_errors']) {
                errors = JSON.parse(data['form_errors']);
                if (errors['venue_username']) {
                    form_venue_username_error.style.display = 'block';
                    form_venue_username_error.innerHTML = errors['venue_username'][0]['message']
                }
                else {
                    form_venue_username_error.style.display = 'none';
                    form_venue_username_error.innerHTML = '';
                }
            }
            else {
                form.submit();
            }
        })
    }
    else if (form_address.value != "") {
        form_errors.innerHTML = ""
        fetch('/partyup/choose_venue/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            body: new URLSearchParams({
                'address': form_address.value,
            })
        }).then((response) => {
            return response.json()
        }).then((data)=> {
            if (data['form_errors']) {
                errors = JSON.parse(data['form_errors']);
                if (errors['vendor_username']) {
                    form_venue_username_error.style.display = 'block';
                    form_venue_username_error.innerHTML = errors['venue_username'][0]['message']
                }
                else {
                    form_venue_username_error.style.display = 'none';
                    form_venue_username_error.innerHTML = '';
                }
            }
            else {
                form.submit();
            }
        })
    }
})

