<template>
  <div id="gviz">
    <button @click="testMessage()" right>test me</button>
    <d3-network
      v-if="nodes"
      :net-nodes="nodes"
      :net-links="links"
      :options="options"
    />
  </div>
</template>

<script>
// import * as d3 from "d3"
import D3Network from 'vue-d3-network'
export default {
  name: "gviz",
  props: {},
  components: {
    "d3-network": D3Network
  },
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
      this.nodes = JSON.parse(JSON.stringify(this.parseGraphson(JSON.parse(event.data).result.data)))
      this.links = [
        { 
          id: "1bcb9911-bbbb-aaaa-cccc-1ab8e09f8b8c",
          name: "knows",
          tid: '1bcb9911-b7f9-4916-914b-1ab8e09f8b8c',
          sid: '42e7fe6d-b67f-42b1-a99d-27e1949519f1',
          _color: "black"
        }
        ]
      this.updateSimulation()
    }
  },
  methods: {
    parseGraphson(graphson) {
      return graphson["@value"].map(i => { 
        return {
          id: i["@value"].id["@value"],
          label: i["@value"].label,
          name: "ID: " + i["@value"].id["@value"] + " LABEL: " + i["@value"].label,
          _color: "green",
          x: null,
          y: null,
        }
      })
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
  },
  data() {
    return {
      gremlin_websocket: null,
      nodes: [],
      links: [],
      width: Math.max(document.documentElement.clientWidth, window.innerWidth || 0),
      height: Math.max(document.documentElement.clientHeight, window.innerHeight || 0) - 40,
      options: {
        nodeSize: 35,
        nodeLabels: true,
        linkLabels: true,
        force: 10000
      }
    }
  }
}
</script>

<style scoped>
</style>
