var contribution_box = document.getElementById("contribution_box")
var personal_output = document.getElementById("personal");
var errors = document.getElementById("errors")
var other_errors = document.getElementsByClassName("otree-form-errors").item(0)
personal_output.innerHTML = 0;


if(contribution_box.value == ""){
    if(other_errors != null) other_errors.style.display="none";
    personal_output.innerHTML = 0;
    contribution_box.style.background = 'red';
    contribution_box.style.color = 'white';
    contribution_box.style.fontWeight = 'bold'
    errors.style.display = "block";
    errors.style.color = "red";
    errors.style.fontSize = "30px";
    errors.innerHTML = "Please enter a number of energy tokens​";
}

contribution_box.oninput = function () {
    if(0 <= this.value && this.value <= 10){
        personal_output.innerHTML = 10 - this.value;
        contribution_box.style.color = 'blue'
        contribution_box.style.background = 'transparent'
        contribution_box.style.fontWeight = 'bold'
        errors.style.display = "none"
        other_errors.style.display = "none"
    }else{
        personal_output.innerHTML = 0;
        contribution_box.style.background = 'red';
        contribution_box.style.color = 'white';
        contribution_box.style.fontWeight = 'bold'
        errors.style.display = "block";
        errors.style.color = "red";
        errors.style.fontSize = "30px";
        errors.innerHTML = "Please enter the number of energy tokens from 0 to 10​";
    }
}