
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
