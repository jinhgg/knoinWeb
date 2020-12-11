<template>
  <div>
    <bread-crumb :breadCrumb="breadCrumb" />
    <b-card title="Card Title" no-body>
      <b-card-header header-tag="nav">
        <b-nav card-header pills>
          <b-nav-item :active="curNav == 0" @click="curNav = 0"
            >报告生成</b-nav-item
          >
          <b-nav-item :active="curNav == 1" @click="curNav = 1"
            >报告模板</b-nav-item
          >
          <b-nav-item :active="curNav == 2" @click="curNav = 2"
            >结果数据筛选</b-nav-item
          >
        </b-nav>
      </b-card-header>

      <b-card-body class="newProj" v-show="curNav == 0">
        <b-card title="基本信息" class="basicInfo">
          <b-input-group prepend="姓名">
            <b-form-input></b-form-input>
          </b-input-group>
          <b-input-group prepend="年龄">
            <b-form-input></b-form-input>
          </b-input-group>
          <b-input-group prepend="性别">
            <b-form-input></b-form-input>
          </b-input-group>
          <b-input-group prepend="编号">
            <b-form-input></b-form-input>
          </b-input-group>
          <b-input-group prepend="样本类型">
            <b-form-input></b-form-input>
          </b-input-group>
          <b-input-group prepend="表型">
            <b-form-input></b-form-input>
          </b-input-group>
        </b-card>
        <b-card class="btnGroup">
          <b-button variant="primary">数据选取</b-button>
          <b-button variant="primary">参考选取</b-button>
          <b-button variant="primary">保存</b-button>
          <b-button variant="danger">分析</b-button>
        </b-card>

        <b-card class="analysisConfig" title="分析设置">
          <b-input-group prepend="MQ">
            <b-form-input></b-form-input>
          </b-input-group>
          <b-input-group prepend="BQ">
            <b-form-input></b-form-input>
          </b-input-group>
          <b-input-group prepend="AD">
            <b-form-input></b-form-input>
          </b-input-group>
        </b-card>
      </b-card-body>
      <b-card-body v-show="curNav == 1" class="text-center">
        <b-table striped hover :items="items"></b-table>
      </b-card-body>
      <b-card-body v-show="curNav == 2" class="text-center">
        <b-table striped hover :items="finishedItems"></b-table>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
import BreadCrumb from '@/components/BreadCrumb.vue'

export default {
  name: 'Result',
  components: { BreadCrumb },
  mounted() {
    console.log(this.$route)
  },
  data() {
    return {
      curNav: 0,
      breadCrumb: [
        { href: '/project-01', name: '传感染mNGS临床检测分析', isActive: false },
        { href: '', name: '结果', isActive: true }
      ],
      items: [
        { 项目ID: 40, 项目名称: 'Dickerson', 开始时间: '2020-10-1', 文件: '计算文件', 分析参数: '参数详情', 项目情况: '分析中：50%' },
        { 项目ID: 21, 项目名称: 'Larsen', 开始时间: '2020-10-1', 文件: '计算文件', 分析参数: '参数详情', 项目情况: '分析中：50%' },
        { 项目ID: 89, 项目名称: 'Geneva', 开始时间: '2020-10-1', 文件: '计算文件', 分析参数: '参数详情', 项目情况: '分析中：50%' },
        { 项目ID: 38, 项目名称: 'Jami', 开始时间: '2020-10-1', 文件: '计算文件', 分析参数: '参数详情', 项目情况: '分析中：50%' }
      ],
      finishedItems: [
        { 项目ID: 40, 项目名称: 'Dickerson', 开始时间: '2020-10-1', 结束时间: '2020-12-1', 操作: '查看结果' },
        { 项目ID: 21, 项目名称: 'Larsen', 开始时间: '2020-10-1', 结束时间: '2020-12-1', 操作: '查看结果' },
        { 项目ID: 89, 项目名称: 'Geneva', 开始时间: '2020-10-1', 结束时间: '2020-12-1', 操作: '查看结果' },
        { 项目ID: 38, 项目名称: 'Jami', 开始时间: '2020-10-1', 结束时间: '2020-12-1', 操作: '查看结果' }
      ]
    }
  },
  methods: {}
}
</script>

<style lang="less" scoped>
.breadcrumb {
  background-color: #fff;
  margin-top: 1rem;
  margin-bottom: 1rem;
}
.input-group {
  margin: 5px auto;
}
// .text-center {
//   background-color: #fff !important;
// }
// .newProj {
//
// }
.card {
  border: 2px solid rgba(0, 0, 0, 0.125);
  .card-body {
    // background-color: #598392;
    .basicInfo {
      max-width: 30%;
      float: left;
      margin-left: 50px;
    }
    .btnGroup {
      max-width: 30%;
      float: left;
      margin-left: 100px;
      border: 0px;
      button {
        display: block;
        margin: 30px auto;
      }
    }
    .analysisConfig {
      max-width: 30%;
      float: left;
      margin-left: 100px;
    }
  }
}
</style>
