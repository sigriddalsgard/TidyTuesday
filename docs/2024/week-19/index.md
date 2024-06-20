---
title: Objects Launched into Space
theme: [light, alt]
toc: false
---

# Rolling Stone Album Rankings

<style>
text {
  font-family: Arial, Helvetica;
  opacity: 0.8;
}

image {
  opacity: 0.8;
}

rect {
  opacity: 0.8;
}

</style>

```js
import { Legend } from '../../components/legend.js'
```

```js
const data = FileAttachment('rolling_stone.csv').csv({ typed: true })
```

```js
const image = FileAttachment('asfalt-dark.png').url()
```

```js
const row = data.find(d => d.genre === 'Blues/Blues ROck')
row.genre = 'Blues/Blues Rock'
```

```js
data.sort((a, b) => b.release_year - a.release_year);
```

```js
const years = d3.range(...d3.extent(data, d => d.release_year))
```

```js
const groups = d3.group(data, d => d.genre, d => d.release_year)
```

```js
const genres = [
  "Afrobeat",
  "Rock n' Roll/Rhythm & Blues",
  "Big Band/Jazz",
  "Reggae",
  "Funk/Disco",
  "Hard Rock/Metal",
  "Singer-Songwriter/Heartland Rock",
  "Blues/Blues Rock",
  "Punk/Post-Punk/New Wave/Power Pop",
  "Electronic",
  "Latin",
  "Country/Folk/Country Rock/Folk Rock",
  "Indie/Alternative Rock",
  "Soul/Gospel/R&B",
  "Hip-Hop/Rap"
]
```

```js
const values = genres.map(genre => years.map(year => {
  const albums = groups.get(genre).get(year) || null
  if (albums === null) return 0
  return d3.sum(albums, d => d.weeks_on_billboard || 0)
}))
```

<div class='card'>

```js
const marginTop = 20
const marginRight = 30
const marginBottom = 50
const marginLeft = 200
const rowHeight = 16;
const height = rowHeight * genres.length + marginTop + marginBottom;

const svg = d3.create('svg')
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", [0, 0, width, height])
  .attr("style", "display: block; max-width: 100%; height: auto;")   
  .style('background-color', 'rgb(227, 226, 206)')
  .style('background-image', `url(${image})`)

const x = d3.scaleLinear()
  .domain(d3.extent(years))
  .rangeRound([marginLeft, width - marginRight])

const y = d3.scaleBand()
  .domain(genres)
  .rangeRound([marginTop, height - marginBottom])

const color = d3.scaleSequentialSqrt([0, d3.max(values, d => d3.max(d))], d3.interpolateOranges);

const xAxis = svg.append('g')
  .call(g => g.append('g')
    .attr("transform", `translate(0,${marginTop})`)
      .call(d3.axisTop(x).ticks(null, "d"))
      .call(g => g.select(".domain").remove()))

const yAxis = svg.append('g')
  .attr('transform', `translate(${marginLeft}, 0)`)
  .call(d3.axisLeft(y).tickSize(0))
  .call(g => g.select(".domain").remove());

const rect = svg.append("g")
  .selectAll("g")
  .data(values)
  .join("g")
    .attr("transform", (d, i) => `translate(0,${y(genres[i])})`)
  .selectAll('rect')
  .data(d => d)
  .join('rect')
    .attr("x", (d, i) => x(years[i]) + 1)
    .attr("width", (d, i) => x(years[i] + 1) - x(years[i]) - 1)
    .attr("height", y.bandwidth() - 1)
    .attr("fill", d => d === 0 ? "rgba(0,0,0,.1)" : color(d))

const legend = svg.append("g")
  .attr("transform", "translate(878,260)")
  .append(() => Legend(color, {width: 260}))

const headline = svg.append('g')
  .append('text')
  .attr('y', 295)
  .attr('x', 199)
  .style('font-size', 'xx-large')
  .style('font-weight', 900)
  .style('opacity', 0.8)
  .style('letter-spacing', '-3px')
  .text("Rolling Stone's Billboard List")

const weekText = svg.append('g')
  .append('text')
  .attr('y', 274)
  .attr('x', 876)
  .text('Total weeks:')

const chartA = svg.node()
```
  <div>${chartA}</div>
</div>
