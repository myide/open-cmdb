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
          <Input search v-model="getParams.search" placeholder="机房名/地址" @on-search="handleGetList" />
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
      title="创建机房"
      @on-ok="handleCreate"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="createForm" :model="createForm" :rules="ruleForm" :label-width="100">
              <FormItem label="机房名：" prop="name">
                <Input v-model="createForm.name" placeholder="机房"></Input>
              </FormItem>
              <FormItem label="地址：" prop="address">
                <Input v-model="createForm.address" placeholder="地址"></Input>
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
      title="修改机房"
      @on-ok="handleUpdate"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="updateForm" :model="updateForm" :rules="ruleForm" :label-width="100">
              <FormItem label="机房名：" prop="host">
                <Input v-model="updateForm.name" placeholder="机房名"></Input>
              </FormItem>
              <FormItem label="地址：" prop="port">
                <Input v-model="updateForm.address" placeholder="地址"></Input>
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
      title="删除机房"
      @on-ok="handleDelete"
      @on-cancel="cancel">
      <div>
        <p>确认删除机房 {{deleteData.name}} ?</p>
      </div>
    </Modal>

  </div>
</template>
<script>
  import copyright from '@/view/components/public/copyright.vue'
  import {Button, Table, Modal, Message, Tag} from 'iview';
  import {GetIdcList, CreateIdc, UpdateIdc, DeleteIdc} from '@/api/category/idcs'
  import {alertWarning} from '@/libs/view/common'

  export default {
    components: {copyright},
    data () {
      return {
      spinShow:false,
      deleteModal:false,
      createModal:false,
      updateModal:false,
      search:'',
      dataList:[],
      deleteData:{
        id:'',
        name:''
      },
      createForm:{
        name: '',
        address: '',
        remark: ''
      },
      updateForm:{
        id:'',
        name:'',
        address:'',
        remark:''
      },
      ruleForm: {
        name: [{ required: true, message: '机房名不能为空', trigger: 'blur' }],
        address: [{ required: true, message: '机房地址不能为空', trigger: 'blur' }],
      },
      columnsDataList: [
        {
          title: 'ID',
          width: 80,
          render: (h, params) => {
            return h('router-link', {props:{to:'/category/idcs/'+params.row.id}}, params.row.id)
          }
        },
        {
          title: '机房名',
          key: 'name'
        },
        {
          title: '机柜数',
          render: (h, params) => {
            let row = params.row
            return h('div', [h('span',{props:{}}, row.racks.length)])
          }
        },
        {
          title: '地址',
          key: 'address'
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
                      this.updateForm.address = row.address
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
    },

    methods: {

      handleGetList () {
        GetIdcList(this.getParams)
        .then(
          res => {
            this.dataList = res.data.results
            this.total = res.data.count
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
          CreateIdc(data)
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
          UpdateIdc(id, data)
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
        DeleteIdc(id)
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
