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
              <p> {{row.system_product}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>SSH 用户：</b> </p>
            </Col>
            <Col span="19">
              <p> {{updateCron.name}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>SSH 地址/端口：</b> </p>
            </Col>
            <Col span="19">
              <p> {{row.ssh_ip}} / {{row.ssh_port}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>SSH连接：</b> </p>
            </Col>
            <Col span="19">
              <p> <router-link :to="get_webssh_url"> 连接 </router-link> </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>创建时间：</b> </p>
            </Col>
            <Col span="19">
              <p> {{row.create_time | parseTime}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="5">
              <p> <b>修改时间：</b> </p>
            </Col>
            <Col span="19">
              <p> {{row.update_time | parseTime}} </p>
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

        </div>
      </Card>
    </Col>

    <Col span="12">
      <Card>
        <Tabs>
          
          <TabPane label="相关用户">
            <div>
              <div class="modalcontent">
                <Table :columns="columnsUserList" :data="row.users" size="small"></Table>
              </div>
            </div>
          </TabPane>

          <TabPane label="相关项目">
            <div>
              <div class="modalcontent">
                <Table :columns="columnsProjectList" :data="row.projects" size="small"></Table>
              </div>
            </div>
          </TabPane>

          <TabPane label="定时任务">
            <Row>
              <Col span="24">
                <div style="margin-bottom:10px">
                  <i-input type="textarea" :rows="10" v-model="updateCron.content" placeholder="请输入..."></i-input>
                </div>
              </Col>
              <div>
              <ButtonGroup>
                <Button @click="handleUpdateServerCron">保存</Button>
                <Button @click="handleSyncServerCron">同步</Button>
                <Button @click="handleFetchServerCronLog">日志</Button>
              </ButtonGroup>
              </div>
            </Row>
          </TabPane>

        </Tabs>

      </Card>
    </Col>
    </Row>

    <copyright> </copyright>

    <Modal
      v-model="cronLogModal"
      width="900"
      title="cron日志"
      @on-ok=""
      @on-cancel="">
      <div style="height: 500px; overflow-y:scroll; background:#000; color:#FFF">
        <pre>{{cronlog}}</pre>
      </div>
    </Modal>

    <Modal
      v-model="cronSyncModal"
      width="900"
      title="cron同步"
      @on-ok="handleSyncCron"
      @on-cancel="">
      <div>
        <Row>
          <Col span="2">选择项目</Col>
          <Col span="22">
            <RadioGroup v-model="project" @on-change="getProjectHosts">
              <Radio v-for="item in projects" :label="item.id">{{item.name}}</Radio>
            </RadioGroup>
          </Col>
        </Row>
        <br>
        <div>
          <Row>
            <Col span="2">选择主机</Col>
            <Col span="22">
              <div style="border-bottom: 1px solid #e9e9e9;padding-bottom:6px;margin-bottom:6px;">
                  <Checkbox
                      :indeterminate="indeterminate"
                      :value="checkAll"
                      @click.prevent.native="handleCheckAll">全选</Checkbox>
              </div>
            </Col>
          </Row>
          <CheckboxGroup v-model="checkAllGroup" @on-change="checkAllGroupChange">
            <Checkbox v-for="item in projectServers" :label="item.id">{{item.ssh_ip}}</Checkbox>
          </CheckboxGroup>
        </div>

      </div>
    </Modal>

  </div>
</template>

<script>
import {Button} from 'iview';
import copyright from '@/view/components/public/copyright.vue'
import {GetServer, FetchServerCron, FetchServerCronLog, UpdateServerCron, SyncServerCron} from '@/api/category/servers'
import {GetProject} from '@/api/category/projects'
import {alertWarning} from '@/libs/view/common'


export default {

  components: {copyright},

  created () {
    this.handleGetDetail()
  },

  filters:{
    parseTime (t) {
      try{
        return t.split(".")[0].replace('T',' ')
      }
      catch(err){
      }
    }

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
    }

  },

  data () {
    return {
      row:{},
      cronLogModal:false,
      cronSyncModal:false,
      cronlog:'',
      project:'',
      projects:[],
      projectServers:[],
      user:'',
      updateCron:{
        name:'',
        content:''
      },
      indeterminate: true,
      checkAll: false,
      checkAllGroup: [],
      changeCheckData: {},
      checkValueAll:[],
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
      ]

    }
  },

  methods: {
    handleGetDetail () {
      GetServer(this.$route.params.id)
        .then(res => {
          this.row = res.data
          this.projects = res.data.projects
          this.user = res.data.ssh_user.id
          this.updateCron.name = res.data.ssh_user.name
          this.updateCron.content = res.data.cron_content
        })
    },

    handleFetchServerCron (name) {
      let data = {name: name}
      FetchServerCron(this.$route.params.id, data)
        .then(res => {
          this.updateCron.content = res.data.data
        })
    },

    handleFetchServerCronLog() {
      this.cronLogModal = true
      let data = {count: 100}
      FetchServerCronLog(this.$route.params.id, data)
        .then(res => {
          this.cronlog = res.data.data
        })
    },

    handleUpdateServerCron () {
      UpdateServerCron(this.$route.params.id, this.updateCron)
        .then(res => {
          console.log(res)
          alertWarning('update', this.$Notice, res.data.name)
        })
    },

    handleSyncServerCron () {
      this.cronSyncModal = true

    },

    getProjectHosts (v) {
      GetProject(v)
        .then(res => {
          let checkValueAll = []
          let projectServers = []
          for (let server of res.data.servers){
            if (server.ssh_ip != this.row.ssh_ip){
              checkValueAll.push(server.id)
              projectServers.push(server)
            }
          }
          this.checkValueAll = checkValueAll
          this.projectServers = projectServers
        })      
    },

    handleSyncCron () {
      console.log(this.checkAllGroup)
      let data = {servers: this.checkAllGroup}
      SyncServerCron(this.$route.params.id, data)
        .then(res => {
          alertWarning('sync', this.$Notice, data.servers)
        })
    },

    handleCheckAll () {
      if (this.indeterminate) {
        this.checkAll = false;
      } else {
        this.checkAll = !this.checkAll;
      }
      this.indeterminate = false;
      if (this.checkAll) {
        this.checkAllGroup = this.checkValueAll;
      } else {
        this.checkAllGroup = [];
      }
    },

    checkAllGroupChange (data) {
      let n = this.checkValueAll.length
      if (data.length === n) {
        this.indeterminate = false;
        this.checkAll = true;
      } else if (data.length > 0) {
        this.indeterminate = true;
        this.checkAll = false;
      } else {
        this.indeterminate = false;
        this.checkAll = false;
      }
    },

  },


}
</script>
