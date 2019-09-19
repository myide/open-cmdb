<style scoped>
</style>

<template>
  <div>
    <Row>
    <Col span="12">
      <Card>
        <Tabs>
          <TabPane label="基本信息（机房）"></TabPane>
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
              <p> <b>机房名：</b> </p>
            </Col>
            <Col span="20">
              <p> {{row.name}} </p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>机柜数：</b> </p>
            </Col>
            <Col span="20">
              <p> {{get_racks_length}} </p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>地址：</b> </p>
            </Col>
            <Col span="20">
              <p> {{row.address}} </p>
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
          <TabPane label="相关机柜"></TabPane>
        </Tabs>
        <div style="margin-top:10px;margin-bottom:10px">
          <Table :columns="columnsRackList" :data="rackList" size="small"></Table>
        </div>
      </Card>
    </Col>
    </Row>
    <copyright> </copyright>

  </div>
</template>

<script>
import copyright from '@/view/components/public/copyright.vue'
import {GetIdc} from '@/api/category/idcs'

export default {

  components: {copyright},

  created () {
    this.handleGetDetail()
  },

  computed: {
    get_racks_length: function () {
      let racks = this.row.racks
      if (typeof(racks) == "undefined") {
        var racks_length = 0
      } else {
        racks_length = racks.length
      }
      return racks_length
    }
  },
  data () {
    return {
      row:{},
      rackList:[],
      columnsRackList: [
        {
          title: 'ID',
          width: 80,
          render: (h, params) => {
            return h('router-link', {props:{to:'/category/racks/'+params.row.id}}, params.row.id)
          }
        },
        {
          title: '机柜名',
          key: 'name'
        }
      ]
    }
  },

  methods: {
    handleGetDetail () {
      GetIdc(this.$route.params.id)
        .then(res => {
          this.row = res.data
          this.rackList = res.data.racks
        })
    },

  },

}
</script>
