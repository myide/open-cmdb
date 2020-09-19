<template>
  <div>
    <Card>
      <Row>
        <Col span="4">
          <Input search v-model="getParams.search" placeholder="搜索" @on-search="handleGetUserList" />
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
          <Table :columns="columnsUser" :data="userList" size="small"></Table>
        </Col>
      </Row>
      </br>
      <Page :total=total show-sizer :current=getParams.page @on-change="pageChange" @on-page-size-change="sizeChange"></Page>
    </Card>
    <copyright> </copyright>

    <Modal
      v-model="createModal"
      width="900"
      title="创建用户"
      @on-ok="handleCreateUser"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="createUserForm" :model="createUserForm" :rules="ruleCreateUserForm" :label-width="100">
              <Row>
                <Col span="12">
                  <FormItem label="用户名：" prop="username">
                    <Input v-model="createUserForm.username"></Input>
                  </FormItem>
                </Col>
                <Col span="12">
                  <FormItem label="密码：" prop="password">
                    <Input type="password" v-model="createUserForm.password"></Input>
                  </FormItem>
                </Col>
              </Row>
              <Row>
                <Col span="12">
                  <FormItem label="角色：">
                    <Select v-model="createUserForm.role">
                      <Option v-for="item in roleList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                  </FormItem>
                </Col>
                <Col span="12">
                  <FormItem label="属组：">
                    <Select v-model="createUserForm.groups[0]" filterable>
                      <Option v-for="item in groupList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                  </FormItem>
                </Col>
              </Row>
              <Row>
                <Col span="12">
                  <FormItem label="系统身份：" prop="systemAccount">
                    <CheckboxGroup v-model="createSysaccount">
                      <Checkbox label="is_active">已激活</Checkbox>
                      <Checkbox label="is_staff">登录后台</Checkbox>
                      <Checkbox label="is_superuser">管理员</Checkbox>
                    </CheckboxGroup>
                  </FormItem>
                </Col>
                <Col span="12">
                  <FormItem label="邮箱：" prop="email">
                    <Input v-model="createUserForm.email"></Input>
                  </FormItem>
                </Col>
              </Row>
            </Form>
          </Col>
        </Row>
      </div>
    </Modal>

    <Modal
      v-model="updateModal"
      width="900"
      title="修改用户"
      @on-ok="handleUpdateUser"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="updateUserForm" :model="updateUserForm" :rules="ruleUpdateUserForm" :label-width="100">
              <Row>
                <Col span="12">
                  <FormItem label="用户名：" prop="username">
                    <Input v-model="updateUserForm.username"></Input>
                  </FormItem>
                </Col>
                <Col span="12">
                  <FormItem label="密码：" prop="password">
                    <Input type="password" v-model="updateUserForm.password"></Input>
                  </FormItem>
                </Col>
              </Row>
              <Row>
                <Col span="12">
                  <FormItem label="角色：">
                    <Select v-model="updateUserForm.role">
                      <Option v-for="item in roleList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                  </FormItem>
                </Col>
                <Col span="12">
                  <FormItem label="属组：">
                    <Select v-model="updateUserForm.groups[0]">
                      <Option v-for="item in groupList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                  </FormItem>
                </Col>
              </Row>
              <Row>
                <Col span="12">
                  <FormItem label="系统身份：">
                    <CheckboxGroup v-model="updateSysaccount">
                      <Checkbox label="is_active">已激活</Checkbox>
                      <Checkbox label="is_staff">登录后台</Checkbox>
                      <Checkbox label="is_superuser">管理员</Checkbox>
                    </CheckboxGroup>
                  </FormItem>
                </Col>
                <Col span="12">
                  <FormItem label="邮箱：" prop="email">
                    <Input v-model="updateUserForm.email"></Input>
                  </FormItem>
                </Col>
              </Row>
            </Form>
          </Col>
        </Row>
      </div>

    </Modal>

    <Modal
      v-model="deleteModal"
      width="450"
      title="删除用户"
      @on-ok="handleDeleteUser">
      <div>
        <center> 删除用户 {{deletedata.username}} </center>
      </div>
    </Modal>

  </div>
</template>

<script>
  import '@/static/base.css'
  import copyright from '@/view/components/public/copyright.vue'
  import {Button, Table, Modal, Message, Badge, Icon} from 'iview';
  import {GetUserList, UpdateUser, CreateUser, DeleteUser} from '@/api/account/users'
  import {GetGroupList} from '@/api/account/groups'
  import {alertWarning} from '@/libs/view/common'

  export default {
    components: {Button, Table, Modal, Message, Badge, Icon, copyright},
    data () {
      return {
        deleteModal:false,
        createModal:false,
        updateModal:false,
        listStyle: {
          width: '300px',
          height: '300px'
        },
        groupList:[],
        roleList:[
          {
            value: 'developer',
            label: '研发'
          },
          {
            value: 'developer_manager',
            label: '研发经理'
          },
          {
            value: 'developer_supremo',
            label: '研发总监'
          },
        ],
        baseAuth:['is_active', 'is_staff', 'is_superuser'],
        // 创建用户数据
        createSysaccount:['is_active', 'is_staff'],
        createUserForm: {
          username:'',
          password:'',
          email:'',
          role:'developer',
          groups:[],
        },
        ruleCreateUserForm: {
          username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
          password: [{ required: true, message: '密码不能为空', trigger: 'blur' }],
          email: [{ required: true, message: '邮箱不能为空', trigger: 'blur' }],
        },
        // 修改用户数据
        updateSysaccount:[],
        updateUserForm: {
          id: '',
          username:'',
          password:'',
          email:'',
          role:'',
          groups:[],
        },
        ruleUpdateUserForm: {
          username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
          email: [{ required: true, message: '邮箱不能为空', trigger: 'blur' }],
        },
        columnsUser: [
          {
            title: 'ID',
            width: 80,
            key: 'id'
          },
          {
            title: '用户名',
            width: 150,
            render: (h, params) => {
            return h('Tag', {}, params.row.username)
            }
          },
          {
            title: '邮箱',
            key: 'email'
          },
          {
            title: '角色',
            width:100,
            render: (h, params) => {
            const roleMap = {
                developer:'研发',
                developer_manager:'研发经理',
                developer_supremo:'研发总监'
            }
            let role = params.row.role
            return h('span', {}, roleMap[role])
            }
          },
          {
            title: '属组',
            render: (h, params) => {
            return h('span', {}, params.row.groups.name)
            }
          },
          {
            title: '系统身份',
            width: 220,
            render: (h, params) => {
              const iconMap = {
                true: 'checkmark-circled',
                false: 'close-circled'
              }
              let sysele = []
              let superuser = params.row.is_superuser
              let active = params.row.is_active
              let staff = params.row.is_staff
              sysele.push(h('span', {}, '管理员'))
              sysele.push(h('Icon', {props:{type:iconMap[superuser]}, style:{marginRight:'10px'}}, ''))
              sysele.push(h('span', {}, '已激活'))
              sysele.push(h('Icon', {props:{type:iconMap[active]}, style:{marginRight:'10px'}}, ''))
              sysele.push(h('span', {}, '登录后台'))
              sysele.push(h('Icon', {props:{type:iconMap[staff]}}, ''))
              return h('div', {}, sysele)
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
                          this.updateUserForm.id = params.row.id
                          this.updateUserForm.username = params.row.username
                          this.updateUserForm.role = params.row.role
                          this.updateUserForm.email = params.row.email
                          this.updateUserForm.groups = JSON.stringify(params.row.groups) == "{}" ? [] : [params.row.groups.id]
                          this.updateUserForm.password = params.row.password
                          // 系统身份
                          let sysaccount = []
                          if (params.row.is_superuser == true) {
                            sysaccount.push('is_superuser')
                          }
                          if (params.row.is_active == true) {
                            sysaccount.push('is_active')
                          }
                          if (params.row.is_staff == true) {
                            sysaccount.push('is_staff')
                          }
                          this.updateSysaccount = sysaccount
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
                        this.deletedata.id = params.row.id
                        this.deletedata.username = params.row.username
                      }
                    }
                  }, '删除')
                ])
              }
          },
        ],
        // delete
        deletedata: {
          id:'',
          username:'',
        },
        // get
        total:1,
        userList:[],
        getParams:{
          page:1,
          pagesize:10,
          search:'',
        },
        getMaxParams:{
          page:1,
          pagesize:10000,
          search:'',
        },
      }
    },
    created (){
      this.handleGetGroupList()
      this.handleGetUserList()
    },
    methods: {

      pageChange (page) {
        this.getParams.page = page
        this.handleGetUserList()
      },

      sizeChange(size){
        this.getParams.pagesize = size
        this.handleGetUserList()
      },
      groupsFormat (grouplist) {
        let groups = []
        grouplist.map( (item) => {
          groups.push({
            value:item.id,
            label:item.name
          })
        })
        this.groupList = groups
        this.createUserForm.groups = groups.length > 0 ? [groups[0].value] : [] // 设置 groups 默认值
      },

      handleChangeCreate (newTargetKeys) {
        this.targetKeysCreate = newTargetKeys;
      },
      handleChangeupdate (newTargetKeys) {
        this.targetKeysupdate = newTargetKeys;
      },
      getSysaccount (sysaccount, data) {
        for (let auth in this.baseAuth){
          data[this.baseAuth[auth]] = 0
        }
        for (let acc in sysaccount){
          data[sysaccount[acc]] = 1
        }
        return data
      },
      handleCreateUser () {
        this.$refs.createUserForm.validate((valid) => {
          if (!valid) {
            return
          }
          let sysaccount = this.createSysaccount
          let data = this.createUserForm
          data = this.getSysaccount(sysaccount, data)
          data.db_id_list = this.targetKeysCreate
          CreateUser(data)
          .then(res => {
            this.handleGetUserList()
            alertWarning('create', this.$Notice, data.username)
          })
        })
      },

      handleUpdateUser () {
        this.$refs.updateUserForm.validate((valid) => {
          if (!valid) {
            return
          }
          let sysaccount = this.updateSysaccount
          let data = this.updateUserForm
          data = this.getSysaccount(sysaccount, data)
          data.db_id_list = this.targetKeysupdate
          UpdateUser(this.updateUserForm.id, data)
          .then(res => {
            this.handleGetUserList()
            alertWarning('update', this.$Notice, this.updateUserForm.id)
          })
        })
      },

      handleDeleteUser () {
        DeleteUser(this.deletedata.id)
        .then(res => {
          this.handleGetUserList()
          alertWarning('delete', this.$Notice, this.deletedata.id)
        })
      },

      handleGetUserList () {
        GetUserList(this.getParams)
        .then(res => {
          this.userList = res.data.results
          this.total = res.data.count
        })
      },

      handleGetGroupList () {
        GetGroupList(this.getMaxParams)
        .then(res => {
          this.groupsFormat(res.data.results)
        })
      },

      cancel () {
        Message.info('Clicked cancel');
      },
    },
  }
</script>
