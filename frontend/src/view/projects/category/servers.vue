<style scoped>
  .parm_check_element {
    width: 400px;
    margin-left: 10px;
  }
  .left20 {
    margin-left: 20px
  }

</style>

<template>
  <div>
      <Card>
      <Row>
        <Col span="4">
          <Input search v-model="getParams.search" placeholder="主机名/SSH地址" @on-search="handleGetList" />
        </Col>

        <Col span="10">
          <center>
            <Button type="primary" icon="md-add" @click="createModal = true">创建</Button>
          </center>
        </Col>
      </Row>
      </br>
      <Row>
        <Col span="24">
          <Table :columns="columnsDataList" :data="dataList" size="small"></Table>
        </Col>
      </Row>
      </br>
      <Page :total=total show-sizer :current=getParams.page @on-change="pageChange" @on-page-size-change="sizeChange"></Page>

    </Card>
    <copyright> </copyright>

    <Spin size="large" fix v-if="spinShow"></Spin>

    <Modal
      v-model="createModal"
      width="500"
      title="创建服务器"
      @on-ok="handleCreate"
      @on-cancel="cancel">
      <div class="formcontent">
        <Row>
          <Col span="22">
            <Form ref="createForm" :model="createForm" :rules="ruleForm" :label-width="100">
              <FormItem label="选择机房：">
                <Select v-model="createForm.idc"  @on-change="handleGetListRacks(createForm.idc)">
                  <Option v-for="item in idcList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="选择机柜：">
                <Select v-model="createForm.rack">
                  <Option v-for="item in rackList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="业务用户：">
                <Select v-model="createForm.users" multiple>
                  <Option v-for="item in userList" :value="item.id" :key="item.id">{{ item.username }}</Option>
                </Select>
              </FormItem>
              <FormItem label="SSH用户：">
                <Select v-model="createForm.ssh_user">
                  <Option v-for="item in sshUserList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="SSH IP地址：" prop="ssh_ip">
                <Input v-model="createForm.ssh_ip" placeholder="SSH IP地址"></Input>
              </FormItem>
              <FormItem label="SSH 端口：" prop="ssh_port">
                <Input v-model="createForm.ssh_port" placeholder="SSH IP端口（留空默认为22）"></Input>
              </FormItem>
              <FormItem label="备注：">
                <Input v-model="createForm.remark" placeholder="备注"></Input>
              </FormItem>
            </Form>
          </Col>
        </Row>
      </div>
    </Modal>

    <Modal
      v-model="updateModal"
      width="500"
      :title="'修改服务器 (ID: ' + updateForm.id + ')'"
      @on-ok="handleUpdate"
      @on-cancel="cancel">
      <div class="formcontent">
        <Row>
          <Col span="22">
            <Form ref="updateForm" :model="updateForm" :rules="ruleForm" :label-width="100">
              <FormItem label="所属机房：">
                <Select v-model="updateForm.idc" @on-change="handleGetListRacks(updateForm.idc)">
                  <Option v-for="item in idcList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="所属机柜：">
                <Select v-model="updateForm.rack">
                  <Option v-for="item in rackList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="业务用户：">
                <Select v-model="updateForm.users" multiple>
                  <Option v-for="item in userList" :value="item.id" :key="item.id">{{ item.username }}</Option>
                </Select>
              </FormItem>
              <FormItem label="SSH用户：">
                <Select v-model="updateForm.ssh_user">
                  <Option v-for="item in sshUserList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="SSH IP地址：" prop="ssh_ip">
                <Input v-model="updateForm.ssh_ip" placeholder="SSH IP地址"></Input>
              </FormItem>
              <FormItem label="SSH 端口：" prop="ssh_port">
                <Input v-model="updateForm.ssh_port" placeholder="SSH IP端口（留空默认为22）"></Input>
              </FormItem>
              <FormItem label="备注：" prop="remark">
                <Input v-model="updateForm.remark"></Input>
              </FormItem>
            </Form>
          </Col>
        </Row>
      </div>
    </Modal>

    <Modal
      v-model="deleteModal"
      width="450"
      :title="'删除服务器 (ID: ' + deleteData.id + ')'"
      @on-ok="handleDelete"
      @on-cancel="cancel">
      <div>
        <p>确认删除服务器 {{deleteData.name}} ?</p>
      </div>
    </Modal>

    <Modal
      v-model="fetchServerInfoModal"
      width="450"
      :title="'采集服务器信息 (ID: ' + serverInfoData.id + ')'"
      @on-ok="handleFetchServerInfo"
      @on-cancel="cancel">
      <div>
        <p>确认采集服务器（{{serverInfoData.name}}）信息?</p>
      </div>
    </Modal>

  </div>
</template>
<script>
  import '@/static/base.css'
  import {Button, Table, Modal, Message, Tag} from 'iview';
  import copyright from '@/view/components/public/copyright.vue'
  import {GetUserList} from '@/api/account/users'
  import {GetSSHUserList} from '@/api/category/sshusers'
  import {GetServerList, CreateServer, UpdateServer, DeleteServer, FetchServerInfo} from '@/api/category/servers'
  import {GetIdcList, GetIdc} from '@/api/category/idcs'
  import {GetRackList} from '@/api/category/racks'
  import {alertWarning} from '@/libs/view/common'

  export default {
    components: {copyright},
    data () {
      return {
      spinShow:false,
      deleteModal:false,
      createModal:false,
      updateModal:false,
      fetchServerInfoModal:false,
      idc:'',
      search:'',
      idcList:[],
      rackList:[],
      dataList:[],
      deleteData:{
        id:'',
        name:''
      },
      serverInfoData:{
        id:'',
        name:''
      },
      serverTypeList:[
        '物理机',
        '虚拟机',
        '容器'
      ],
      userList:[],
      sshUserList:[],
      createForm:{
        idc:'',
        users:[],
        ssh_user:'',
        ssh_ip:'',
        ssh_port:'22',
        rack:'',
        remark:''
      },
      updateForm:{
        id:'',
        idc:'',
        users:[],
        ssh_user:'',
        ssh_ip:'',
        ssh_port:'',
        rack:'',
        remark:''
      },
      ruleForm: {
      },
      columnsDataList: [
        {
          title: 'ID',
          width: 60,
          render: (h, params) => {
            return h('router-link', {props:{to:'/category/servers/'+params.row.id}}, params.row.id)
          }
        },
        {
          title: '主机名',
          key: 'name'
        },
        {
          title: 'SSH地址',
          key: 'ssh_ip',
          width: 120,
        },
        {
          title: '所属机柜',
          key: 'rack_name',
          width: 100,
        },
        {
          title: '服务器类型',
          key: 'system_product'
        },
        {
          title: '状态',
          width: 100,
          render: (h, params) => {
            let status = params.row.status
            if (status == '0') {
              var tag = h('Badge',{props:{status:'warning', text:"下线"}}, '')
            } else {
              tag = h('Badge',{props:{status:'success', text:"在线"}}, '')
            }
            return h('div', [tag])
          }
        },
        {
          title: '备注',
          key: 'remark'
        },
        {
          title: '操作',
          width: 210,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h(Button, {
                props: {
                  type: 'primary',
                  size: 'small'
                },
                style: {
                  marginRight: '12px'
                },
                on: {
                  click: () => {
                    const row = params.row
                    this.updateModal = true
                    this.updateForm.id = row.id
                    this.updateForm.users = []
                    for (let u of row.users){
                      this.updateForm.users.push(u.id)
                    }
                    this.updateForm.ssh_user = row.ssh_user.id
                    this.updateForm.ssh_ip = row.ssh_ip
                    this.updateForm.ssh_port = row.ssh_port
                    this.updateForm.idc = row.idc
                    this.updateForm.rack = row.rack
                    this.updateForm.remark = row.remark
                    this.handleGetListRacks(row.idc)
                  }
                }
              }, '修改'),
              h(Button, {
                props: {
                  type: 'error',
                  size: 'small'
                },
                style: {
                  marginRight: '12px'
                },
                on: {
                  click: () => {
                    this.deleteModal = true
                    this.deleteData.id = params.row.id
                    this.deleteData.name = params.row.name
                  }
                }
              }, '删除'),
              h(Button, {
                props: {
                  type: 'success',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.fetchServerInfoModal = true
                    this.serverInfoData.id = params.row.id
                    this.serverInfoData.name = params.row.name
                  }
                }
              }, '采集')
            ])
          }
        },
      ],
      total:1,
      getParams:{
        page:1,
        pagesize:10,
        search:'',
      },
      getMaxParams:{
        page:1,
        pagesize:1000,
        search:'',
      },
      }
    },

    created () {
      this.handleGetList()
      this.handleGetListIdcs()
      this.handleGetListUsers()
      this.handleGetListSSHUsers()
    },

    methods: {

      handleGetList () {
        GetServerList(this.getParams)
        .then(
          res => {
            this.dataList = res.data.results
            this.total = res.data.count
          }
        )
      },

      handleGetListIdcs () {
        GetIdcList(this.getMaxParams)
        .then(
          res => {
            this.idcList = res.data.results
          }
        )
      },

      handleGetListRacks (idc_id) {
        GetIdc(idc_id)
        .then(
          res => {
            this.createForm.rack = ''
            this.rackList = res.data.racks
          }
        )
      },

      handleGetListUsers () {
        GetUserList(this.getMaxParams)
        .then(
          res => {
            this.createForm.users = []
            this.userList = res.data.results
          }
        )
      },

      handleGetListSSHUsers () {
        GetSSHUserList(this.getMaxParams)
        .then(
          res => {
            this.createForm.ssh_user = ''
            this.sshUserList = res.data.results
          }
        )
      },

      pageChange (page) {
        this.getParams.page = page
        this.handleGetList()
      },

      sizeChange (size){
        this.getParams.pagesize = size
        this.handleGetList()
      },

      handleCreate () {
        this.$refs.createForm.validate((valid) => {
          if (!valid) {
            return
          }
          let data = JSON.parse(JSON.stringify(this.createForm))  // 深拷贝
          CreateServer(data)
          .then(
            res => {
              this.handleGetList()
              alertWarning('create', this.$Notice, '')
            },
          )
        })
      },

      handleUpdate () {
        this.$refs.updateForm.validate((valid) => {
          if (!valid) {
            return
          }
          let id = this.updateForm.id
          let data = JSON.parse(JSON.stringify(this.updateForm))  // 深拷贝
          UpdateServer(id, data)
          .then(
            res => {
              this.handleGetList()
              alertWarning('update', this.$Notice, id)
            }
          )
        })
      },

      handleDelete () {
        let id = this.deleteData.id
        DeleteServer(id)
        .then (res => {
          this.handleGetList()
          alertWarning('delete', this.$Notice, id)
        })
      },

      handleFetchServerInfo () {
        let id = this.serverInfoData.id
        FetchServerInfo(id)
        .then (res => {
          this.handleGetList()
          alertWarning('fetchInfo', this.$Notice, id)
        })
      },

      cancel () {
        Message.info('Clicked cancel');
      }

    },
  }
</script>
