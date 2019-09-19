<template>
  <div class="container">
    <Alert>IDC信息：/ {{row.idc_name}} / {{row.rack_name}} / {{row.ssh_ip}} </Alert>
    <my-terminal :terminal="terminal"></my-terminal>
  </div>
</template>

<script>
import {GetServer} from '@/api/category/servers'
import Console from './Console'

export default {
  
  name: 'WebSSH',
  
  created (){
    this.handleGetDetail()
  },

  data () {
    return {
      row:{},
      terminal:{
        server_id: this.$route.params.server_id,
        user_id: this.$route.params.user_id,        
        name: 'terminal',
        cols: 600,
        rows: 400
      }
    }
  },

  methods: {
    handleGetDetail () {
      GetServer(this.terminal.server_id)
      .then(res => {
        this.row = res.data
      })
    },

  },

  components: {
    'my-terminal': Console
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
