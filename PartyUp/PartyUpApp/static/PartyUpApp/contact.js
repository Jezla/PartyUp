contactForm = document.getElementById('contact-form')
sendBtn = document.getElementById('send-btn')
contactDiv = document.getElementById('contactDiv')
sentMsg = document.getElementById('sentDiv')
document.querySelector('textarea').addEventListener("input", function(){
    this.style.height = '0px';
    this.style.height = this.scrollHeight + 'px';
  })
name_input = document.getElementById('nameInput');
email_input = document.getElementById('emailInput');
message_input = document.getElementById('messageInput');

//https://stackoverflow.com/questions/6957443/how-to-display-div-after-click-the-button-in-javascript
contactForm.addEventListener('submit', function() {
    // email_input = document.getElementById('emailInput')
    // name_input = document.getElementById('nameInput')
    // message_input = document.getElementById('messageInput')
    name_input.value = '';
    email_input.value = '';
    message_input.value = '';
});
