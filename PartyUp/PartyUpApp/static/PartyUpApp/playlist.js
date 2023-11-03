// upon change of charfield, search for spotify tracks by fetching endpoint in the view
nextButton = document.querySelector('.submit-btn')

form = document.getElementById('playlist_form');
form_errors = document.querySelector('.form-errors');
error = document.querySelector('#song-insertion-error')


table = document.getElementById('song_table')
table_body = table.getElementsByTagName('tbody')[0]

playlist_search_input = document.getElementById('id_playlist_search')
playlist_search_input_error = document.getElementById('playlist-search-error');

playlist_name_input = document.getElementById('id_playlist_name')
playlist_name_input_error = document.getElementById('playlist-name-error');

track_search_input = document.getElementById('id_track_search')
track_search_input_error = document.getElementById('track-search-error');

addButton = document.querySelector('.party-add-song-btn')

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

let i = 0;

addButton.addEventListener('click', function() {
    
    if (track_search_input.value == "") {
        error.innerText = "You must enter a valid song name!"; 
        error.style.display = "block"
        return
    }

    
        for (var j = 0, r = table.rows.length; j < r; j++) {
            if (table.rows[j].cells[0].innerText == track_search_input.value) {
                error.innerText = "Cannot add the same song more than once!"
                error.style.display = "block"
                return;
            }
        } 
        let row = table_body.insertRow(i)

        let song_name_cell = row.insertCell(0)
        let delete_cell = row.insertCell(1)

        song_name_cell.innerHTML = track_search_input.value
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

nextButton.addEventListener("click", function() {
    if (playlist_search_input.value == "" && playlist_name_input.value == "") {
        form_errors.innerHTML = 'Name your custom playlist or search through your own!'
        return;
    }
    if (playlist_search_input.value != "" && playlist_search_input.value != "") {
        form_errors.innerHTML = 'You can only choose one of the two methods!'
        return;
    }
    if (playlist_name_input.value != "") {
        song_list = []
        song_id_list = []
        for (var j = 1, r = table.rows.length; j < r; j++) {
            
            song_text = table.rows[j].cells[0].innerText.split(', Id: ')
            song_name = song_text[0]
            song_id = song_text[1]
            song_list.push(song_name)
            song_id_list.push(song_id)
        } 

        form_errors.innerHTML = ""
        fetch('/partyup/playlist/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            body: new URLSearchParams({
                'playlist_name': playlist_name_input.value,
                'song_list': song_list,
                'song_id_list': song_id_list
            })
        }).then((response) => {
            return response.json()
        }).then((data)=> {
            if (data['form_errors']) {
                
            }
            else {
                form.submit();
            }
        })
    }
    else if (playlist_search_input.value != "") {

        playlist_search_text = playlist_search_input.value.split(', Id: ')
        playlist_search_name = playlist_search_text[0]
        playlist_search_id = playlist_search_text[1]
        form_errors.innerHTML = ""
        fetch('/partyup/playlist/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            body: new URLSearchParams({
                'playlist_search': playlist_search_id
            })
        }).then((response) => {
            return response.json()
        }).then((data)=> {
            if (data['form_errors']) {
                errors = JSON.parse(data['form_errors']);
                
            }
            else {
                form.submit();
            }
        })
    }
})

