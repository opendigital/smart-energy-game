console.log('charts 3');

// VISUAL GAME CHARTS
function drawProximityChart(oldContributions, newContributions, userID, randomArray, roundNumber) {
  // need previous round's offsets
  renderOldPoints(oldContributions, userID, randomArray, roundNumber - 1);
  movePoints(newContributions, userID, randomArray, roundNumber);
}


function movePoints(newContributions, userID, randomArray, roundNumber) {
  console.log(randomArray);
  console.log("below is roundNumber");
  console.log(roundNumber);
  let contributionObjects = {};

  for (let i = 0; i < newContributions.length; ++i) {
    if (contributionObjects[newContributions[i]] != undefined) {
      ++contributionObjects[newContributions[i]].count;
    } else {
      contributionObjects[newContributions[i]] = {
        value: newContributions[i],
        count: 1
      };
    }
  }

  let allPoints = [];

  let pointScale = d3.scaleLinear()
  .domain([0, numPlayers])
  .range([pointRadius, (2 * numPlayers + 1) * pointRadius])

  newContributions.forEach((value, index) => {
    let instance = 0; // if this is the third instance of "value" in the array this will be 3
    for (let i = index; i >= 0; --i) {
      if (newContributions[i] == value) {
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


function renderOldPoints(oldContributions, userID, randomArray, roundNumber) {
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
    let instance = 0; // if this is the third instance of "value" in the array this will be 3
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

  // plot points
  let maxOffset = 3;
  let visibleRadius = pointRadius - maxOffset;
  svg.selectAll("point")
  .data(allPoints)
  .enter()
  .append("circle")
  .attr("class", "point")
  .attr("transform", function (d, i) {

    // if (randomArray[roundNumber] == undefined) {
    //     console.log("randomArray[roundNumber] broke");
    //     console.log("roundNumber = " + roundNumber);
    //     console.log(randomArray);
    //     console.log(randomArray[roundNumber]);
    // }
    console.log("before calcing offsets");
    console.log(roundNumber);

    let xOffset;
    let yOffset;

    if (roundNumber < 0) {
      xOffset = yOffset = 0;
    } else {
      xOffset = (roundNumber < 0) ? 0 : randomArray[roundNumber][i][0];
      yOffset = (roundNumber < 0) ? 0 : randomArray[roundNumber][i][0]; randomArray[roundNumber][i][1];
    }

    console.log("after calcing offsets");
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
  .attr("r", visibleRadius)
  .attr("fill", function (d, i) {
    let is_user = i === userID;
    return is_user ? userColor : othersColor;
  })
}
