addButton = document.querySelector('.party-add-item-btn')

item_input = document.getElementById('id_name')

table = document.getElementById('items_table')
table_body = table.getElementsByTagName('tbody')[0]

next_form = document.getElementById('checklist_form')
error = document.querySelector('#item-insertion-error')
skip_form = document.getElementById('skip_checklist_form')
form_errors = document.querySelector('.form-errors')


nextButton = document.querySelector('.submit-btn')
skipButton = document.querySelector('.skip-btn')

let i = 0;

addButton.addEventListener('click', function() {
    if (item_input.value == "") {
        error.innerText = "You must enter a valid item name!"; 
        error.style.display = "block"
        return
    }
   
    for (var j = 0, r = table.rows.length; j < r; j++) {
        if (table.rows[j].cells[0].innerText == item_input.value) {
            error.innerText = "Cannot add the same item more than once!"
            error.style.display = "block"
            return;
        }
    } 
    let row = table_body.insertRow(i)

    let username_cell = row.insertCell(0)
    let delete_cell = row.insertCell(1)

    username_cell.innerHTML = item_input.value
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
    item_list = []
    for (var j = 1, r = table.rows.length; j < r; j++) {
        item_list.push(table.rows[j].cells[0].innerText)
    } 

    fetch('/partyup/checklist/', {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest', 
            'X-CSRFToken': csrftoken,
        },
        body: new URLSearchParams({
            'item_list': item_list
        })
    }).then((response) => {
        return response.json()
    });

    fetch('/partyup/spotify/is_authenticated')
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            if (!data['is_spotify_authenticated']) {
                fetch('/partyup/spotify/get_auth_url')
                    .then((response) => {
                        return response.json()
                    })
                    .then((data) => {
                        window.location.replace(data['url'])
                    })
            }
            else {
                window.location.replace('/partyup/playlist/')
            }
        })

})

skipButton.addEventListener("click", function() {
    item_list = []
    for (var j = 1, r = table.rows.length; j < r; j++) {
        item_list.push(table.rows[j].cells[0].innerText)
    } 
    // fetch the transaction page and send item_list with it
    fetch('/partyup/checklist/', {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest', 
            'X-CSRFToken': csrftoken,
        },
        body: new URLSearchParams({
            'item_list': item_list
        })
    }).then((response) => {
        return response.json()
    }).then(skip_form.submit())
})
