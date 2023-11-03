deleteButton = document.getElementById('delete-btn')
deleteModalButton = document.getElementById('delete-modal-btn')
error = document.getElementById('error')

event_json = JSON.parse(document.getElementById('event').textContent);
event_id = event_json['id']

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

deleteButton.addEventListener('click', function() {

    fetch('/partyup/event/delete', {
        method: "POST",
        credentials: 'same-origin',
        headers:{
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest', 
            'X-CSRFToken': csrftoken,
        },
        body: new URLSearchParams({
            'event_id': event_id
        })
    }).then((response) => {
        return response.json()
    }).then((data) => {
        if (data['error']) {
            error.innerText = data['error']
        }
        else {
            var row = deleteModalButton.parentNode.parentNode
            row.parentNode.removeChild(row);
            error.innerText = `You're event was succesfully deleted!`
        } 
    })
})