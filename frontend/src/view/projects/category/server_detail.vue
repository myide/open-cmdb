<style scoped>
</style>

<template>
  <div>
    <Row>
    <Col span="12">
      <Card>
        <Tabs>
          <TabPane label="基本信息（服务器）"></TabPane>
        </Tabs>
        <div style="margin-top:10px;margin-bottom:10px">

          <Row>
            <Col span="5">
              <p> <b>ID：</b> </p>
            </Col>
            <Col span="19">
              <p> {{this.$route.params.id}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>主机名：</b> </p>
            </Col>
            <Col span="19">
              <p> {{row.name}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>归属机房/机柜：</b> </p>
            </Col>
            <Col span="19">
              <p><router-link :to="get_idc_url">{{row.idc_name}}</router-link> / <router-link :to="get_rack_url">{{row.rack_name}}</router-link></p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>UUID：</b> </p>
            </Col>
            <Col span="19">
              <p> {{row.uuid}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>CPU：</b> </p>
            </Col>
            <Col span="19">
              <p> {{row.cpu}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>内存：</b> </p>
            </Col>
            <Col span="19">
              <p> {{row.memory}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>磁盘：</b> </p>
            </Col>
            <Col span="19">
              <p> {{row.disk}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>类型：</b> </p>
            </Col>
            <Col span="19">
              <p> {{row.server_type}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>备注：</b> </p>
            </Col>
            <Col span="19">
              <p> {{row.remark}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>SSH 地址：</b> </p>
            </Col>
            <Col span="19">
              <p> {{row.ssh_ip}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>SSH连接：</b> </p>
            </Col>
            <Col span="10">
              <Select v-model="user" placeholder="请选择SSH用户">
                <Option v-for="item in ssh_users" :value="item.id" :key="item.id">{{ item.name }}</Option>
              </Select>
            </Col>
            <Col span="9">
              <p style="text-align:center" v-if="user"> <router-link :to="get_webssh_url"> 连接 </router-link> </p>
            </Col>
          </Row>

        </div>
      </Card>
    </Col>

    <Col span="12">
      <Card>
        <Tabs>
          
          <TabPane label="采集信息">
            <div style="margin-top:10px;margin-bottom:10px">
              <div v-for="(value,key) in daq" :value="value" :key="key">
                <Row>
                  <Col span="6">
                    <b>{{key}}: </b>
                  </Col>
                  <Col span="18">
                    <span>{{value}}</span>
                  </Col>
                </Row>
              </div>
            </div>
          </TabPane>
          
          <TabPane label="相关用户">
            <div style="margin-top:10px;margin-bottom:10px">
              <div class="modalcontent">
                <Table :columns="columnsUserList" :data="row.users" size="small"></Table>
              </div>
            </div>
          </TabPane>

          <TabPane label="相关项目">
            <div style="margin-top:10px;margin-bottom:10px">
              <div class="modalcontent">
                <Table :columns="columnsProjectList" :data="row.projects" size="small"></Table>
              </div>
            </div>
          </TabPane>
        </Tabs>

      </Card>
    </Col>
    </Row>

    <copyright> </copyright>

    <Modal
      v-model="sshuserModal"
      width="600"
      title="选择SSH用户">
      <div>
        <Select v-model="user">
          <Option v-for="item in ssh_users" :value="item.id" :key="item.id">{{ item.name }}</Option>
        </Select>
      </div>
    </Modal>

  </div>
</template>

<script>
import copyright from '@/view/components/public/copyright.vue'
import {GetServer} from '@/api/category/servers'

export default {

  components: {copyright},

  created () {
    this.handleGetDetail()
  },

  computed: {

    get_idc_url: function () {
      let url = '/category/idcs/' + this.row.idc
      return url
    },

    get_rack_url: function () {
      let url = '/category/racks/' + this.row.rack
      return url
    },

    get_webssh_url: function () {
      let url = '/category/webssh/' + this.row.id + '/' + this.user
      return url
    },

  },

  data () {
    return {
      row:{},
      daq:'',
      user:'',
      ssh_users:[],
      sshuserModal:false,
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
      columnsProjectList:[
        {
          title: 'ID',
          key: 'id',
          width: 80
        },
        {
          title: '项目名',
          key: 'name'
        }
      ],

    }
  },

  methods: {
    handleGetDetail () {
      GetServer(this.$route.params.id)
        .then(res => {
          this.row = res.data
          this.ssh_users = res.data.ssh_users
          try {
            this.daq = JSON.parse(res.data.daq)
          } catch (err) {
            console.log(err)
            this.daq = ""
          }
        })
    },

  },

}
</script>
