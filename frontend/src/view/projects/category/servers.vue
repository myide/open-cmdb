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
          <Input search v-model="getParams.search" placeholder="搜索" @on-click="handleGetList" @on-enter="handleGetList" />
        </Col>

        <Col span="10">
          <center>
            <Button type="primary" icon="md-add" @click="createModal = true">创建</Button>
          </center>
        </Col>
      </Row>
      </br>
      <Row>
        <Col span="23">
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
              <FormItem label="服务器类型：">
                <Select v-model="createForm.server_type">
                  <Option v-for="item in serverTypeList" :value="item" :key="item">{{ item }}</Option>
                </Select>
              </FormItem>
              <FormItem label="主机名：" prop="name">
                <Input v-model="createForm.name" placeholder="主机名"></Input>
              </FormItem>
              <FormItem label="业务用户：">
                <Select v-model="createForm.users" multiple>
                  <Option v-for="item in userList" :value="item.id" :key="item.id">{{ item.username }}</Option>
                </Select>
              </FormItem>
              <FormItem label="SSH用户：">
                <Select v-model="createForm.ssh_users" multiple>
                  <Option v-for="item in sshUserList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="SSH IP地址：" prop="ssh_ip">
                <Input v-model="createForm.ssh_ip" placeholder="SSH IP地址"></Input>
              </FormItem>
              <FormItem label="SSH 端口：" prop="ssh_port">
                <Input v-model="createForm.ssh_port" placeholder="SSH IP端口（留空默认为22）"></Input>
              </FormItem>
              <FormItem label="UUID：" prop="uuid">
                <Input v-model="createForm.uuid" placeholder="UUID"></Input>
              </FormItem>
              <FormItem label="CPU：">
                <Input v-model="createForm.cpu" placeholder="CPU"></Input>
              </FormItem>
              <FormItem label="内存：">
                <Input v-model="createForm.memory" placeholder="内存"></Input>
              </FormItem>
              <FormItem label="磁盘：">
                <Input v-model="createForm.disk" placeholder="磁盘"></Input>
              </FormItem>
              <FormItem label="运行状态：" prop="status">
                <RadioGroup v-model="createForm.status">
                    <Radio label="在线"></Radio>
                    <Radio label="下线"></Radio>
                </RadioGroup>
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
      title="修改服务器"
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
              <FormItem label="服务器类型：">
                <Select v-model="updateForm.server_type">
                  <Option v-for="item in serverTypeList" :value="item" :key="item">{{ item }}</Option>
                </Select>
              </FormItem>
              <FormItem label="主机名：" prop="name">
                <Input v-model="updateForm.name" placeholder="主机名"></Input>
              </FormItem>
              <FormItem label="业务用户：">
                <Select v-model="updateForm.users" multiple>
                  <Option v-for="item in userList" :value="item.id" :key="item.id">{{ item.username }}</Option>
                </Select>
              </FormItem>
              <FormItem label="SSH用户：">
                <Select v-model="updateForm.ssh_users" multiple>
                  <Option v-for="item in sshUserList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="SSH IP地址：" prop="ssh_ip">
                <Input v-model="updateForm.ssh_ip" placeholder="SSH IP地址"></Input>
              </FormItem>
              <FormItem label="SSH 端口：" prop="ssh_port">
                <Input v-model="updateForm.ssh_port" placeholder="SSH IP端口（留空默认为22）"></Input>
              </FormItem>
              <FormItem label="UUID：" prop="uuid">
                <Input v-model="updateForm.uuid" placeholder="UUID"></Input>
              </FormItem>
              <FormItem label="CPU：">
                <Input v-model="updateForm.cpu" placeholder="CPU"></Input>
              </FormItem>
              <FormItem label="内存：">
                <Input v-model="updateForm.memory" placeholder="内存"></Input>
              </FormItem>
              <FormItem label="磁盘：">
                <Input v-model="updateForm.disk" placeholder="磁盘"></Input>
              </FormItem>
              <FormItem label="运行状态：" prop="status">
                <RadioGroup v-model="updateForm.status">
                    <Radio label="在线"></Radio>
                    <Radio label="下线"></Radio>
                </RadioGroup>
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
      title="删除服务器"
      @on-ok="handleDelete"
      @on-cancel="cancel">
      <div>
        <p>确认删除服务器 {{deleteData.name}} ?</p>
      </div>
    </Modal>

    <Modal
      v-model="daqModal"
      width="600"
      title="采集信息">
      <div>
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
    </Modal>

  </div>
</template>
<script>
  import '@/static/base.css'
  import {Button, Table, Modal, Message, Tag} from 'iview';
  import copyright from '@/view/components/public/copyright.vue'
  import {GetUserList} from '@/api/account/users'
  import {GetSSHUserList} from '@/api/category/sshusers'
  import {GetServerList, CreateServer, UpdateServer, DeleteServer} from '@/api/category/servers'
  import {GetIdcList, GetIdc} from '@/api/category/idcs'
  import {GetRackList} from '@/api/category/racks'
  import {alertWarning} from '@/libs/view/common'

  export default {
    components: {copyright},
    data () {
      return {
      spinShow:false,
      daqModal:false,
      deleteModal:false,
      createModal:false,
      updateModal:false,
      daq:'',
      idc:'',
      search:'',
      idcList:[],
      rackList:[],
      dataList:[],
      deleteData:{
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
        ssh_users:[],
        ssh_ip:'',
        ssh_port:'22',
        rack:'',
        name:'',
        server_type:'',
        uuid:'',
        cpu:'',
        memory:'',
        disk:'',
        status:'在线',
        remark:''
      },
      updateForm:{
        id:'',
        idc:'',
        users:[],
        ssh_users:[],
        ssh_ip:'',
        ssh_port:'',
        rack:'',
        name:'',
        server_type:'',
        uuid:'',
        cpu:'',
        memory:'',
        disk:'',
        status:'',
        remark:''
      },
      ruleForm: {
        name: [{ required: true, message: '主机名不能为空', trigger: 'blur' }],
        uuid: [{ required: true, message: 'UUID不能为空', trigger: 'blur' }],
        cpu: [{ required: true, message: 'CPU不能为空', trigger: 'blur' }],
        memory: [{ required: true, message: '内存不能为空', trigger: 'blur' }],
        disk: [{ required: true, message: '磁盘不能为空', trigger: 'blur' }],
        status: [{ required: true, message: '状态不能为空', trigger: 'blur' }],
      },
      columnsDataList: [
        {
          title: 'ID',
          width: 80,
          render: (h, params) => {
            return h('router-link', {props:{to:'/category/servers/'+params.row.id}}, params.row.id)
          }
        },
        {
          title: '主机名',
          key: 'name'
        },
        {
          title: '所属机柜',
          key: 'rack_name'
        },
        {
          title: '服务器类型',
          key: 'server_type'
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
          title: '采集数据',
          width: 100,
          render: (h, params) => {
            return h('div', [
              h(Button, {
                props: {
                  type: 'info',
                  size: 'small'
                },
                on: {
                  click: () => {
                    const row = params.row
                    this.daqModal = true
                    let daq = row.daq
                    this.daq = JSON.parse(daq)
                    console.log(daq)
                  }
                }
              }, '查看')
            ])
          },
        },
        {
          title: '操作',
          width: 150,
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
                    this.updateForm.ssh_users = []
                    for (let u of row.ssh_users){
                      this.updateForm.ssh_users.push(u.id)
                    }
                    this.updateForm.ssh_ip = row.ssh_ip
                    this.updateForm.ssh_port = row.ssh_port
                    this.updateForm.idc = row.idc
                    this.updateForm.rack = row.rack
                    this.updateForm.name = row.name
                    this.updateForm.server_type = row.server_type
                    this.updateForm.uuid = row.uuid
                    this.updateForm.cpu = row.cpu
                    this.updateForm.memory = row.memory
                    this.updateForm.disk = row.disk
                    this.updateForm.cpu = row.cpu
                    this.updateForm.status = this.status_map[row.status]
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
                on: {
                  click: () => {
                    this.deleteModal = true
                    this.deleteData.id = params.row.id
                    this.deleteData.name = params.row.name
                  }
                }
              }, '删除')
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
      status_map:{
        '0':'下线',
        '1':'在线',
        '下线':'0',
        '在线':'1'
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
            this.createForm.ssh_users = []
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
          data.status = this.status_map[data.status]
          CreateServer(data)
          .then(
            res => {
              this.handleGetList()
              alertWarning('create', this.$Notice, data.name)
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
          data.status = this.status_map[data.status]
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

      cancel () {
        Message.info('Clicked cancel');
      }

    },
  }
</script>
