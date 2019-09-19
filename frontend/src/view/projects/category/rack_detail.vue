<style scoped>
</style>

<template>
  <div>
    <Row>
    <Col span="12">
      <Card>
        <Tabs>
          <TabPane label="基本信息（机柜）"></TabPane>
        </Tabs>
        <div style="margin-top:10px;margin-bottom:10px">
          <Row>
            <Col span="4">
              <p> <b>ID：</b> </p>
            </Col>
            <Col span="20">
              <p> {{this.$route.params.id}} </p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>机柜名：</b> </p>
            </Col>
            <Col span="20">
              <p> {{row.name}} </p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>归属机房：</b> </p>
            </Col>
            <Col span="20">
              <p><router-link :to="get_idc_url">{{row.idc_name}}</router-link></p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>服务器数：</b> </p>
            </Col>
            <Col span="20">
              <p> {{get_servers_length}} </p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>编号：</b> </p>
            </Col>
            <Col span="20">
              <p> {{row.number}} </p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>U型：</b> </p>
            </Col>
            <Col span="20">
              <p> {{row.size}} </p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>备注：</b> </p>
            </Col>
            <Col span="20">
              <p> {{row.remark}} </p>
            </Col>
          </Row>
        </div>
      </Card>
    </Col>

    <Col span="12">
      <Card>
        <Tabs>
          <TabPane label="相关服务器"></TabPane>
        </Tabs>
        <div style="margin-top:10px;margin-bottom:10px">
          <Table :columns="columnsServerList" :data="serverList" size="small"></Table>
        </div>
      </Card>
    </Col>
    </Row>
    <copyright> </copyright>

  </div>
</template>

<script>
import copyright from '@/view/components/public/copyright.vue'
import {GetRack} from '@/api/category/racks'

export default {

  components: {copyright},

  created () {
    this.handleGetDetail()
  },

  computed: {
    get_servers_length: function () {
      let servers = this.row.servers
      if (typeof(servers) == "undefined") {
        var servers_length = 0
      } else {
        servers_length = servers.length
      }
      return servers_length
    },

    get_idc_url: function () {
      let url = '/category/idcs/' + this.row.idc
      return url
    }
  },
  data () {
    return {
      row:{},
      serverList:[],
      columnsServerList: [
        {
          title: 'ID',
          width: 80,
          render: (h, params) => {
            return h('router-link', {props:{to:'/category/servers/'+params.row.id}}, params.row.id)
          }
        },
        {
          title: '服务器名',
          key: 'name'
        }
      ]
    }
  },

  methods: {
    handleGetDetail () {
      GetRack(this.$route.params.id)
        .then(res => {
          this.row = res.data
          this.serverList = res.data.servers
        })
    },

  },

}
</script>
