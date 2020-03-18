/**
 * Copyright (c) 2010 Maxim Vasiliev
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * @author Maxim Vasiliev
 * Date: 09.09.2010
 * Time: 19:02:33
 */


(function (root, factory)
{
  if (typeof exports !== 'undefined' && typeof module !== 'undefined' && module.exports) {
    // NodeJS
    module.exports = factory();
  }
  else if (typeof define === 'function' && define.amd)
  {
    // AMD. Register as an anonymous module.
    define(factory);
  }
  else
  {
    // Browser globals
    root.form2js = factory();
  }
}(this, function ()
{
  "use strict";

  /**
   * Returns form values represented as Javascript object
   * "name" attribute defines structure of resulting object
   *
   * @param rootNode {Element|String} root form element (or it's id) or array of root elements
   * @param delimiter {String} structure parts delimiter defaults to '.'
   * @param skipEmpty {Boolean} should skip empty text values, defaults to true
   * @param nodeCallback {Function} custom function to get node value
   * @param useIdIfEmptyName {Boolean} if true value of id attribute of field will be used if name of field is empty
   */
  function form2js(rootNode, delimiter, skipEmpty, nodeCallback, useIdIfEmptyName, getDisabled)
  {
    getDisabled = getDisabled ? true : false;
    if (typeof skipEmpty == 'undefined' || skipEmpty == null) skipEmpty = true;
    if (typeof delimiter == 'undefined' || delimiter == null) delimiter = '.';
    if (arguments.length < 5) useIdIfEmptyName = false;

    rootNode = typeof rootNode == 'string' ? document.getElementById(rootNode) : rootNode;

    var formValues = [],
      currNode,
      i = 0;

    /* If rootNode is array - combine values */
    if (rootNode.constructor == Array || (typeof NodeList != "undefined" && rootNode.constructor == NodeList))
    {
      while(currNode = rootNode[i++])
      {
        formValues = formValues.concat(getFormValues(currNode, nodeCallback, useIdIfEmptyName, getDisabled));
      }
    }
    else
    {
      formValues = getFormValues(rootNode, nodeCallback, useIdIfEmptyName, getDisabled);
    }

    return processNameValues(formValues, skipEmpty, delimiter);
  }

  /**
   * Processes collection of { name: 'name', value: 'value' } objects.
   * @param nameValues
   * @param skipEmpty if true skips elements with value == '' or value == null
   * @param delimiter
   */
  function processNameValues(nameValues, skipEmpty, delimiter)
  {
    var result = {},
      arrays = {},
      i, j, k, l,
      value,
      nameParts,
      currResult,
      arrNameFull,
      arrName,
      arrIdx,
      namePart,
      name,
      _nameParts;

    for (i = 0; i < nameValues.length; i++)
    {
      value = nameValues[i].value;

      if (skipEmpty && (value === '' || value === null)) continue;

      name = nameValues[i].name;
      _nameParts = name.split(delimiter);
      nameParts = [];
      currResult = result;
      arrNameFull = '';

      for(j = 0; j < _nameParts.length; j++)
      {
        namePart = _nameParts[j].split('][');
        if (namePart.length > 1)
        {
          for(k = 0; k < namePart.length; k++)
          {
            if (k == 0)
            {
              namePart[k] = namePart[k] + ']';
            }
            else if (k == namePart.length - 1)
            {
              namePart[k] = '[' + namePart[k];
            }
            else
            {
              namePart[k] = '[' + namePart[k] + ']';
            }

            arrIdx = namePart[k].match(/([a-z_]+)?\[([a-z_][a-z0-9_]+?)\]/i);
            if (arrIdx)
            {
              for(l = 1; l < arrIdx.length; l++)
              {
                if (arrIdx[l]) nameParts.push(arrIdx[l]);
              }
            }
            else{
              nameParts.push(namePart[k]);
            }
          }
        }
        else
          nameParts = nameParts.concat(namePart);
      }

      for (j = 0; j < nameParts.length; j++)
      {
        namePart = nameParts[j];

        if (namePart.indexOf('[]') > -1 && j == nameParts.length - 1)
        {
          arrName = namePart.substr(0, namePart.indexOf('['));
          arrNameFull += arrName;

          if (!currResult[arrName]) currResult[arrName] = [];
          currResult[arrName].push(value);
        }
        else if (namePart.indexOf('[') > -1)
        {
          arrName = namePart.substr(0, namePart.indexOf('['));
          arrIdx = namePart.replace(/(^([a-z_]+)?\[)|(\]$)/gi, '');

          /* Unique array name */
          arrNameFull += '_' + arrName + '_' + arrIdx;

          /*
           * Because arrIdx in field name can be not zero-based and step can be
           * other than 1, we can't use them in target array directly.
           * Instead we're making a hash where key is arrIdx and value is a reference to
           * added array element
           */

          if (!arrays[arrNameFull]) arrays[arrNameFull] = {};
          if (arrName != '' && !currResult[arrName]) currResult[arrName] = [];

          if (j == nameParts.length - 1)
          {
            if (arrName == '')
            {
              currResult.push(value);
              arrays[arrNameFull][arrIdx] = currResult[currResult.length - 1];
            }
            else
            {
              currResult[arrName].push(value);
              arrays[arrNameFull][arrIdx] = currResult[arrName][currResult[arrName].length - 1];
            }
          }
          else
          {
            if (!arrays[arrNameFull][arrIdx])
            {
              if ((/^[0-9a-z_]+\[?/i).test(nameParts[j+1])) currResult[arrName].push({});
              else currResult[arrName].push([]);

              arrays[arrNameFull][arrIdx] = currResult[arrName][currResult[arrName].length - 1];
            }
          }

          currResult = arrays[arrNameFull][arrIdx];
        }
        else
        {
          arrNameFull += namePart;

          if (j < nameParts.length - 1) /* Not the last part of name - means object */
          {
            if (!currResult[namePart]) currResult[namePart] = {};
            currResult = currResult[namePart];
          }
          else
          {
            currResult[namePart] = value;
          }
        }
      }
    }

    return result;
  }

    function getFormValues(rootNode, nodeCallback, useIdIfEmptyName, getDisabled)
    {
        var result = extractNodeValues(rootNode, nodeCallback, useIdIfEmptyName, getDisabled);
        return result.length > 0 ? result : getSubFormValues(rootNode, nodeCallback, useIdIfEmptyName, getDisabled);
    }

    function getSubFormValues(rootNode, nodeCallback, useIdIfEmptyName, getDisabled)
  {
    var result = [],
      currentNode = rootNode.firstChild;

    while (currentNode)
    {
      result = result.concat(extractNodeValues(currentNode, nodeCallback, useIdIfEmptyName, getDisabled));
      currentNode = currentNode.nextSibling;
    }

    return result;
  }

    function extractNodeValues(node, nodeCallback, useIdIfEmptyName, getDisabled) {
        if (node.disabled && !getDisabled) return [];

        var callbackResult, fieldValue, result, fieldName = getFieldName(node, useIdIfEmptyName);

        callbackResult = nodeCallback && nodeCallback(node);

        if (callbackResult && callbackResult.name) {
            result = [callbackResult];
        }
        else if (fieldName != '' && node.nodeName.match(/INPUT|TEXTAREA/i)) {
            fieldValue = getFieldValue(node, getDisabled);
            if (null === fieldValue) {
                result = [];
            } else {
                result = [ { name: fieldName, value: fieldValue} ];
            }
        }
        else if (fieldName != '' && node.nodeName.match(/SELECT/i)) {
          fieldValue = getFieldValue(node, getDisabled);
          result = [ { name: fieldName.replace(/\[\]$/, ''), value: fieldValue } ];
        }
        else {
            result = getSubFormValues(node, nodeCallback, useIdIfEmptyName, getDisabled);
        }

        return result;
    }

  function getFieldName(node, useIdIfEmptyName)
  {
    if (node.name && node.name != '') return node.name;
    else if (useIdIfEmptyName && node.id && node.id != '') return node.id;
    else return '';
  }


  function getFieldValue(fieldNode, getDisabled)
  {
    if (fieldNode.disabled && !getDisabled) return null;

    switch (fieldNode.nodeName) {
      case 'INPUT':
      case 'TEXTAREA':
        switch (fieldNode.type.toLowerCase()) {
          case 'radio':
      if (fieldNode.checked && fieldNode.value === "false") return false;
          case 'checkbox':
                        if (fieldNode.checked && fieldNode.value === "true") return true;
                        if (!fieldNode.checked && fieldNode.value === "true") return false;
      if (fieldNode.checked) return fieldNode.value;
            break;

          case 'button':
          case 'reset':
          case 'submit':
          case 'image':
            return '';
            break;

          default:
            return fieldNode.value;
            break;
        }
        break;

      case 'SELECT':
        return getSelectedOptionValue(fieldNode);
        break;

      default:
        break;
    }

    return null;
  }

  function getSelectedOptionValue(selectNode)
  {
    var multiple = selectNode.multiple,
      result = [],
      options,
      i, l;

    if (!multiple) return selectNode.value;

    for (options = selectNode.getElementsByTagName("option"), i = 0, l = options.length; i < l; i++)
    {
      if (options[i].selected) result.push(options[i].value);
    }

    return result;
  }

  return form2js;

}));



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

(function(window){
  window.htmlentities = {
    encode : function(str) {
      var buf = [];

      for (var i=str.length-1;i>=0;i--) {
        buf.unshift(['&#', str[i].charCodeAt(), ';'].join(''));
      }

      return buf.join('');
    },
    decode : function(str) {
      return str.replace(/&#(\d+);/g, function(match, dec) {
        return String.fromCharCode(dec);
      });
    }
  };
})(window);

function reset_form_fields(){
  var fields = document.querySelectorAll('.form-check-input');

  for (field of fields) {
    if (field.checked === true) {
      field.checked = false;
    }
  }
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

function toggleButton(node) {
  if (typeof node === 'string') {
    document.querySelector(node).classList.toggle('disabled');
  } else {
    node.classList.toggle('disabled');
  }
}

function checkForm(){
  var reports = {};
  var box_good_class = 'success';
  var box_warn_class = 'error';
  var msg_good_class = 'show-success';
  var msg_warn_class = 'show-hint';

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
    var box_class = reports[field] ? box_good_class : box_warn_class;
    var msg_class = reports[field] ? msg_good_class : msg_warn_class;
    document.querySelector(`#id_${field}`).classList.add(box_class);
    document.querySelector(`#id_${field}_message`).classList.add(msg_class);

  }

  if (errors.length > 0) {
    window.formFail();
    return "failed"

  } else {
    window.formSuccess();
    return true;
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
  var form_messages = document.querySelector(`${formBtnBox}`);
  form_messages.classList.add('success');
  toggleButton(checkButton);
  enableButton(nextButton);
}

function formFail() {
  var form_messages = document.querySelector(`${formBtnBox}`);
  form_messages.classList.add('error');
  disableButton(checkButton);
  if (CAN_REVIEW == 'True') {
    enableButton(reviewButton);
  } else {
    enableButton(nextButton);
  }
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
