---
title: Worldwide Bureaaucracy Indicators
theme: [light, alt]
toc: false
---

<link href="https://fonts.googleapis.com/css?family=Abril+Fatface&display=swap" rel="stylesheet">

# Worldwide Bureaucracy Indicators

```js
import { Legend } from '../../components/legend.js'
import { Scrubber } from '../../components/scrubber.js'
```

```js
const data = FileAttachment('filtered_data.csv').csv({ typed: true })
const world =  FileAttachment('countries-50m.json').json()
```

```js
data.sort((a, b) => b.value - a.value);
data.sort((a, b) => a.year - b.year);
```

<div class='card'>

```js
const height = 200
const marginTop = 20
const marginRight = 30
const marginBottom = 30
const marginLeft = 150

const x = d3.scaleLinear()
  .domain(d3.extent(data, d => d.value))
  .range([marginLeft, width - marginRight])

const countries = Array.from(new Set(data.map(d => d.short_name)))

const y = d3.scaleBand()
  .domain(countries)
  .range([height - marginBottom, marginTop])
  .paddingInner(0.1)

const svg = d3.create('svg')
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", [0, 0, width, height])
  .attr("style", "max-width: 100%; height: auto;")

const xAxis = svg.append('g')
  .attr("transform", `translate(0,${height - marginBottom})`)
  .call(d3.axisBottom(x))
    //.tickFormat(d => d3.format('d')(d)))

const yAxis = svg.append('g')
  .attr('transform', `translate(${marginLeft},0)`)
  .call(d3.axisLeft(y))
    //.ticks(10)
  .call(g => g.select(".domain").remove())

svg.append('g')
    .attr('fill', 'steelblue')
  .selectAll()
  .data(data)
  .join('rect')
    .attr('x', marginLeft)
    .attr('y', (d) => y(d.short_name))
    .attr('height', y.bandwidth())
    .attr('width', (d) => x(d.value) - marginLeft)

//const dot = svg.append('g')
//  .selectAll('circle')
//  .data(data)
//  .enter()
 // .append('circle')
  //  .attr('cx', d => x(d.value))
  //  .attr('cy', d => y(d.year))
  //  .attr('r', 3)
  //  .attr('fill', 'none')
  //  .attr('stroke', 'red')
  //  .attr('stroke-width', 2)

const chartA = svg.node()
```

<div>${chartA}</div>

</div>

<div class='card'>

```js
const countries = topojson.feature(world, world.objects.countries)

const countrymesh = topojson.mesh(world, world.objects.countries, (a, b) => a !== b)

const filteredCountries = countries.features.filter(d => d.properties.name !== "Antarctica")

const candidates = new Map()

for (const d of data) {
  if (d.year > year) continue
  let closest = candidates.get(d.short_name) || d
  if (d.year > closest.year) closest = d
  candidates.set(d.short_name, closest)
}

const dataForCurrentYear = [...candidates.values()]

const dataByShortname = new Map(dataForCurrentYear.map(d => [d.short_name, d.value]))

const dataByCountry = d3.group(dataForCurrentYear, d => d.short_name)

const height = 600
const marginTop = 20
const marginRight = 30
const marginBottom = 30
const marginLeft = 150

const projection = d3.geoNaturalEarth1()
  .center([10, 20])
  .scale(210)
  .translate([width / 2, height / 2])

const path = d3.geoPath(projection)

const color = d3.scaleSequentialLog(d3.extent(dataByShortname, d => d[1]), d3.interpolateYlGn)

const svg = d3.create('svg')
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", [0, 0, width, height])
  .attr("style", "display: block; max-width: 100%; height: auto;")  
  .style('background-color', 'rgb(110, 210, 231)')

svg.append('g')
  .selectAll('path')
  .data(filteredCountries)
  .join("path")
    .attr("fill", d => {
      const value = dataByShortname.get(d.properties.name)
      if (value === undefined) {
        //console.error(d.properties.name + ' is missing')
        return 'rgb(246, 246, 246)'
      }
      return color(value)
    })
    .attr("d", path)

svg.append('g').append("path")
    .datum(countrymesh)
    .attr("fill", "none")
    .attr("stroke", "rgb(246, 246, 246)")
    .attr('stroke-width', 0.4)
    .attr("d", path)

const legend = svg.append("g")
  .attr("transform", "translate(10,580) rotate(-90)")
  .append(() => Legend(color, {width: 260}))

legend.selectAll('text')
  .attr('transform', 'translate(13, 10) rotate(90)')
  .attr('text-anchor', 'start')

const headline = svg.append('text')
  .attr('y', 60)
  .attr('x', width/2)
  .attr('text-anchor', 'middle')
  .style('font-family', 'Abril Fatface')
  .style('font-size', '50px')
  .text('Public paid employees')


const chartB = svg.node()
```

<div style="height:578px">${chartB}</div>

```js
// Scrubber

const extent = d3.extent(data, d => d.year)

const numberOfYears = Array.from({length: extent[1] - extent[0] + 1}, (_, i) => i + extent[0])

const scrubber = Scrubber(numberOfYears, {loop: false, delay: 500, autoplay: false})

const year = view(scrubber)
```

<style>
.scrubber {
  padding: 10px 20px;
  background-color: rgb(110, 210, 231);
}

.scrubber form {
  display: flex;
}

.scrubber label {
  flex: 1;
}

.scrubber input {
  flex: 1;
}

.scrubber output {
  font-family: 'Abril Fatface';
  font-weight: 10;
  font-size: 22px;
}

.scrubber button {
  padding: 1px 10px;
  border: 1px solid black;
  border-radius: 50% 20% / 10% 40%;
  background: none;
  color: black;
  font-family: 'Abril Fatface';
  font-size: 22px;
}
</style>

<div class="scrubber">${scrubber}</div>

</div>

<div>
  <p>
    This was my first attempt to make an interactive chart. I had to get help from my husband to make it, but in the end I was actually proud of it. It was also the first #TidyTuesday chart which I showed to others on the Data Science community on Slack.
  </p>
</div>
