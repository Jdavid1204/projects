const title = document.getElementById('title');
const content = document.getElementById('content');
const form = document.getElementById('Blog-form');
const error = document.getElementById('error')




form.addEventListener('submit', (e)=>{
    if (title.value == "" || title.value == null){
        e.preventDefault();
        title.style.backgroundColor = "lightgrey";
        error.innerHTML = "Please enter a value!";


    }

    if (content.value == "" || content.value == null){
        e.preventDefault();
        content.style.backgroundColor = "lightgrey";
        error.innerHTML = "Please enter a value!";

    }

})


function clearIt(){
    if (confirm("Would you like to clear content?")){
        document.getElementById("Blog-form").reset();
    }

}