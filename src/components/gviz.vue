<template>
  <div id="gviz">
    {{graph.nodes}}
    <button @click="testMessage()" right>test me</button>
    <svg :width="width+'px'"
        :height="height+'px'"
        @mousemove="drag($event)"
        @mouseup="drop()"
        v-if="bounds.minX">
      <line v-for="(link, linkIndex) in graph.links" :key="linkIndex"
        :x1="coords[link.source.index].x"
        :y1="coords[link.source.index].y"
        :x2="coords[link.target.index].x"
        :y2="coords[link.target.index].y"
        stroke="black" stroke-width="2"/>
      <circle v-for="(node, nodeIndex) in graph.nodes" :key="nodeIndex"
        :cx="coords[nodeIndex].x"
        :cy="coords[nodeIndex].y"
        :r="20"
        :fill="colors[Math.ceil(Math.sqrt(node.index))]"
        stroke="white"
        stroke-width="1"
        @mousedown="currentMove = {x: $event.screenX, y: $event.screenY, node: node}"
      >
      </circle>
      <foreignObject v-for="(node, nodeIndex) in graph.nodes" :key="nodeIndex"
        :x="coords[nodeIndex].x - 150"
        :y="coords[nodeIndex].y - 60"
        :width="300"
        :height="35"
        :fill="colors[Math.ceil(Math.sqrt(node.index))]"
      >
        <div style="color: white; font: 12px serif; height: 100%; overflow: auto; text-align: center">
          <b>id</b>:{{node.id}}
          <br>
          <b>label</b>: {{node.label}}
        </div>
      </foreignObject>
    </svg>
  </div>
</template>

<script>
import * as d3 from "d3"
export default {
  name: "gviz",
  props: {},
  created() {
    // this.updateSimulation()

    this.gremlin_websocket = new WebSocket("ws://127.0.0.1:8182/gremlin")
    this.gremlin_websocket.onopen = (event) => {
      console.log(event)
    }
    this.gremlin_websocket.onerror = (error) => {
      console.log(error)
    }
    this.gremlin_websocket.onmessage = (event) => {
      var vertices = JSON.parse(JSON.stringify(this.parseGraphson(JSON.parse(event.data).result.data)))
      this.graph.nodes = vertices
      this.graph.links = []
      this.updateSimulation()
    }
    // var query = "g.V().elementMap().toList()"
    // var message = JSON.stringify(this.createMessage(query))
    // this.gremlin_websocket.send(message)
    // console.log(this.gremlin_websocket)
  },
  methods: {
    drag(e) {
      if (this.currentMove) {
        this.currentMove.node.fx = this.currentMove.node.x - (this.currentMove.x - e.screenX) * (this.bounds.maxX - this.bounds.minX) / (this.width - 2 * this.padding)
        this.currentMove.node.fy = this.currentMove.node.y -(this.currentMove.y - e.screenY) * (this.bounds.maxY - this.bounds.minY) / (this.height - 2 * this.padding)
        this.currentMove.x = e.screenX
        this.currentMove.y = e.screenY
      }
    },
    drop(){
      if (this.currentMove) {
        delete this.currentMove.node.fx
        delete this.currentMove.node.fy    
        this.currentMove = null
        this.simulation.alpha(1)
        this.simulation.restart()
      }
    },
    parseGraphson(graphson) {
      return graphson["@value"].map(i => { 
        return { 
          id: i["@value"].id["@value"],
          label: i["@value"].label,
          x: null,
          y: null,
        } 
      })
    },
    updateSimulation() {
      this.simulation = d3.forceSimulation(this.graph.nodes)
        .force('center', d3.forceCenter(this.width / 2, this.height / 2))
        .force('collision', d3.forceCollide().radius(10))
        .force('link', d3.forceLink(this.graph.links))
        // .force('x', d3.forceX().x(this.width / 2))
        // .force('y', d3.forceY().y(this.height / 2))
    },
    testMessage() {
      var query = "g.V()"
      var message = JSON.stringify(this.createMessage(query))
      this.gremlin_websocket.send(message)
    },
    createMessage(gremlin_query) {
      return {
        requestId: "df1c2dbb-29d9-4495-afae-db7fa15639f8",
        op: "eval",
        processor: "",
        args: {
          gremlin: gremlin_query,
          bindings: {},
          language: "gremlin-groovy",
        },
      }
    },
  },
  computed: {
    bounds() {
      return {
        minX: Math.min(...this.graph.nodes.map(n => n.x)),
        maxX: Math.max(...this.graph.nodes.map(n => n.x)),
        minY: Math.min(...this.graph.nodes.map(n => n.y)),
        maxY: Math.max(...this.graph.nodes.map(n => n.y))
      }
    },
    coords() {
      return this.graph.nodes.map(node => {
        return {
          x: this.padding + (node.x - this.bounds.minX) * (this.width - 2*this.padding) / (this.bounds.maxX - this.bounds.minX),
          y: this.padding + (node.y - this.bounds.minY) * (this.height - 2*this.padding) / (this.bounds.maxY - this.bounds.minY)
        }
      })
    }
  },
  data() {
    return {
      gremlin_websocket: null,
      graph: {
        nodes: d3.range(100).map(i => ({ index: i, x: null, y: null })),
        links: d3.range(100).map(i => ({ source: i, target: Math.floor(Math.random() * i) }))
      },
      width: Math.max(document.documentElement.clientWidth, window.innerWidth || 0),
      height: Math.max(document.documentElement.clientHeight, window.innerHeight || 0) - 40,
      padding: 100,
      colors: ['#2196F3', '#E91E63', '#7E57C2', '#009688', '#00BCD4', '#EF6C00', '#4CAF50', '#FF9800', '#F44336', '#CDDC39', '#9C27B0'],
      simulation: null,
      currentMove: null,
    }
  }
}
</script>

<style scoped>
/* Tooltip container */
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
}

/* Tooltip text */
.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  padding: 5px 0;
  border-radius: 6px;
 
  /* Position the tooltip text - see examples below! */
  position: absolute;
  z-index: 1;
}

/* Show the tooltip text when you mouse over the tooltip container */
.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
