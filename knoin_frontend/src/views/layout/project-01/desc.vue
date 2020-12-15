<template>
  <div>
    <bread-crumb :breadCrumb="breadCrumb" />
    <b-card no-body>
      <b-tabs card>
        <b-tab title="新建项目" active>
          <b-card-body>
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
        </b-tab>
        <b-tab title="进行中">
          <b-card-body>
            <b-table striped hover :items="items"></b-table>
          </b-card-body>
        </b-tab>
        <b-tab title="已完成">
          <b-card-body>
            <b-table striped hover :items="finishedItems" :fields="fields">
              <template v-slot:cell(操作)="">
                <b-button
                  :to="{ name: 'Result01' }"
                  variant="info"
                  size="sm"
                  class="mr-2"
                >
                  查看结果
                </b-button>
                <b-button variant="danger" size="sm" class="mr-2">
                  重新分析
                </b-button>
              </template>
            </b-table>
          </b-card-body>
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import BreadCrumb from '@/components/BreadCrumb.vue'

export default {
  name: 'Desc01',
  components: { BreadCrumb },
  data() {
    return {
      breadCrumb: [
        { href: '', name: '传感染mNGS临床检测分析', isActive: true }
      ],
      items: [
        { 项目ID: 40, 项目名称: 'Dickerson', 开始时间: '2020-10-1', 文件: '计算文件', 分析参数: '参数详情', 项目情况: '分析中：50%' },
        { 项目ID: 21, 项目名称: 'Larsen', 开始时间: '2020-10-1', 文件: '计算文件', 分析参数: '参数详情', 项目情况: '分析中：50%' },
        { 项目ID: 89, 项目名称: 'Geneva', 开始时间: '2020-10-1', 文件: '计算文件', 分析参数: '参数详情', 项目情况: '分析中：50%' },
        { 项目ID: 38, 项目名称: 'Jami', 开始时间: '2020-10-1', 文件: '计算文件', 分析参数: '参数详情', 项目情况: '分析中：50%' }
      ],
      fields: ['项目ID', '项目名称', '开始时间', '结束时间', '操作'],
      finishedItems: [
        { 项目ID: 40, 项目名称: 'Dickerson', 开始时间: '2020-10-1', 结束时间: '2020-12-1' },
        { 项目ID: 21, 项目名称: 'Larsen', 开始时间: '2020-10-1', 结束时间: '2020-12-1' },
        { 项目ID: 89, 项目名称: 'Geneva', 开始时间: '2020-10-1', 结束时间: '2020-12-1' },
        { 项目ID: 38, 项目名称: 'Jami', 开始时间: '2020-10-1', 结束时间: '2020-12-1' }
      ]
    }
  },
  methods: {}
}
</script>

<style lang="less" scoped>
.btn {
  margin: 0;
}
.input-group {
  margin: 5px auto;
}
.card {
  border: 2px solid rgba(0, 0, 0, 0.125);
  .card-body {
    .basicInfo {
      max-width: 30%;
      float: left;
      margin-left: 50px;
      margin-bottom: 40px;
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
