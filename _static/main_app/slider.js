  var slider = document.getElementById("myRange");
  var group_output = document.getElementById("group");
  var personal_output = document.getElementById("personal");
  var tokens_left = document.getElementById('left');
  var hidden_input = document.getElementById('id_my_hidden_input');

  const is_trial = hidden_input.name
  const left = parseInt(hidden_input.value.split(" ")[0]);

  group_output.innerHTML = slider.value;
  personal_output.innerHTML = slider.value;

  if (is_trial != "True"){
    tokens_left.innerHTML = left - slider.value;
  }



  slider.oninput = function() {
    group_output.innerHTML = this.value;
    personal_output.innerHTML = 10 - this.value;
    if (is_trial != "True") {
      tokens_left.innerHTML = left - this.value;
    }
  }

/*
document.querySelector('input[type=range]').addEventListener('input', function() {
  this.setAttribute('value', this.value);
});
*/

document.querySelector('input[type=range]').addEventListener('input', function() {
  this.setAttribute('value', this.value);
}, false);