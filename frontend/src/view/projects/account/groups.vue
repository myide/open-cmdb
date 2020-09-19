<template>
  <div>
    <Card>
      <Row>
        <Col span="4">
          <Input search v-model="getParams.search" placeholder="搜索" @on-search="handleGetGroupList" />
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
          <Table :columns="columnsUser" :data="groupList" size="small"></Table>
        </Col>
      </Row>
      </br>
      <Page :total=total show-sizer :current=getParams.page @on-change="pageChange" @on-page-size-change="sizeChange"></Page>
    </Card>
    <copyright> </copyright>

    <Modal
      v-model="createModal"
      width="500"
      title="创建组"
      @on-ok="handleCreateGroup"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="createGroupForm" :model="createGroupForm" :rules="ruleCreateGroupForm" :label-width="100">
              <FormItem label="组名：" prop="name">
                <Input v-model="createGroupForm.name"></Input>
              </FormItem>
            </Form>
          </Col>
        </Row>
      </div>
    </Modal>

    <Modal
      v-model="updateModal"
      width="500"
      title="修改组"
      @on-ok="handleUpdateGroup"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="updateGroupForm" :model="updateGroupForm" :rules="ruleUpdateGroupForm" :label-width="100">
              <FormItem label="组名：" prop="name">
                <Input v-model="updateGroupForm.name"></Input>
              </FormItem>
            </Form>
          </Col>
        </Row>
      </div>
    </Modal>

    <Modal
        v-model="showContent.modal"
        width="450"
        :title="showContent.title">
        <div class="modalcontent">
          <div v-for="item in showContent.data" :value="item.label" :key="item.label">
            <p v-if="item.role == 'developer'"> {{ item.name }} ( 研发 ) </p>
            <p v-else-if="item.role == 'developer_manager'"> {{ item.name }} ( 研发经理 ) </p>
            <p v-else-if="item.role == 'developer_supremo'"> {{ item.name }} ( 研发总监 ) </p>
            <p v-else> {{ item.label }} </p>
          </div>
        </div>
    </Modal>

    <Modal
        v-model="deleteModal"
        width="450"
        title="删除组"
        @on-ok="handleDeleteGroup">
        <div>
          <center> 删除组 {{deleteData.name}} </center>
        </div>
    </Modal>

  </div>
</template>
<script>
  import '@/static/base.css'
  import copyright from '@/view/components/public/copyright.vue'
  import {Button, Table, Modal, Message, Badge} from 'iview';
  import {GetGroupList, CreateGroup, UpdateGroup, DeleteGroup} from '@/api/account/groups'
  import {alertWarning} from '@/libs/view/common'

  export default {
    components: {Button, Table, Modal, Message, Badge, copyright},
    data () {
      return {
        deleteModal:false,
        createModal:false,
        updateModal:false,
        listStyle:{
          width: '300px',
          height: '300px'
        },
        transferTitles:['可选', '已选'],
        groupList:[],
        // 显示组权限或成员
        showContent:{
          modal:false,
          title:'',
          data:[],
        },
        // 创建组数据
        createGroupForm:{
          name:'',
        },
        ruleCreateGroupForm:{
          name: [{ required: true, message: '组名不能为空', trigger: 'blur' }],
        },
        // 修改组数据
        updateGroupForm:{
          id: '',
          name:'',
        },
        ruleUpdateGroupForm:{
          name: [{ required: true, message: '组名不能为空', trigger: 'blur' }],
        },
        columnsUser: [
          {
            title: 'ID',
            width: 80,
            key: 'id'
          },

          {
            title: '组名',
            render: (h, params) => {
              return h('Tag', {}, params.row.name)
            }
          },
          {
            title: '成员',
            render: (h, params) => {
              let data = params.row.members
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
                          this.showContent.modal = true
                          this.showContent.title = params.row.name + ' 成员'
                          this.showContent.data = data
                        }
                      }
                  }, '成员' + ' (' + data.length + ')')
                ]
              }
              return h('div', {}, subelm)
            }
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
                        this.updateModal = true
                        this.updateGroupForm.id = params.row.id
                        this.updateGroupForm.name = params.row.name
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
        // delete
        deleteData: {
          id:'',
          name:'',
        },
        // get
        total:1,
        userlist:[],
        getParams:{
          page:1,
          pagesize:10,
          search:'',
        }
      }
    },
    created (){
      this.handleGetGroupList()
    },
    methods: {

      pageChange (page) {
        this.getParams.page = page
        this.handleGetGroupList()
      },

      sizeChange(size){
        this.pagesize = size
        this.handleGetGroupList()
      },

      filterMethod (data, query) {
        return data.label.indexOf(query) > -1;
      },
      handleCreateGroup () {
        this.$refs.createGroupForm.validate((valid) => {
          if (!valid) {
            return
          }
          CreateGroup(this.createGroupForm)
          .then(res => {
            this.handleGetGroupList()
            alertWarning('create', this.$Notice, data.name)
          })
        })
      },
      handleUpdateGroup () {
        this.$refs.updateGroupForm.validate((valid) => {
          if (!valid) {
            return
          }
          UpdateGroup(this.updateGroupForm.id, this.updateGroupForm)
          .then(res => {
            this.handleGetGroupList()
            alertWarning('update', this.$Notice, id)
          })
        })
      },

      handleDeleteGroup () {
        DeleteGroup(this.deleteData.id)
        .then(res => {
          this.handleGetGroupList()
          alertWarning('update', this.$Notice, id)
        })
      },

      handleGetGroupList () {
        GetGroupList(this.getParams)
        .then(res => {
          this.groupList = res.data.results
          this.total = res.data.count
        })
      },

      cancel () {
        Message.info('Clicked cancel');
      },
    },
  }
</script>
