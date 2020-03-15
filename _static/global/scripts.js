// https://ourcodeworld.com/articles/read/188/encode-and-decode-html-entities-using-pure-javascript
(function(window){
  window.htmlentities = {
    /**
    * Converts a string to its html characters completely.
    * @param {String} str String with unescaped HTML characters
    **/
    encode : function(str) {
      var buf = [];

      for (var i=str.length-1;i>=0;i--) {
        buf.unshift(['&#', str[i].charCodeAt(), ';'].join(''));
      }

      return buf.join('');
    },
    /**
    * Converts an html characterSet into its original character.
    * @param {String} str htmlSet entities
    **/
    decode : function(str) {
      return str.replace(/&#(\d+);/g, function(match, dec) {
        return String.fromCharCode(dec);
      });
    }
  };
})(window);


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

function toggleButton(node) {
  if (typeof node === 'string') {
    document.querySelector(node).classList.toggle('disabled');
  } else {
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

function parseTemplateObject(str) {
  str = htmlentities.decode(str);
  str = str.replace(/'/g, '"');
  try {
    var parsed_data = JSON.parse(str);
  } catch (e) {
    console.log('bad characters', e);
    return str;
  } finally {
    return parsed_data;
  }
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


function checkForm(){
  var reports = {};
  var box_good_class = 'success';
  var box_warn_class = 'error';
  var msg_bad_class = 'show-hint';
  var msg_good_class = 'show-success';

  var errors = [];
  var prefix ='field_';
  var otree_form = document.querySelector('form#form');


  // USE THE BUILTIN BROWSER VALIDATION WHERE ITS AVAIABLE
  // BEFORE DOING EXTRA WORK
  if (typeof document.forms.form.checkValidity == 'function') {
    if (!otree_form.checkValidity()){
      otree_form.reportValidity();
      return false;
    }
  }

  // form2js -
  var form_data = form2js(otree_form);
  if (form_data.length === 0) {
    console.log('nothing selected');
    return false;
  }

  for (field of Object.keys(FORM_KEY)) {
    if (field in form_data) {
      if (form_data[`${field}`] == FORM_KEY[`${field}`]) {
        reports[`${prefix}${field}`] = true;
      } else {
        reports[`${prefix}${field}`] = false;
        errors.push({field: form_data[`${field}`]});
      }
    }
  }


  for (var field of Object.keys(reports)) {
    var field_class = field ? box_warn_class : box_good_class;
    var msg_class = field ? msg_good_class : msg_bad_class;
    document.querySelector(`#id_${field}`).classList.add(field_class);
    document.querySelector(`#id_${field}_message`).classList.add(msg_class);

  }

  if (errors.length > 0) {
    window.formFail();
  } else {
    window.formSuccess();
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

function formSuccess() {
  document.querySelector(`${formBtnBox}`).classList.add('success');
  toggleButton(checkButton);
  enableButton(nextButton);
}

function formFail() {
  document.querySelector(`${formBtnBox}`).classList.add('error');
  disableButton(checkButton);
  enableButton(reviewButton);
}
