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
      title="创建SSH用户"
      @on-ok="handleCreate"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="createForm" :model="createForm" :rules="ruleForm" :label-width="100">
              <FormItem label="SSH用户名：" prop="name">
                <Input v-model="createForm.name" placeholder="远程服务器的SSH用户名"></Input>
              </FormItem>
              <FormItem label="SSH密码：" prop="password">
                <Input type="password" v-model="createForm.password" placeholder="SSH密码"></Input>
              </FormItem>
              <FormItem label="备注：" prop="remark">
                <Input v-model="createForm.remark" placeholder="备注"></Input>
              </FormItem>
            </Form>
            <Alert show-icon>SSH免密建议</Alert>
            <div>
            本机SSH用户{{ localSSHUser }}, 远程服务器SSH用户{{ createForm.name }}
            </div>
            <div>
            建议做本机对远程服务器的SSH免密登录:
            </div>
            <div>
            1. 通过ssh-copy-id或手工复制的方式，把本地用户{{ localSSHUser }}的id_rsa.pub内容追加到远程用户{{ createForm.name }}的authorized_keys 
            </div>
            <div>
            2. 把远程用户{{ createForm.name }}加入sudoers，并设置免密sudo
            </div>
          </Col>
        </Row>
      </div>
    </Modal>

    <Modal
      v-model="updateModal"
      width="500"
      title="修改用户"
      @on-ok="handleUpdate"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="updateForm" :model="updateForm" :rules="ruleForm" :label-width="100">
              <FormItem label="SSH用户名：" prop="name">
                <Input v-model="updateForm.name" placeholder="SSH用户名"></Input>
              </FormItem>
              <FormItem label="SSH密码：" prop="password">
                <Input v-model="updateForm.password" placeholder="SSH密码"></Input>
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
      title="删除用户"
      @on-ok="handleDelete"
      @on-cancel="cancel">
      <div>
        <p>确认删除用户 {{deleteData.name}} ?</p>
      </div>
    </Modal>

  </div>
</template>
<script>
  import copyright from '@/view/components/public/copyright.vue'
  import {Button, Table, Modal, Message, Tag} from 'iview';
  import {GetSSHUserList, CreateSSHUser, UpdateSSHUser, DeleteSSHUser, GetLocalSSHUser} from '@/api/category/sshusers'
  import {alertWarning} from '@/libs/view/common'

  export default {
    components: {copyright},
    data () {
      return {
      spinShow:false,
      deleteModal:false,
      createModal:false,
      updateModal:false,
      localSSHUser:'',
      search:'',
      dataList:[],
      deleteData:{
        id:'',
        name:''
      },
      createForm:{
        name: '',
        password: '',
        remark: ''
      },
      updateForm:{
        id:'',
        name:'',
        password:'',
        remark:''
      },
      ruleForm: {
        name: [{ required: true, message: 'SSH用户名不能为空', trigger: 'blur' }],
        password: [{ required: true, message: 'SSH密码不能为空', trigger: 'blur' }],
      },
      columnsDataList: [
        {
          title: 'ID',
          key: 'id',
          width: 80
        },
        {
          title: 'SSH用户名',
          key: 'name'
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
                      this.updateForm.password = row.password
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
      }
    },

    created () {
      this.handleGetList()
      this.handleGetLocalSSHUser()
    },

    methods: {

      handleGetList () {
        GetSSHUserList(this.getParams)
        .then(
          res => {
            this.dataList = res.data.results
            this.total = res.data.count
          }
        )
      },

      handleGetLocalSSHUser () {
        GetLocalSSHUser({})
        .then(
          res => {
            this.localSSHUser = res.data.data
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
          CreateSSHUser(data)
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
          let data = this.updateForm
          UpdateSSHUser(id, data)
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
        DeleteSSHUser(id)
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
