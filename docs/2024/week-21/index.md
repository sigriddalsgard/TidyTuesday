---
title: Carbon Majors Emissions Data
theme: [light, alt]
toc: false
---

# Carbon Majors Emissions Data

<div class='card'>

```js
import embed from 'npm:vega-embed'
```

```js
const image = await FileAttachment('CO2-image.jpg').url()
```

```js
let data = await FileAttachment('emissions.csv').csv({ typed: true })

data = d3.sort(data, (a, b) => d3.ascending(a.year, b.year))
```

```js
const groups = d3.groups(data, d => d.parent_type)
```

```js
const height = 600
const marginTop = 30
const marginRight = 40
const marginBottom = 30
const marginLeft = 40

const year = [...new Set(data.map(d => d.year))]

const svg = d3.create('svg')
  .attr('width', width)
  .attr('height', height)
  .attr('viewBox', [0, 0, width, height])
  .attr("style", "max-width: 100%; height: auto;")
//  .style('background-image', `url(${image})`)
//  .style('background-size', 'cover')

//svg.append('rect')
//  .attr('width', width)
//  .attr('height', height)
//  .attr('fill', 'white')
//  .attr('opacity', 0.5)

const xTickValues = [1854, 1880, 1900, 1920, 1940, 1960, 1980, 2000, 2022]

const x = d3.scaleLinear()
  .domain(d3.extent(xTickValues))
  .range([marginLeft, width - marginRight])


const xAxis = svg.append("g")
  .attr("transform", `translate(0,${height - marginBottom})`)
  .call(d3.axisBottom(x)
    .ticks()
    .tickSize(3)
    .tickValues(xTickValues)
    .tickFormat(d3.format('d')))
  .select('.domain').remove()

groups.forEach(([title, data], i) => {
  const offset = (height - marginBottom) * i / 3

  const y = d3.scaleSymlog()
    .domain([0, 15000])
    .range([(height - marginBottom) / 3, marginTop])
    .constant(200)

  const plot = svg.append("g")
    .attr("transform", `translate(0, ${offset})`)

  const headline = plot.append('text')
    .attr('x', (width - marginLeft) / 2)
    .attr('y', 20)
    .attr('text-anchor', 'middle')
    .attr('font-family', 'sans-serif')
    .attr('font-size', '14px')
    .attr('font-weight', 'bold')
    .text(title)

  const yTickValues = [0, 50, 100, 500, 1000, 5000, 10000, 15000]

  const yAxis = plot.append('g')
    .attr('transform', `translate(${marginLeft}, 0)`)
    .call(d3.axisLeft(y)
      .tickValues(yTickValues)
      .tickSize(3))

  const xGrid = plot.append('g')
      .attr("stroke", "currentColor")
      .attr("stroke-opacity", 0.1)
      .call(g => g.append("g")
        .selectAll(".tick line")
        .data(xTickValues)
        .join("line")
          .attr("x1", d => x(d))
          .attr("x2", d => x(d))
          .attr("y1", marginTop)
          .attr("y2", (height - marginBottom)/3))

  const yGrid = plot.append('g')
    .attr("stroke", "currentColor")
    .attr("stroke-opacity", 0.1)
    .call(g => g.append("g")
      .selectAll(".tick line")
      .data(yTickValues)
      .join("line")
        .attr("y1", d => y(d))
        .attr("y2", d => y(d))
        .attr("x1", marginLeft)
        .attr("x2", width - marginRight))

  const keys = d3.union(d3.map(data, d => d.commodity))

  const color = d3.scaleOrdinal()
    .domain(keys)
    .range(d3.schemeTableau10)

  const rollup = d3.rollup(data, D => d3.sum(D, d => d.total_emissions_MtCO2e),
    d => d.year,
    d => d.commodity
  )

  const stack = d3.stack()
    .keys(keys)
    .order(d3.stackOrderInsideOut)
    .value(([year, data], commodity) => data.get(commodity))
    ([...rollup])

  const area = d3.area()
    .x(d => x(d.data[0]))
    .y0(d => y(d[0]))
    .y1(d => y(d[1]))

  plot.selectAll("mylayers")
    .data(stack)
    .enter()
    .append("path")
      .style("fill", d => color(d.key))
      .attr("stroke", "black")
      .attr("stroke-opacity", 0.3)
      .attr("d", area)
})

const chart = svg.node()
```
  <div>${chart}</div>
</div>

