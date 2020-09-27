// VISUAL GAME CHARTS

function drawProximityChart({
  previousContributions,
  newContributions,
  userID,
  randomArray,
  roundNumber
}) {

  renderOldProximityPoints(previousContributions, userID, randomArray, roundNumber - 1);
  moveProximityPoints(newContributions, userID, randomArray, roundNumber);
}


function moveProximityPoints(newContributions, userID, randomArray, roundNumber) {
  let contributions = {}
  for (contribution of newContributions) {
    if (!contributions[contribution]) {
      contributions[contribution] = {
        value: contribution,
        count: 1,
      }
    } else {
      contributions[contribution].count += 1
    }
  }

  let allPoints = [];

  let pointScale = d3.scaleLinear()
  .domain([0, numPlayers])
  .range([pointRadius, (2 * numPlayers + 1) * pointRadius])

  newContributions.forEach((value, index) => {
    // if this is the third instance of "value" in the array this will be 3
    let instance = 0;
    for (let i = index; i >= 0; --i) {
      if (newContributions[i] == value) {
        ++instance;
      }
    }

    let pointObject = {
      value: value,
      x: instance
    };

    let count = contributions[value].count;
    let centerValue = numPlayers / 2;

    let centerIndex;
    if (count % 2 == 1) {
      centerIndex = Math.floor(count / 2) + 0.5;
    } else {
      centerIndex = Math.floor(count / 2);
    }

    pointObject.x += (centerValue - centerIndex);
    allPoints.push(pointObject);
  })

  // plot points
  let maxOffset = 3;

  // move points to new positions
  svg.selectAll(".point")
  .data(allPoints)
  .transition()
  .duration(1000)
  .attr("class", "point")
  .attr("transform", function (d, i) {
    // if (randomArray[roundNumber] == undefined) {
    //     console.log("randomArray[roundNumber] broke");
    //     console.log("roundNumber = " + roundNumber);
    //     console.log(randomArray);
    //     console.log(randomArray[roundNumber]);
    // }

    let xOffset;
    let yOffset;

    if (roundNumber < 0) {
      xOffset = yOffset = 0;
    } else {
      xOffset = (roundNumber < 0) ? 0 : randomArray[roundNumber][i][0];
      yOffset = (roundNumber < 0) ? 0 : randomArray[roundNumber][i][0]; randomArray[roundNumber][i][1];
    }

    // if (xOffset == undefined) {
    //     console.log("xOffset broke");
    //     console.log("roundNumber = " + roundNumber + ", i = " + i);
    //     console.log(randomArray);
    //     console.log(randomArray[roundNumber]);
    //     console.log(randomArray[roundNumber][i]);
    //     console.log(randomArray[roundNumber][i][0]);
    // }

    // if (yOffset == undefined) {
    //     console.log("yOffset broke");
    //     console.log("roundNumber = " + roundNumber + ", i = " + i);
    //     console.log(randomArray);
    //     console.log(randomArray[roundNumber]);
    //     console.log(randomArray[roundNumber][i]);
    //     console.log(randomArray[roundNumber][i][1]);
    // }

    let x = pointScale(d.x) + xOffset + padding;
    let y = yScale(d.value) + yOffset + padding;
    return "translate(" + [x, y] + ")";
  })
  .attr("fill", function (d, i) {
    return i === userID ? userColor : othersColor;
  })
}


function renderOldProximityPoints(oldContributions, userID, randomArray, roundNumber) {
  let contributionObjects = {};

  for (let i = 0; i < oldContributions.length; ++i) {
    if (contributionObjects[oldContributions[i]] != undefined) {
      ++contributionObjects[oldContributions[i]].count;
    } else {
      contributionObjects[oldContributions[i]] = {
        value: oldContributions[i],
        count: 1
      };
    }
  }

  let allPoints = [];

  let pointScale = d3.scaleLinear()
  .domain([0, numPlayers])
  .range([pointRadius, (2 * numPlayers + 1) * pointRadius])

  oldContributions.forEach((value, index) => {
    // if this is the third instance of "value" in the array this will be 3
    let instance = 0;
    for (let i = index; i >= 0; --i) {
      if (oldContributions[i] == value) {
        ++instance;
      }
    }

    let pointObject = {
      value: value,
      x: instance
    };

    let count = contributionObjects[value].count;
    let centerValue = numPlayers / 2;

    let centerIndex;
    if (count % 2 == 1) {
      centerIndex = Math.floor(count / 2) + 0.5;
    } else {
      centerIndex = Math.floor(count / 2);
    }

    pointObject.x += (centerValue - centerIndex);
    allPoints.push(pointObject);
  })

  let maxOffset = 3;
  let visibleRadius = pointRadius - maxOffset;

  console.log('round', roundNumber);
  let index = roundNumber - 1;

  svg.selectAll("point")
    .data(allPoints)
    .enter()
    .append("circle")
    .attr("class", "point")
    .attr("transform", function (d, i) {
      let xOffset;
      let yOffset;
      if (index < 0) {
        xOffset = yOffset = 0;
      } else {
        xOffset = (index < 0) ? 0 : randomArray[index][i][0];
        yOffset = (index < 0) ? 0 : randomArray[index][i][1];
      }

      let x = pointScale(d.x) + xOffset + padding;
      let y = yScale(d.value) + yOffset + padding;
    return "translate(" + [x, y] + ")";
  })
  .attr("r", visibleRadius)
  .attr("fill", function (d, i) {
    let is_user = i === userID;
    return is_user ? userColor : othersColor;
  })
}


function renderProximityAxis(yScale) {
    let yAxis = d3.axisLeft()
        .scale(yScale)
        .ticks(5);

    svg.append("g")
        .attr("transform", "translate(" + padding + ", " + padding + ")")
        .call(yAxis);

    svg.append("text")
        .attr("class", "y label")
        .attr("text-anchor", "middle")
        .attr("y", padding / 2)
        .attr("x", -svgHeight / 2)
        .attr("transform", "rotate(-90)")
        .text("Contribution");
}


function getPreviousContributions(userId, count) {
  let defaultValue = 0;
  let previous = JSON.parse(localStorage.getItem("oldData"));

  if (previous == null
    || typeof (previous) != "object"
    || !previous.hasOwnProperty("length")
    || previous.length == 0) {

    previous = [];
    for (let i = 0; i < count - 1; i++) {
      previous.push(defaultValue);
    }

    previous.splice(userId, 0, defaultValue);
  }
  return previous;
}

function initProximityChart({newData, userID, myContribution, randomArray, roundNumber}) {
  let padding = 50;
  let pointRadius = 15;
  let numPlayers = 22;
  let maxContribution = 10;

  let svgWidth = pointRadius * (2 * numPlayers) + 2 * padding;
  let svgHeight = pointRadius * (2 * maxContribution) + 2 * padding;

  let userColor = "#999";
  let othersColor = "#555";

  let svg = d3.select("#chart_container")
      .append("svg")
      .attr("width", svgWidth)
      .attr("height", svgHeight)

  let xScale = d3.scaleLinear()
      .domain([0, numPlayers])
      .range([0, numPlayers * 2 * pointRadius]);

  let yScale = d3.scaleLinear()
      .domain([0, maxContribution])
      .range([2 * maxContribution * pointRadius, 0]);

  renderProximityAxis(yScale);

  if (newData.indexOf(']') > -1) {
    newData = JSON.parse(newData)
  }

  newData.splice(userID, 0, myContribution);

  let oldData = getPreviousContributions(userID, newData.length);

  drawProximityChart({
    previousContributions: oldData,
    newContributions: newData,
    userID: userID,
    randomArray: randomArray,
    roundNumber: roundNumber
  });

  localStorage.removeItem("oldData");
  localStorage.setItem("oldData", JSON.stringify(newData));
}
