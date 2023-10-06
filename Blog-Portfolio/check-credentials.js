const passwordValue = document.getElementById('password')
const password2Value = document.getElementById('password-confirmation')
const form = document.getElementById('form')
const error = document.getElementById('error')



form.addEventListener('submit', (e)=>{
    let messages = [];
    if (passwordValue.value == "" || passwordValue.value == null){
        e.preventDefault();
        error.innerHTML = "Please enter a value.";
    }

    else if (passwordValue.value != password2Value.value){
        e.preventDefault();
        error.innerHTML = "Passwords should be the same";
    }
})
