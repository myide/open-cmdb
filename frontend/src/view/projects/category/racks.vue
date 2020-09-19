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
          <Input search v-model="getParams.search" placeholder="机柜名" @on-search="handleGetList" />
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
      title="创建机柜"
      @on-ok="handleCreate"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="createForm" :model="createForm" :rules="ruleForm" :label-width="100">
              <FormItem label="选择机房：">
                <Select v-model="createForm.idc">
                  <Option v-for="item in idcList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="机柜名：" prop="name">
                <Input v-model="createForm.name" placeholder="机柜"></Input>
              </FormItem>
              <FormItem label="编号：" prop="number">
                <Input v-model="createForm.number" placeholder="编号"></Input>
              </FormItem>
              <FormItem label="U型：" prop="size">
                <Input v-model="createForm.size" placeholder="U型"></Input>
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
      title="修改机柜"
      @on-ok="handleUpdate"
      @on-cancel="cancel">
      <div>
        <Row>
          <Col span="22">
            <Form ref="updateForm" :model="updateForm" :rules="ruleForm" :label-width="100">
              <FormItem label="所属机房：">
                <Select v-model="updateForm.idc">
                  <Option v-for="item in idcList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
              </FormItem>
              <FormItem label="机柜名：" prop="name">
                <Input v-model="updateForm.name" placeholder="机柜名"></Input>
              </FormItem>
              <FormItem label="编号：" prop="number">
                <Input v-model="updateForm.number" placeholder="编号"></Input>
              </FormItem>
              <FormItem label="U型：" prop="size">
                <Input v-model="updateForm.size" placeholder="U型"></Input>
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
      title="删除机柜"
      @on-ok="handleDelete"
      @on-cancel="cancel">
      <div>
        <p>确认删除机柜 {{deleteData.name}} ?</p>
      </div>
    </Modal>

  </div>
</template>
<script>
  import {Button, Table, Modal, Message, Tag} from 'iview';
  import copyright from '@/view/components/public/copyright.vue'
  import {GetRackList, CreateRack, UpdateRack, DeleteRack} from '@/api/category/racks'
  import {GetIdcList} from '@/api/category/idcs'
  import {alertWarning} from '@/libs/view/common'

  export default {

    components: {copyright},
    data () {
      return {
      spinShow:false,
      deleteModal:false,
      createModal:false,
      updateModal:false,
      idc:'',
      search:'',
      idcList:[],
      dataList:[],
      deleteData:{
        id:'',
        name:''
      },
      createForm:{
        idc:'',
        name:'',
        number:'',
        size:'',
        remark:''
      },
      updateForm:{
        id:'',
        name:'',
        idc:'',
        number:'',
        size:'',
        remark:''
      },
      ruleForm: {
        name: [{ required: true, message: '机柜名不能为空', trigger: 'blur' }],
        number: [{ required: true, message: '机柜编号不能为空', trigger: 'blur' }],
        size: [{ required: true, message: '机柜型号不能为空', trigger: 'blur' }]
      },
      columnsDataList: [
        {
          title: 'ID',
          width: 80,
          render: (h, params) => {
            return h('router-link', {props:{to:'/category/racks/'+params.row.id}}, params.row.id)
          }
        },
        {
          title: '机柜名',
          key: 'name'
        },
        {
          title: '所属机房',
          key: 'idc_name'
        },
        {
          title: '服务器数',
          width: 100,
          render: (h, params) => {
            let row = params.row
            return h('div', [h('span',{props:{}}, row.servers.length)])
          }
        },
        {
          title: 'U型',
          key: 'size',
          width: 80
        },
        {
          title: '编号',
          key: 'number'
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
                      this.updateForm.idc = row.idc
                      this.updateForm.number = row.number
                      this.updateForm.size = row.size
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
      this.handleGetListIdcs()
    },

    methods: {

      handleGetList () {
        GetRackList(this.getParams)
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
          CreateRack(data)
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
          UpdateRack(id, data)
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
        DeleteRack(id)
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
