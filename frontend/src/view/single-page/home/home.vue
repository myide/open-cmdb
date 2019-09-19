<template>
  <div>
    <Row :gutter="20">
      <i-col :xs="12" :md="8" :lg="6" v-for="(infor, i) in inforCardData" :key="`infor-${i}`" style="height: 120px;padding-bottom: 10px;">
        <infor-card shadow :color="infor.color" :icon="infor.icon" :icon-size="36">
          <count-to :end="infor.count" count-class="count-style"/>
          <p>{{ infor.title }}</p>
        </infor-card>
      </i-col>
    </Row>
    <Row :gutter="20" style="margin-top: 10px;">
      <i-col :md="24" :lg="8" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-pie v-if="flag" style="height: 300px;" :value="pieData" text="机房设备统计"></chart-pie>
        </Card>
      </i-col>
      <i-col :md="24" :lg="16" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-bar v-if="flag" style="height: 300px;" :value="barData" text="每周用户活跃量"/>
        </Card>
      </i-col>
    </Row>
    <Row>
      <Card shadow>
        <example style="height: 310px;"/>
      </Card>
    </Row>
  </div>
</template>

<script>
import InforCard from '_c/info-card'
import CountTo from '_c/count-to'
import { ChartPie, ChartBar } from '_c/charts'
import Example from './example.vue'
import {GetDashBoardData} from '@/api/dashboard/dashboard_data'


export default {
  name: 'home',
  components: {
    InforCard,
    CountTo,
    ChartPie,
    ChartBar,
    Example
  },
  data () {
    return {
      flag: false,
      info_map: {
        '服务器数': 'server_count',
        '业务线数': 'business_count',
        '项目数': 'project_count',
        '用户数': 'user_count'
      },
      inforCardData: [
        { title: '服务器数', icon: 'logo-tux', count: 803, color: '#2d8cf0' },
        { title: '业务线数', icon: 'md-locate', count: 232, color: '#19be6b' },
        { title: '项目数', icon: 'md-share', count: 142, color: '#ff9900' },
        { title: '用户数', icon: 'md-person-add', count: 657, color: '#ed3f14' }
      ],
      pieData: [
        /*
        { value: 335, name: '直接访问' },
        { value: 310, name: '邮件营销' },
        { value: 234, name: '联盟广告' },
        { value: 135, name: '视频广告' },
        { value: 1548, name: '搜索引擎' }
        */
      ],
      barData: {}
    }
  },
  mounted () {
    this.handleGetData()
  },
  methods: {
    handleGetData () {
      GetDashBoardData()
        .then(res => {
          let data = res.data.data
          this.pieData = []
          let pie = data.pie
          for (let i of pie){
            let item = {value: i.value, name:i.name}
            this.pieData.push(item)
          }
          let info = data.info
          for (let i of this.inforCardData) {
            i.count = info[this.info_map[i.title]]
          }
          this.barData = data.date_login

          console.log(this.pieData)
          this.flag = true
        })
    },

  }

}
</script>

<style lang="less">
.count-style{
  font-size: 50px;
}
</style>
