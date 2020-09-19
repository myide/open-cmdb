
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
          <Input search v-model="getParams.search" placeholder="搜索" @on-search="handleGetList" />
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
      title="创建项目"
      @on-ok="handleCreate"
      @on-cancel="cancel">
      <div class="formcontent">
        <Row>
          <Col span="22">
            <Form ref="createForm" :model="createForm" :rules="ruleForm" :label-width="100">
              <FormItem label="项目名：" prop="name">
                <Input v-model="createForm.name" placeholder="项目名"></Input>
              </FormItem>
              <FormItem label="状态：" prop="status">
                <RadioGroup v-model="createForm.status">
                  <Radio label="启用"></Radio>
                  <Radio label="停用"></Radio>
                </RadioGroup>
              </FormItem>
              <FormItem label="相关用户：">
                <Select v-model="createForm.users" filterable multiple>
                  <Option v-for="item in userList" :value="item.id" :key="item.id">{{ item.username }}</Option>
                </Select>
              </FormItem>
              <FormItem label="所属业务线：">
                <Select v-model="createForm.businesses" filterable multiple>
                  <Option v-for="item in businessLineList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="相关服务器：">
                <Select v-model="createForm.servers" filterable multiple>
                  <Option v-for="item in serverList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="语言：">
                <Select v-model="createForm.language_type" prop="language_type">
                  <Option v-for="item in languageList" :value="item" :key="item">{{ item }}</Option>
                </Select>
              </FormItem>
              <FormItem label="版本库地址：" prop="repo_url">
                <Input v-model="createForm.repo_url" placeholder="版本库地址"></Input>
              </FormItem>
              <FormItem label="Jenkins Job：" prop="jenkins_job">
                <Input v-model="createForm.jenkins_job" placeholder="Jenkins Job"></Input>
              </FormItem>
              <FormItem label="备注：" prop="remark">
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
      title="修改项目"
      @on-ok="handleUpdate"
      @on-cancel="cancel">
      <div class="formcontent">
        <Row>
          <Col span="22">
            <Form ref="updateForm" :model="updateForm" :rules="ruleForm" :label-width="100">
              <FormItem label="项目名：" prop="name">
                <Input v-model="updateForm.name" placeholder="项目名"></Input>
              </FormItem>
              <FormItem label="状态：" prop="status">
                <RadioGroup v-model="updateForm.status">
                    <Radio label="启用"></Radio>
                    <Radio label="停用"></Radio>
                </RadioGroup>
              </FormItem>
              <FormItem label="相关用户：">
                <Select v-model="updateForm.users" filterable multiple>
                  <Option v-for="item in userList" :value="item.id" :key="item.id">{{ item.username }}</Option>
                </Select>
              </FormItem>
              <FormItem label="所属业务线：">
                <Select v-model="updateForm.businesses" filterable multiple>
                  <Option v-for="item in businessLineList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="相关服务器：">
                <Select v-model="updateForm.servers" filterable multiple>
                  <Option v-for="item in serverList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="语言：">
              <Select v-model="updateForm.language_type" prop="language_type">
                <Option v-for="item in languageList" :value="item" :key="item">{{ item }}</Option>
              </Select>
              </FormItem>
              <FormItem label="版本库地址：" prop="repo_url">
                <Input v-model="updateForm.repo_url" placeholder="版本库地址"></Input>
              </FormItem>
              <FormItem label="Jenkins Job：" prop="jenkins_job">
                <Input v-model="updateForm.jenkins_job" placeholder="Jenkins Job"></Input>
              </FormItem>
              <FormItem label="备注：">
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
      title="删除业务线"
      @on-ok="handleDelete"
      @on-cancel="cancel">
      <div>
        <p>确认删除项目 {{deleteData.name}} ?</p>
      </div>
    </Modal>

    <Modal
      v-model="showBusinessLine.modal"
      width="450"
      :title="showBusinessLine.title">
      <div class="modalcontent">
        <Table :columns="columnsBusinessLineList" :data="showBusinessLine.data" size="small"></Table>
      </div>
    </Modal>

  </div>
</template>
<script>
  import '@/static/base.css'
  import copyright from '@/view/components/public/copyright.vue'
  import {Button, Table, Modal, Message, Tag} from 'iview';
  import {GetProjectList, CreateProject, UpdateProject, DeleteProject} from '@/api/category/projects'
  import {GetUserList} from '@/api/account/users'
  import {GetBusinessLineList} from '@/api/category/businesslines'
  import {GetServerList} from '@/api/category/servers'
  import {alertWarning} from '@/libs/view/common'

  export default {
    components: {copyright},
    data () {
      return {
      spinShow:false,
      deleteModal:false,
      createModal:false,
      updateModal:false,
      languageList:['python', 'java', 'php', 'golang'],
      userList:[],
      businessLineList:[],
      serverList:[],
      dataList:[],
      showBusinessLine:{
        modal:false,
        title:'',
        data:[]
      },
      deleteData:{
        id:'',
        name:''
      },
      createForm:{
        name:'',
        users:[],
        businesses:[],
        servers:[],
        language_type:'',
        repo_url:'',
        jenkins_job:'',
        status:'启用',
        remark:''
      },
      updateForm:{
        id:'',
        name:'',
        users:[],
        businesses:[],
        servers:[],
        language_type:'',
        repo_url:'',
        jenkins_job:'',
        status:'',
        remark:''
      },
      ruleForm: {
        name: [{ required: true, message: '业务线名不能为空', trigger: 'blur' }],
      },
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
      columnsDataList: [
        {
          title: 'ID',
          width: 80,
          render: (h, params) => {
            return h('router-link', {props:{to:'/category/projects/'+params.row.id}}, params.row.id)
          }
        },
        {
          title: '项目名',
          key: 'name'
        },
        {
          title: '状态',
          width: 100,
          render: (h, params) => {
            let status = params.row.status
            if (status == '0') {
              var tag = h('Badge',{props:{status:'success', text:"启用"}}, '')
            } else {
              tag = h('Badge',{props:{status:'warning', text:"停用"}}, '')
            }
            return h('div', [tag])
          }
        },
        {
          title: '所属业务线',
          width: 100,
          render: (h, params) => {
            let data = params.row.businesses
            if (data.length == 0) {
              var subelm = []
            } else {
              var subelm = [
                h(Button, {
                    props: {
                      type: 'info',
                      size: 'small'
                    },
                    style: {
                      marginRight: '12px'
                    },
                    on: {
                      click: () => {
                        this.showBusinessLine.modal = true
                        this.showBusinessLine.title = params.row.name + ' 项目'
                        this.showBusinessLine.data = data
                      }
                    }
                }, '详情' + ' (' + data.length + ')')
              ]
            }
            return h('div', {}, subelm)
          }
        },
        {
          title: '语言',
          key: 'language_type'
        },
        {
          title: '版本库',
          key: 'repo_url'
        },
        {
          title: 'Jenkins Job',
          key: 'jenkins_job'
        },
        {
          title: '备注',
          key: 'remark'
        },
        {
          title: '操作',
          key: 'action',
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
                      this.updateForm.name = row.name
                      let users = []
                      for (let item of row.users) {
                        users.push(item.id)
                      }
                      this.updateForm.users = users
                      let businesses = []
                      for (let item of row.businesses) {
                        businesses.push(item.id)
                      }
                      this.updateForm.businesses = businesses
                      this.updateForm.repo_url = row.repo_url
                      this.updateForm.language_type = row.language_type
                      this.updateForm.status = this.status_map[row.status]
                      this.updateForm.jenkins_job = row.jenkins_job
                      this.updateForm.remark = row.remark
                      this.updateForm.servers = []
                      for (let server of row.servers) {
                        this.updateForm.servers.push(server.id)
                      }
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
        '0':'启用',
        '1':'停用',
        '启用':'0',
        '停用':'1'
      }

      }
    },

    created () {
      this.handleGetList()
      this.handleGetListUsers()
      this.handleGetListBusinessLines()
      this.handleGetListServers()
    },

    methods: {

      handleGetList () {
        GetProjectList(this.getParams)
        .then(
          res => {
            this.dataList = res.data.results
            this.total = res.data.count
          }
        )
      },

      handleGetListUsers () {
        GetUserList(this.getMaxParams)
        .then(
          res => {
            this.userList = res.data.results
          }
        )
      },

      handleGetListBusinessLines () {
        GetBusinessLineList(this.getMaxParams)
        .then(
          res => {
            this.businessLineList = res.data.results
          }
        )
      },

      handleGetListServers () {
        GetServerList(this.getMaxParams)
        .then(
          res => {
            this.serverList = res.data.results
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
          CreateProject(data)
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
          UpdateProject(id, data)
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
        DeleteProject(id)
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
