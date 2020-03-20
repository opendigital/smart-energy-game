var contribution_box = document.getElementById("contribution_box")
var personal_output = document.getElementById("personal");
var errors = document.getElementById("errors")
var other_errors = document.getElementsByClassName("otree-form-errors").item(0)
personal_output.innerHTML = 0;

if(other_errors != null){
    other_errors.style.display = "none"
    errors.style.display = "block";
    errors.style.color = "#CC444B";
    errors.style.fontSize = "30px";
    errors.innerHTML = "Please enter a number of energy tokens";
    errors.style.background = "transparent"
    errors.style.marginBottom = "10px"
    errors.style.borderRadius = "15px"
}

function game_contribution_onchange(){
  document.getElementById('personal').setAttribute('value',10-this.value)
  document.getElementById('private_box').setAttribute('value',10-this.value)
}
function game_contribution_oninput(){
    if(0 <= this.value && this.value <= 10){
        personal_output.innerHTML = 10 - this.value;
    } else {
        personal_output.innerHTML = 0;
    }

}

contribution_box.onchange = function(){
    document.getElementById('personal').setAttribute('value',10-this.value)
    document.getElementById('private_box').setAttribute('value',10-this.value)
}

contribution_box.oninput = function () {
    if(0 <= this.value && this.value <= 10){
        personal_output.innerHTML = 10 - this.value;
        contribution_box.style.color = 'blue'
        contribution_box.style.background = 'transparent'
        contribution_box.style.fontWeight = 'bold'
        errors.style.display = "none"
        if (other_errors != null)
        other_errors.style.display = "none"
    }else{
        personal_output.innerHTML = 0;
        contribution_box.style.background = "#CC444B";
        contribution_box.style.color = 'white';
        contribution_box.style.fontWeight = 'bold'
        if(other_errors)other_errors.style.display = "none"
        errors.style.display = "block";
        errors.style.color = "#CC444B";
        errors.style.fontSize = "30px";
        errors.innerHTML = "Please enter a number of energy tokens";
        errors.style.background = "transparent"
        errors.style.marginBottom = "10px"
        errors.style.borderRadius = "15px"
    }
}