---
title: Objects Launched into Space
theme: [light, alt]
toc: false
---

# Objects Launched into Space

```js
const data = await FileAttachment('outer_space_objects.csv').csv({ typed: true })

const chartA = resize(width => {

  const height = 390
  const marginTop = 20
  const marginRight = 30
  const marginBottom = 30
  const marginLeft = 40

  const xAxis = d3.scaleLinear()
    .domain(d3.extent(data, d => d.Year))
    .range([marginLeft, width - marginRight])

  const yAxis = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.num_objects)])
    .range([height - marginBottom, marginTop])

  const svg = d3.create('svg')
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto;")

  const gx = svg.append('g')
    .attr("transform", `translate(0,${height - marginBottom})`)
    .call(d3.axisBottom(xAxis)
      .ticks(5)
      .tickFormat(d => d3.format('d')(d)))
    .call(g => g.selectAll('.tick text')
      .attr('font-family', 'Lato, "Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif')
      .attr('fill', 'rgb(91, 91, 91)')
      .attr('font-size', '13.5px'))
    .call(g => g.append("text")
      .attr("x", width)
      .attr("y", marginBottom)
      .attr("fill", "currentColor")
      .attr("text-anchor", "end")
      .text("Year"))

  const line = d3.line(
    (d) => xAxis(d.Year),
    (d) => yAxis(d.num_objects)
  )
    
  const gy = svg.append('g')
    .attr('transform', `translate(${marginLeft},0)`)
    .call(d3.axisLeft(yAxis)
      .ticks(5)
      .tickSize(0))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll('.tick text')
      .attr('font-family', 'Lato, "Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif')
      .attr('fill', 'rgb(91, 91, 91)')
      .attr('font-size', '13.5px'))
    .call(g => g.selectAll('.tick line')
      .clone()
      .attr('x2', width - marginLeft - marginRight)
      .attr('stroke-opacity', 0.1)
      .attr('stroke-dasharray', '4, 2'))
    .call(g => g.append("text")
        .attr("x", -marginLeft)
        .attr("y", 10)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .text("Number of objects"))

  const colors = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"]

  const colorScale = d3.scaleOrdinal()
    .domain(data.map(d => d.Entity))
    .range(colors)

  const entities = d3.group(data, (d) => d.Entity)

  for (const [entity, data] of entities) {
    const g = svg.append('g')

    const dot = g.append('g')
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 0.5)
      .selectAll('circle')
      .data(data)
      .join('circle')
        .attr('transform', d => `translate(${xAxis(d.Year)}, ${yAxis(d.num_objects)})`)
        .attr('r', 2)
        .attr('fill', d => colorScale(d.Entity))

    const path = d3.path(data)

    const lines = g.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', ([d]) => colorScale(d.Entity))
      .attr('d', line)

  }

  const groupedData = d3.group(data, d => d.Entity, d => d.Year);

  const serie = svg.append("g")
    .attr('font-family', 'Lato, "Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif')
  .selectAll("g")
  .data(data)
  .join("g")

  serie.append("text")
    .datum(d => ({ Entity: d.Entity, Year: d.Year, num_objects: d.num_objects }))
    .attr("fill", d => colorScale(d.Entity))
    .attr("paint-order", "stroke")
    .attr("stroke", "white")
    .attr("stroke-width", 3)
    .attr("x", xAxis.range()[1] + 3)
    .attr("y", d => yAxis(d.num_objects))
    .attr("dy", "0.35em")
    .text(d => d.Entity);

  return svg.node()
})
```

```js
const data = await FileAttachment('outer_space_objects.csv').csv({ typed: true })

const chartB = resize(width => {

  const height = 390
  const marginTop = 20
  const marginRight = 30
  const marginBottom = 30
  const marginLeft = 40

  const groupedYear = d3.rollups(
    data,
    values => d3.sum(values, d => d.num_objects),
    d => d.Year
  )

  groupedYear.sort((a, b) => a[0] - b[0])

  const cumsum = d3.zip(groupedYear, d3.cumsum(groupedYear, d => d[1]))
  console.log(cumsum)


  const percentages = []

  for (let i = 1; i < cumsum.length; i++) {
    const current = cumsum[i][1]
    const previous = cumsum[i - 1][1]

    const difference = current - previous
    const percentage = difference / current * 100
    console.log(percentage)
  }


  const xAxis = d3.scaleLinear()
    .domain(d3.extent(data, d => d.Year))
    .range([marginLeft, width - marginRight])

  const yAxis = d3.scaleLinear()
    .domain([0, d3.max(cumsum, d => d[1])])
    .range([height - marginBottom, marginTop])

  const svg = d3.create('svg')
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto;")

  const gx = svg.append('g')
    .attr("transform", `translate(0,${height - marginBottom})`)
    .call(d3.axisBottom(xAxis)
      .ticks(5)
      .tickFormat(d => d3.format('d')(d)))
    .call(g => g.select('.domain').remove())
    .call(g => g.selectAll('.tick text')
      .attr('font-family', 'Lato, "Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif')
      .attr('fill', 'rgb(91, 91, 91)')
      .attr('font-size', '13.5px'))
    .call(g => g.append("text")
      .attr("x", width)
      .attr("y", marginBottom)
      .attr("fill", "currentColor")
      .attr("text-anchor", "end")
      .text("Year"))

  const gy = svg.append('g')
    .attr('transform', `translate(${marginLeft},0)`)
    .call(d3.axisLeft(yAxis)
      .ticks(5)
      .tickSize(0))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll('.tick text')
      .attr('font-family', 'Lato, "Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif')
      .attr('fill', 'rgb(91, 91, 91)')
      .attr('font-size', '13.5px'))
    .call(g => g.selectAll('.tick line')
      .clone()
      .attr('x2', width - marginLeft - marginRight)
      .attr('stroke-opacity', 0.1)
      .attr('stroke-dasharray', '4, 2'))
    .call(g => g.append("text")
        .attr("x", -marginLeft)
        .attr("y", 10)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .text("Number of objects - Cummulative sum"))

  const line = d3.line()
      .curve(d3.curveCardinal.tension(0.5))
      .x(d => xAxis(d[0][0])) // Brug den første indgang som x-koordinat
      .y(d => yAxis(d[1]))

  const path = d3.path(data)

  const g = svg.append('g')
    .append('path')
    .datum(cumsum)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 2)
    .attr("d", line)

  const firstYearsByEntity = d3.rollups(data, 
    entities => d3.min(entities, d => d.Year), // Find det første år for hver enhed
    d => d.Entity // Gruppér efter enhed
  )

  const dots = svg.selectAll('circle')
    .data(cumsum)
    .enter().append("circle")
      .attr("cx", d => xAxis(d[0][0]))
      .attr("cy", d => yAxis(d[1]))
      .attr("r", 3) // Juster størrelsen på punkterne efter behov
      .attr("fill", "none")
      .attr('stroke', 'steelblue')
      .attr('transform', 'translate(0, 0)')
      .on('mouseover', mouseovered)
      .on('mouseout', mouseouted)

  function mouseovered(event, d) {
    d3.select(this)
    .transition()
    .duration(200)
    .attr("r", 5)
  }

  function mouseouted(event, d) {
    d3.select(this)
      .transition()
      .duration(200)
      .attr("r", 3)
  }

  return svg.node()
})
```

<div class='grid'>
  <div class='card'>
${chartA}
  </div>
  <div class='card'>
${chartB}
  </div>
</div>

<p>
These two charts were the first D3.js chart's I ever made. The first one was just an attempt to copy the original: <a href=''> Yearly number of objects launched into outer space </a>. I got stuck with the labels - as you can see. Then I tried to answer the question: 'What years saw the biggest increase in space object launches?' by making the next chart, where I took the total sum of all objects each year.

I had an idea of making these charts interactive. But because of my newbie-state I focused on just making something than get stuck for weeks doing the interactive part. So I moved forward to the next week of #TidyTuesday.
</p>
