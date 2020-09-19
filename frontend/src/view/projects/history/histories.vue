<template>
  <div>
    <Card>
      <Row>
        <Col span="4">
          <Input search v-model="getParams.search" placeholder="记录类型" @on-search="handleGetHistoryList" />
        </Col>
      </Row>
      </br>
      <Row>
        <Col span="24">
          <Table :columns="columnsUser" :data="historyList" size="small"></Table>
        </Col>
      </Row>
      </br>
      <Page :total=total show-sizer :current=getParams.page @on-change="pageChange" @on-page-size-change="sizeChange"></Page>
    </Card>
    <copyright> </copyright>

  </div>
</template>
<script>
  import '@/static/base.css'
  import copyright from '@/view/components/public/copyright.vue'
  import {Button, Table, Modal, Message, Badge} from 'iview';
  import {GetHistoryList} from '@/api/history/histories'
  import {alertWarning} from '@/libs/view/common'

  export default {
    components: {Button, Table, Modal, Message, Badge, copyright},
    data () {
      return {
        listStyle:{
          width: '300px',
          height: '300px'
        },
        getParams:{
          page:1,
          pagesize:10,
          search:'',
        },
        total:1,
        historyList:[],
        columnsUser: [
          {
            title: 'ID',
            width: 60,
            render: (h, params) => {
              return h('router-link', {props:{to:'/history/histories/'+params.row.id}}, params.row.id)
            }
          },
          {
            title: '记录类型',
            key: 'name',
            width: 120,
          },
          {
            title: '创建时间',
            width: 160,
            render: (h, params) => {
              return h('div', [
                h('span', {}, params.row.create_time.split('.')[0].replace('T',' ')),
              ])
            }
          },
          {
            title: '对象',
            key: 'instance',
            width: 120
          },
          {
            title: '之前',
            render: (h, params) => {
              return h('Tag', {}, params.row.before)
            }
          },
          {
            title: '之后',
            render: (h, params) => {
              return h('Tag', {}, params.row.after)
            }
          },

        ]
      }
    },
    created (){
      this.handleGetHistoryList()
    },
    methods: {

      pageChange (page) {
        this.getParams.page = page
        this.handleGetHistoryList()
      },

      sizeChange(size){
        this.pagesize = size
        this.handleGetHistoryList()
      },

      filterMethod (data, query) {
        return data.label.indexOf(query) > -1;
      },

      handleGetHistoryList () {
        GetHistoryList(this.getParams)
        .then(res => {
          this.historyList = res.data.results
          this.total = res.data.count
        })
      },

      cancel () {
        Message.info('Clicked cancel');
      },
    },
  }
</script>
