# Hunting for Exoplanets Using Machine Learning
---

This is a classifier designed to discover exoplanet-containing stars using only light flux data. The flux data was obtained from [Kaggle](https://www.kaggle.com/keplersmachines/kepler-labelled-time-series-data).

## Slides for the Project  

<iframe src="https://docs.google.com/presentation/d/1pucUKCzdeLy-XIkigfJ3_PBa1bkkxwaXUjpiDN_olYA/embed?start=true&loop=true&delayms=10000" frameborder="0" width="700" height="422" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>  

And here is my Fourier Transform visualization from the slides above. Basically, I took the mean of all frequency spectra for exoplanet-containing stars and for stars without exoplanets and plotted them all together. Where you see orange, there frequencies of stars with no exoplanets dominate. The reverse is true for where you see green: exoplanet-containing stars dominate there.  

<style>

body {
  text-align: center;
  font: 10px sans-serif;
}

.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.x.axis path {
  display: none;
}

.area.above {
  fill: rgb(252,141,89);
}

.area.below {
  fill: rgb(145,207,96);
}

.line {
  fill: none;
  stroke: #000;
  stroke-width: 1.5px;
}

</style>
<body>
<script src="https://d3js.org/d3.v3.min.js"></script>
<script>

var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// var parseDate = d3.time.format("%Y%m%d").parse;

// var x = d3.time.scale()
//     .range([0, width]);

var x = d3.scale.linear()
    .range([0, width])
    .domain([0, 0.8]);

// var y = d3.scale.linear()
//     .range([height, 0]);

var y = d3.scale.linear()
    .range([height, 0])
    .domain([0, 0.1]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.area()
    .interpolate("basis")
    .x(function(d) { return x(d.frequency); })
    .y(function(d) { return y(d["avg.spectrum of stars w/exoplanets"]); });

var area = d3.svg.area()
    .interpolate("basis")
    .x(function(d) { return x(d.frequency); })
    .y1(function(d) { return y(d["avg.spectrum of stars w/exoplanets"]); });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("/data/exoplanet_flux_spectrum.csv", function(error, data) {
  if (error) throw error;

  data.forEach(function(d) {
    d.frequency = d.frequency;
    d["avg.spectrum of stars w/exoplanets"]= +d["avg.spectrum of stars w/exoplanets"];
    d["avg.spectrum of stars w/o exoplanets"] = +d["avg.spectrum of stars w/o exoplanets"];
  });

  x.domain(d3.extent(data, function(d) { return d.frequency; }));

  y.domain([
    d3.min(data, function(d) { return Math.min(d["avg.spectrum of stars w/exoplanets"],
      d["avg.spectrum of stars w/o exoplanets"]); }),
    d3.max(data, function(d) { return Math.max(d["avg.spectrum of stars w/exoplanets"],
      d["avg.spectrum of stars w/o exoplanets"]); })
  ]);

  svg.datum(data);

  svg.append("clipPath")
      .attr("id", "clip-below")
    .append("path")
      .attr("d", area.y0(height));

  svg.append("clipPath")
      .attr("id", "clip-above")
    .append("path")
      .attr("d", area.y0(0));

  svg.append("path")
      .attr("class", "area above")
      .attr("clip-path", "url(#clip-above)")
      .attr("d", area.y0(function(d) { return y(d["avg.spectrum of stars w/o exoplanets"]); }));

  svg.append("path")
      .attr("class", "area below")
      .attr("clip-path", "url(#clip-below)")
      .attr("d", area);

  svg.append("path")
      .attr("class", "line")
      .attr("d", line);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .attr("x", 500)
      .attr("y", 25)
      .attr("dx", ".71em")
      .style("text-anchor", "end")
      .text("Observational Frequency, Hz");;

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Unitless Flux");
});

</script>
</body>
