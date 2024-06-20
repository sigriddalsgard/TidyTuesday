---
title: The Great American Coffee Taste Test
theme: [light, alt]
toc: false
---

# The Great American Coffee Taste Test

<div class='card'>

```js
import embed from 'npm:vega-embed'

import { Legend } from '../../components/legend.js'
```

```js
let data = await FileAttachment('coffee_survey.csv').csv({ typed: true })

data = data
  .filter(d => d.age !== 'NA' && d.brew !== 'NA' && d.gender !== 'NA' && d.cups !== 'NA')
  .flatMap(d => {
    d.age = d.age.replace(' years old', '')

    d.cups = d.cups === 'More than 4' ? '>4' : d.cups === 'Less than 1' ? '<1' : String(d.cups)

    d.brew = d.brew
      .replace(' (e.g. Mr. Coffee)', '')
      .replace(' (e.g. Keurig/Nespresso)', '')
      .replace(' (e.g. Cometeer)', '')

    return d.brew.split(/,\s*/).map(brew => {
      return { ...d, brew }
    })
  })
```

```js
const brews = d3.group(data, d => d.brew)
```

```js
const rects = Array.from(brews.keys()).map((brew, i) => {
  i += 2

  return {
    brew,
    row: Math.floor(i / 4),
    col: i % 4
  }
})
```

```js
const height = 800
const marginTop = 30
const marginRight = 30
const marginBottom = 30
const marginLeft = 30
const rectWidth = width / 2 / 2
const rectHeight = height / 3
const centerCircleRadius = 50
const centerX = rectWidth / 2
const centerY = rectHeight / 2

const svg = d3.create('svg')
  .attr('width', width)
  .attr('height', height)
  .attr('viewBox', [0, 0, width, height])
  .attr("style", "max-width: 100%; height: auto;")
  .style('background-color', '#E4C59E')

const grid = svg
  .selectAll('g')
  .data(rects)
  .join('g')
    .attr('transform', d => `translate(${d.col * rectWidth}, ${d.row * rectHeight})`)

const rect = grid
  .append(d => {
    const data = brews.get(d.brew)

    const g = d3.create('svg:g')

    const ages = d3.rollup(data,
      D => d3.rollup(D, v => v.length, d => d.cups),
      d => d.age
    )
    debugger

//    const genders = d3.group(data, d => d.gender)
    const genders = [
      'Other',
      'Prefer not to say',
      'Non-binary',
      'Female',
      'Male'
    ]

    const centerCircle = g.append('g')
      .append('circle')
      .attr('cx', centerX)
      .attr('cy', centerY)
      .attr('r', centerCircleRadius)
      .style('fill', '#322C2B')

//    const cups = d3.group(data, d => d.cups)

    const angleStep = (2 * Math.PI) / genders.length

    const angleScale = d3.scaleOrdinal()
      .domain(genders)
      .range(genders.map((_, i) => i * angleStep)); 

    const radiusScale = d3.scaleOrdinal()
      .domain([...ages.keys()])
      .range([0, 100])

    data.forEach(d => {
      svg.append('line')
        .attr('x1', 0)  // Start at the center
        .attr('y1', 0)
        .attr('x2', d => radiusScale(d.ages) * Math.cos(angleScale(d.gender)))  // End point coordinates
        .attr('y2', d => radiusScale(d.ages) * Math.sin(angleScale(d.gender)))
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 2);
    });
//    const line = d3.lineRadial().angle((d) => a(d.genders));

//    const numberOfCups = [...ages].flatMap(innerMap => [...innerMap.values()])

    
//    const x = d3.scaleBand()
//      .domain([...ages.keys()].sort(compareAges))
//      .range([0, rectWidth - marginLeft])
//      .paddingInner(0.1)

//    const xGender = d3.scaleBand()
//      .domain(genders)
//      .rangeRound([0, x.bandwidth()])
//      .padding(0.05)

//    const y = d3.scaleBand()
//      .domain(genders)
//      .range([marginTop, rectHeight - marginBottom])


//    const z = d3.scaleLinear()
//      .domain([0, ])

//    const xAxis = g.append('g')
//      .attr("transform", `translate(${marginLeft},${rectHeight- marginBottom})`)
//      .call(d3.axisBottom(x))
//      .style('opacity', 0.6)

//    const yAxis = g.append('g')
//      .attr('transform', `translate(${marginLeft}, 0)`)
//      .call(d3.axisLeft(y))
//      .style('opacity', 0.6)

//    const color = d3.scaleOrdinal()
//      .domain(genders)
//      .range(d3.schemeSet1)

//    const groups = g.append('g')
//      .selectAll()
//      .data(ages)
//      .join('g')
//        .attr('transform', ([ages, cups]) => `translate(${x(ages) + marginLeft}, ${y(cups) + marginBottom + 4})`)
//        .append('rect')
//          .attr('x', 0)
//          .attr('y', 0)
//          .attr('width', x.bandwidth())
//          .attr('height', ([, d]) => y('<1') - y(d))
//          .attr('fill', d => color(d.genders))

    const headlines = g.append('g')
      .append('text')
      .attr('x', rectWidth/2)
      .attr('y', rectHeight/2)
      .attr('text-anchor', 'middle')
      .style('fill', '#E4C59E')
      .text(d.brew)

    function compareCups (a, b) {
      a = a === '>4' ? 5 : a === '<1' ? 0 : +a
      b = b === '>4' ? 5 : b === '<1' ? 0 : +b

      return b - a
    }

    function compareAges (a, b) {
      a = a === '>65' ? 66 : a === '<18' ? 0 : parseInt(a, 10)
      b = b === '>65' ? 66 : b === '<18' ? 0 : parseInt(b, 10)

      return a - b
    }

    return g.node()
  })

const chart = svg.node()
```

  <div>${chart}</div>
</div>
