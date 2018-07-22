var slider = document.getElementById("myRange");
var group_output = document.getElementById("group");
var personal_output = document.getElementById("personal");

group_output.innerHTML = slider.value;
personal_output.innerHTML = slider.value;

slider.oninput = function() {
  group_output.innerHTML = this.value;
  personal_output.innerHTML = 10 - this.value;
}