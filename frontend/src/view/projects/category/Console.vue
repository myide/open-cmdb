<template>
    <div class="console" style="height:500px; width:1200px" id="terminal"></div>
</template>
<script>
import axios from '@/libs/api.request'
import Terminal from './Xterm'
export default {
  name: 'Console',
  props: {
    terminal: {
      type: Object,
      default: {}
    }
  },
  data () {
    return {
      term: null,
      terminalSocket: null
    }
  },
  methods: {
    runRealTerminal () {
      console.log('webSocket is finished')
    },
    errorRealTerminal () {
      console.log('error')
    },
    closeRealTerminal () {
      console.log('close')
    }
  },
  mounted () {
    let terminalContainer = document.getElementById('terminal')
    this.term = new Terminal()
    this.term.open(terminalContainer)
    // open websocket
    const ws_addr = axios.baseUrl.replace(/http/, 'ws') + '/webssh/?server_id=' + this.terminal.server_id + '&user_id=' + this.terminal.user_id
    this.terminalSocket = new WebSocket(ws_addr)
    this.terminalSocket.onopen = this.runRealTerminal
    this.terminalSocket.onclose = this.closeRealTerminal
    this.terminalSocket.onerror = this.errorRealTerminal
    this.term.attach(this.terminalSocket)
    this.term._initialized = true
    console.log('mounted is going on')
  },
  beforeDestroy () {
    this.terminalSocket.close()
    this.term.destroy()
  }
}
</script>
