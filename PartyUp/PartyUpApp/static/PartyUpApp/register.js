user_selector = document.getElementById('id_account_type');
vendor_type_selector = document.getElementById('id_vendor_type')

form_p = document.querySelector('.form-p');
form = document.querySelector('.login-container');
submit_wrapper = document.querySelector('.submit-wrapper')

vendor_type_container = document.querySelector('.vendor-type-selection-container');
vendor_address_container = document.querySelector('.address-container');

usernameInput = document.getElementById('id_username');
passwordInput = document.getElementById('id_password1');
confirmPasswordInput = document.getElementById('id_password2');
emailInput = document.getElementById('id_email');
displayNameInput = document.getElementById('id_display_name');
addressInput = document.getElementById('id_address');
numberInput = document.getElementById('id_number');
vendorTypeInput = document.querySelector('id_vendor_type');

user_selector.addEventListener('change', function() {
    if (user_selector.value != "Vendor") {
        vendor_type_container.style.display = "none"
        vendor_address_container.style.display = "none"
        form.style.display = "block";
        submit_wrapper.style.display = "block";

        form_p.innerText = `${user_selector.value} Registration`;
        usernameInput.value = '';
        passwordInput.value = '';
        confirmPasswordInput.value = '';
        emailInput.value = '';
        displayNameInput.value = '';
        numberInput.value = '';

        addressInput.required = false;
        vendorTypeInput.required = false;
    }
    else {
        vendor_type_container.style.display = "block"
        form_p.innerText = `${user_selector.value} Registration`;
        form.style.display = "none";
        submit_wrapper.style.display = "none";
        usernameInput.value = '';
        passwordInput.value = '';
        confirmPasswordInput.value = '';
        emailInput.value = '';
        displayNameInput.value = '';
        numberInput.value = '';
    }
});

vendor_type_selector.addEventListener('change', function() {
    if (vendor_type_selector.value == "Venue") {
        vendor_address_container.style.display = "block";
        addressInput.value = '';
    }
    else {
        vendor_address_container.style.display = "none";
        addressInput.value = '';
        addressInput.required = false;
    }
    form_p.innerText = `${user_selector.value} Registration`;
    form.style.display = "block";
    submit_wrapper.style.display = "block";
    usernameInput.value = '';
    passwordInput.value = '';
    confirmPasswordInput.value = '';
    emailInput.value = '';
    displayNameInput.value = '';
});

passwordInput.placeholder = "\u25CF\u25CF\u25CF\u25CF\u25CF\u25CF\u25CF\u25CF";
confirmPasswordInput.placeholder = "\u25CF\u25CF\u25CF\u25CF\u25CF\u25CF\u25CF\u25CF";


