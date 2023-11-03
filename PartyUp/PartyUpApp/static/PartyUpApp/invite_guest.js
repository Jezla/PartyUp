addButton = document.querySelector('.party-add-vendor-btn')

guest_input = document.getElementById('id_guest_username')

table = document.getElementById('guest_table')
table_body = table.getElementsByTagName('tbody')[0]

form = document.getElementById('invite_guest_form')
error = document.querySelector('#guest-insertion-error')
form_errors = document.querySelector('.form-errors');

nextButton = document.querySelector('.submit-btn')

let i = 0;

addButton.addEventListener('click', function() {
    if (guest_input.value == "") {
        error.innerText = "You must enter a valid guest username!"; 
        error.style.display = "block"
        return
    }

    fetch(`/partyup/guest_info?username=${guest_input.value}`, {
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            error.innerText = data.error
            error.style.display = "block"
        }
        else {
            for (var j = 0, r = table.rows.length; j < r; j++) {
                if (table.rows[j].cells[0].innerText == guest_input.value) {
                    error.innerText = "Cannot add the same guest more than once!"
                    error.style.display = "block"
                    return;
                }
            } 
            let row = table_body.insertRow(i)

            let username_cell = row.insertCell(0)
            let first_name_cell = row.insertCell(1)
            let last_name_cell = row.insertCell(2)
            let delete_cell = row.insertCell(3)
    
            username_cell.innerHTML = guest_input.value
            first_name_cell.innerHTML = data.first_name
            last_name_cell.innerHTML = data.last_name
            let btn = document.createElement("button")
            btn.type = "button"
            btn.innerHTML = `<img class="delete-img" src="/static/PartyUpApp/trash-fill.svg" alt="Delete">`
            btn.classList.add('btn', 'delete-btn')
            btn.setAttribute('id', 'delete-btn');

            btn.addEventListener('click', function() {
                var row = this.parentNode.parentNode
                row.parentNode.removeChild(row);
                i--;
            })

            //finish off delete_cell functionality
            delete_cell.appendChild(btn)
    
            i += 1
            error.style.display = "none"
        }
    })    
})

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
    guest_list = []
    for (var j = 1, r = table.rows.length; j < r; j++) {
        guest_list.push(table.rows[j].cells[0].innerText)
    } 

    fetch('/partyup/invite_guests/', {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest', 
            'X-CSRFToken': csrftoken,
        },
        body: new URLSearchParams({
            'guest_list': guest_list
        })
    }).then((response) => {
        return response.json()
    }).then((data) => {
        if (data['form_errors']) {
            errors = JSON.parse(data['form_errors']);
            if (errors['guest_username']) {
                form_errors.style.display = 'block';
                form_errors.innerHTML = errors['guest_username'][0]['message']
            }
            else {
                form_errors.style.display = 'none';
                form_errors.innerHTML = '';
            }
        }
        else {
            form.submit();
        } 
    })
})
