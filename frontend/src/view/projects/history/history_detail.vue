<style scoped>
</style>

<template>
  <div>
    <Row>
    <Col span="24">
      <Card>
        <Tabs>
          <TabPane label="历史记录"></TabPane>
        </Tabs>
        <div style="margin-top:10px;margin-bottom:10px">

          <Row>
            <Col span="1">
              <p> <b>ID：</b> </p>
            </Col>
            <Col span="2">
              <p> {{this.$route.params.id}} </p>
            </Col>

            <Col span="2">
              <p> <b>记录名：</b> </p>
            </Col>
            <Col span="3">
              <p> {{row.name}} </p>
            </Col>

            <Col span="1">
              <p> <b>用户：</b> </p>
            </Col>
            <Col span="2">
              <p> {{row.user}} </p>
            </Col>

            <Col span="2">
              <p> <b>更新时间：</b> </p>
            </Col>
            <Col span="4">
              <p>{{row.create_time | parseTime}}</p>
            </Col>

            <Col span="1">
              <p> <b>对象：</b> </p>
            </Col>
            <Col span="2">
              <p> {{row.instance}} </p>
            </Col>
          </Row>

          <Row>
            <Col span="1">
              <p> <b>备注：</b> </p>
            </Col>
            <Col span="23">
              <p> {{row.remark}} </p>
            </Col>
          </Row>

        </div>
      </Card>

        <div style="margin-top:10px;margin-bottom:10px">
          <Row>
            <Col span="12">
              <Card>
                <p slot="title">
                  <Icon type="md-arrow-back" />
                    操作前
                </p>
                <div class="code-con">{{row.before | parseJSON}}</div>

              </Card>
            </Col>
            <Col span="12">
              <Card>
                <p slot="title">
                  <Icon type="md-arrow-forward" />
                    操作后
                </p>
                <div class="code-con">{{row.after | parseJSON}}</div>
              </Card>
            </Col>

          </Row>
        </div>

    </Col>

    </Row>

    <copyright> </copyright>

  </div>
</template>

<script>
import {Button} from 'iview';
import copyright from '@/view/components/public/copyright.vue'
import {GetHistory} from '@/api/history/histories'

export default {

  components: {copyright},

  created () {
    this.handleGetDetail()
  },

  computed: {},

  data () {
    return {
      row:{},

    }
  },

  filters:{
    parseTime (t) {
      try{
        return t.split(".")[0].replace('T',' ')
      }
      catch(err){
      }
    },

    parseJSON (v) {
      return v
    }

  },

  methods: {
    handleGetDetail () {
      GetHistory(this.$route.params.id)
        .then(res => {
          this.row = res.data
        })
    },


  },


}
</script>

<style>
.code-con{
  background: #F9F9F9;
  padding-top: 10px;
}
</style>
