// if ('{{ player.timesInstruction2 }}' == '0') {
//     for (i = 0; i < document.getElementsByClassName("form-check-input").length; i++) {
//         document.getElementsByClassName("form-check-input").item(i).checked = false;
//     }
//
// } else {
//     for (i = 0; i < document.getElementsByClassName("form-check-input").length; i++) {
//         document.getElementsByClassName("form-check-input").item(i).checked = false;
//     }
// }
//
// if ('{{ player.page_attempts }}' == '0') {
// var fields = document.querySelectorAll('.form-check-input');
// for (var field of fields) {
//   field.checked = false;
// }
// }

function reset_form_fields(){
  console.log('test');
  var fields = document.querySelectorAll('.form-check-input');

  for (field of fields) {
    console.log('field', field.checked);
    if (field.checked === true) {
      console.log('field checked', field.value);
      field.checked = false;
    }
  }

}


function disableButton(btn) {
  if (typeof btn === 'string') {
    btn = document.querySelector(btn);
  }
  btn.classList.add('disabled');
  btn.disabled = true;
}


function enableButton(btn) {
  if (typeof btn === 'string') {
    btn = document.querySelector(btn);
  }
  btn.classList.remove('disabled');
  btn.disabled = false;
}


function toggleButton(node) {
  if (typeof node === 'string') {
    console.log(node);
    document.querySelector(node).classList.toggle('disabled');
  } else {
    console.log(node, 'toggle' );
    node.classList.toggle('disabled');
  }
}

function parseCurrency(str) {
    raw_numbers = str.split(" ");
    let numbers = [];
    for (let i = 0; i < raw_numbers.length; i++) {
        let n = raw_numbers[i];
        n = n.replace(/\D/g, '');
        n = parseInt(n);
        numbers.push(n);
    }

    return numbers;
}

function gameTableAddRow(container, user_id, current_contribution, total_contribution) {
    let row = document.createElement("tr");
    row.append(document.createElement("td"));
    row.append(document.createElement("td"));

    let label = document.createElement("td");
    label.innerHTML = "Player " + user_id + "'s contribution to the group conservation account:";
    row.append(label);

    let current_contribution_HTML = document.createElement("td");
    current_contribution_HTML.innerHTML = "<e style='color: #0000ff'>" + current_contribution + " tokens</e>";
    row.append(current_contribution_HTML);

    let total_contribution_HTML = document.createElement("td");
    total_contribution_HTML.innerHTML = "<e style='color: #0000ff'>" + total_contribution + " tokens</e>";
    row.append(total_contribution_HTML);

    container.append(row);
}
