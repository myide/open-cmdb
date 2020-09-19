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
      title="创建业务线"
      @on-ok="handleCreate"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="createForm" :model="createForm" :rules="ruleForm" :label-width="100">
              <FormItem label="业务线名：" prop="name">
                <Input v-model="createForm.name" placeholder="机柜"></Input>
              </FormItem>
              <FormItem label="相关用户：">
                <Select v-model="createForm.users" filterable multiple>
                  <Option v-for="item in userList" :value="item.id" :key="item.id">{{ item.username }}</Option>
                </Select>
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
      title="修改业务线"
      @on-ok="handleUpdate"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="updateForm" :model="updateForm" :rules="ruleForm" :label-width="100">
              <FormItem label="业务线名：" prop="name">
                <Input v-model="updateForm.name" placeholder="业务线名"></Input>
              </FormItem>
              <FormItem label="相关用户：">
                <Select v-model="updateForm.users" filterable multiple>
                  <Option v-for="item in userList" :value="item.id" :key="item.id">{{ item.username }}</Option>
                </Select>
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
        <p>确认删除业务线 {{deleteData.name}} ?</p>
      </div>
    </Modal>

    <Modal
      v-model="showProject.modal"
      width="450"
      :title="showProject.title">
      <div class="modalcontent">
        <Table :columns="columnsProjectList" :data="showProject.data" size="small"></Table>
      </div>
    </Modal>

  </div>
</template>
<script>
  import copyright from '@/view/components/public/copyright.vue'
  import {Button, Table, Modal, Message, Tag} from 'iview';
  import {GetBusinessLineList, CreateBusinessLine, UpdateBusinessLine, DeleteBusinessLine} from '@/api/category/businesslines'
  import {GetUserList} from '@/api/account/users'

  export default {
    components: {copyright},
    data () {
      return {
      spinShow:false,
      deleteModal:false,
      createModal:false,
      updateModal:false,
      userList:[],
      search:'',
      dataList:[],
      showProject:{
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
        remark:''
      },
      updateForm:{
        id:'',
        name:'',
        users:[],
        remark:''
      },
      ruleForm: {
        name: [{ required: true, message: '业务线名不能为空', trigger: 'blur' }],
      },
      columnsProjectList:[
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
        }
      ],
      columnsDataList: [
        {
          title: 'ID',
          width: 80,
          key: 'id'
        },
        {
          title: '业务线名',
          key: 'name'
        },
        {
          title: '项目列表',
          render: (h, params) => {
            let data = params.row.projects
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
                        this.showProject.modal = true
                        this.showProject.title = params.row.name + ' 业务线'
                        this.showProject.data = data
                      }
                    }
                }, '详情' + ' (' + data.length + ')')
              ]
            }
            return h('div', {}, subelm)
          }
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
                      this.updateForm.remark = row.remark
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
      }
      }
    },

    created () {
      this.handleGetList()
      this.handleGetListUsers()
    },

    methods: {

      handleGetList () {
        GetBusinessLineList(this.getParams)
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
          let data = this.createForm
          CreateBusinessLine(data)
          .then(
            res => {
              this.handleGetList()
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
          let data = this.updateForm
          UpdateBusinessLine(id, data)
          .then(
            res => {
              this.handleGetList()
            }
          )
        })
      },

      handleDelete () {
        let id = this.deleteData.id
        DeleteBusinessLine(id)
        .then (res => {
          this.handleGetList()
        })
      },

      cancel () {
        Message.info('Clicked cancel');
      }

    },
  }
</script>
