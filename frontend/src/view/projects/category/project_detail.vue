<style scoped>
</style>

<template>
  <div>
    <Row>
    <Col span="12">
      <Card>
        <Tabs>
          <TabPane label="基本信息（项目）"></TabPane>
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
              <p> <b>项目名：</b> </p>
            </Col>
            <Col span="20">
              <p> {{row.name}} </p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>状态：</b> </p>
            </Col>
            <Col span="20">
              <p v-if="row.status == 0"><Badge status="success" text="启用"/></p>
              <p v-else-if="row.status == 1"><Badge status="warning" text="停用"/></p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>语言：</b> </p>
            </Col>
            <Col span="20">
              <p> {{row.language_type}} </p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>版本库：</b> </p>
            </Col>
            <Col span="20">
              <p> {{row.repo_url}} </p>
            </Col>
          </Row>
          <Row>
            <Col span="4">
              <p> <b>Jenkins Job：</b> </p>
            </Col>
            <Col span="20">
              <p> {{row.jenkins_job}} </p>
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
       <TabPane label="所属业务线" icon="ios-git-network">
          <div style="margin-top:10px;margin-bottom:10px">
            <div class="modalcontent">
              <Table :columns="columnsBusinessLineList" :data="row.businesses" size="small"></Table>
            </div>
          </div>
        </TabPane>

        <TabPane label="相关用户" icon="ios-person">
          <div style="margin-top:10px;margin-bottom:10px">
            <div class="modalcontent">
              <Table :columns="columnsUserList" :data="row.users" size="small"></Table>
            </div>
          </div>
        </TabPane>

        <TabPane label="相关服务器" icon="logo-tux">
          <div style="margin-top:10px;margin-bottom:10px">
            <div class="modalcontent">
              <Table :columns="columnsServerList" :data="row.servers" size="small"></Table>
            </div>
          </div>
        </TabPane>

      </Tabs>
      </Card>
    </Col>
    </Row>

    <copyright> </copyright>

  </div>
</template>

<script>
import '@/static/base.css'
import copyright from '@/view/components/public/copyright.vue'
import {GetProject} from '@/api/category/projects'

export default {

  components: {copyright},

  created () {
    this.handleGetDetail()
  },

  data () {
    return {
      row:{},
      columnsBusinessLineList:[
        {
          title: 'ID',
          key: 'id',
          width: 80
        },
        {
          title: '业务线名',
          key: 'name'
        }
      ],
      columnsUserList:[
        {
          title: 'ID',
          key: 'id',
          width: 80
        },
        {
          title: '用户名',
          key: 'username'
        }
      ],
      columnsServerList:[
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
      GetProject(this.$route.params.id)
        .then(res => {
          this.row = res.data
        })
    },

  },

}
</script>
