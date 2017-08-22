# Space Wars! or Star Trek through the Years
---

This is my topic exploration of Star Trek TV series and movies (not including the latest alternative universe Star Trek movies). I was particularly interested in topic distribution through time.

## Presentation Slides for the Project  

<iframe src="https://docs.google.com/presentation/d/1zuFELeFsi3nDDo9JHKE2g3BUCyYsdjZ7GOApei4rPPU/embed?start=true&loop=true&delayms=10000" frameborder="0" width="700" height="422" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>  

## Smoothed D3.js Radar Chart  

<!-- Google fonts -->
<link href='https://fonts.googleapis.com/css?family=Open+Sans:400,300' rel='stylesheet' type='text/css'>
<link href='https://fonts.googleapis.com/css?family=Raleway' rel='stylesheet' type='text/css'>

<!-- D3.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js" charset="utf-8"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3-legend/1.3.0/d3-legend.js" charset="utf-8"></script>

<style>
	body {
		font-family: 'Open Sans', sans-serif;
		font-size: 11px;
		font-weight: 300;
		fill: #242424;
		text-align: center;
		text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff, 0 -1px 0 #fff;
		cursor: default;
	}

	.tooltip {
		fill: #333333;
	}
</style>

<div class="radarChart"></div>

<script src="/data/radarChart.js"></script>
<script>
	//////////////////////////////////////////////////////////////
	//////////////////////// Set-Up //////////////////////////////
	//////////////////////////////////////////////////////////////

	var margin = {top: 100, right: 100, bottom: 100, left: 100},
		legendPosition = {x: 25, y: 25},
		width = Math.min(1000, window.innerWidth - 10) - margin.left - margin.right,
		height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);

	//////////////////////////////////////////////////////////////
	//////////////////// Draw the Chart //////////////////////////
	//////////////////////////////////////////////////////////////

	var color = d3.scale.ordinal()
		.range(["#f20e0e", "#f2970e", "#f2e60e",
						"#a6f20e", "#4bf20e", "#0ef280",
						"#0ef2f2", "#0ea2f2", "#0e38f2",
						"#5e0ef2", "#9e0ef2", "#ea0ef2",
						"#f20e80", "#9752af", "#5277af"]);

						var radarChartOptions = {
						  w: width,
						  h: height,
						  margin: margin,
						  legendPosition: legendPosition,
						  maxValue: 0.5,
						  wrapWidth: 60,
						  levels: 5,
						  roundStrokes: true,
						  color: color,
						  axisName: "reason",
						  areaName: "device",
						  value: "value"
						};

						//Load the data and Call function to draw the Radar chart
						d3.json("/data/space_wars_data.json", function(error, data){
							RadarChart(".radarChart", data, radarChartOptions);
						});

					</script>
