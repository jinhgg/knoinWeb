<template>
  <div>
    <bread-crumb :breadCrumb="breadCrumb" />
    <b-card no-body>
      <b-tabs card>
        <b-tab title="新建项目" active>
          <b-card-body>
            <div class="basicInfo">
              <div hidden="hidden">
                <b-button id="selectProj" v-b-modal.modal-1
                  >Launch demo modal</b-button
                >
                <b-modal
                  ref="proj-modal"
                  size="xl"
                  id="modal-1"
                  title="样本选择"
                  hide-footer
                >
                  <b-table
                    selectable
                    ref="selectableTable"
                    :items="projectList"
                    :fields="project_fields"
                    select-mode="single"
                    @row-selected="onRowSelected"
                  >
                    <template #cell(选择)="{ rowSelected }">
                      <template v-if="rowSelected">
                        <span aria-hidden="true">&check;</span>
                        <span class="sr-only">Selected</span>
                      </template>
                      <template v-else>
                        <span aria-hidden="true">&nbsp;</span>
                        <span class="sr-only">Not selected</span>
                      </template>
                    </template>
                  </b-table>
                  <b-button class="mt-3" block @click="projOnSelect"
                    >确定</b-button
                  >
                </b-modal>
              </div>
              <h4 style="margin-bottom: 30px">基本信息</h4>
              <b-form-group
                label="文件导入:"
                label-for="fileBasic"
                label-cols-sm="3"
              >
                <b-form-file
                  id="fileBasic"
                  size="sm"
                  accept=".xlsx"
                  @change="readExcel($event)"
                  ref="file-proj"
                ></b-form-file>
                <b-button style="float:right;width:62px"  size="sm" @click="clearFiles">重置</b-button>
              </b-form-group>

              <b-form-group label-cols-sm="3" label="姓名:" label-for="name">
                <b-form-input
                  v-model="this.basicForm.name"
                  id="name"
                  size="sm"
                ></b-form-input>
              </b-form-group>

              <b-form-group label-cols-sm="3" label="年龄:" label-for="age">
                <b-form-input
                  v-model="this.basicForm.age"
                  id="age"
                  size="sm"
                ></b-form-input>
              </b-form-group>
              <b-form-group label-cols-sm="3" label="性别:" label-for="gender">
                <b-form-input
                  v-model="this.basicForm.gender"
                  id="gender"
                  size="sm"
                ></b-form-input>
              </b-form-group>
              <b-form-group label-cols-sm="3" label="编号:" label-for="no">
                <b-form-input
                  v-model="this.basicForm.no"
                  id="no"
                  size="sm"
                ></b-form-input>
              </b-form-group>
              <b-form-group
                label-cols-sm="4"
                label="样本类型:"
                label-for="type"
              >
                <b-form-input
                  v-model="this.basicForm.samType"
                  list="type-list-id"
                  size="sm"
                ></b-form-input>
                <datalist id="type-list-id">
                  <option>Manual Option</option>
                  <option>Manual Option</option>
                  <option>Manual Option</option>
                </datalist>
              </b-form-group>

              <b-form-group label-cols-sm="4" label="表型:" label-for="type">
                <b-form-input
                  v-model="this.basicForm.reportType"
                  list="form-list-id"
                  size="sm"
                ></b-form-input>
                <datalist id="form-list-id">
                  <option>Manual Option</option>
                  <option>Manual Option</option>
                  <option>Manual Option</option>
                </datalist>
              </b-form-group>
            </div>

            <div class="basicInfo">
              <h4>数据选取</h4>
              <div style="margin-top: 30px">
                <b-form-file
                  v-model="file01"
                  ref="file-input"
                  class="mb-2"
                ></b-form-file>
              </div>
              <h4 style="margin-bottom: 30px; margin-top: 30px">参考选取</h4>
              <div style="margin-top: 30px">
                <b-form-file
                  v-model="file01"
                  ref="file-input"
                  class="mb-2"
                ></b-form-file>
              </div>

              <div style="margin-top: 30px">
                <b-button style="margin: 0 20px 0 0" variant="outline-success">
                  保存
                </b-button>

                <b-button style="margin: 0 20px 0 0" variant="outline-danger">
                  分析
                </b-button>
              </div>
            </div>

            <!-- <div class="accordion" role="tablist">
    <h4 style="margin-bottom:30px">数据选取</h4>
    <b-card no-body class="mb-1" style="width:500px">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-button block v-b-toggle.accordion-1 variant="outline-secondary">Accordion 1</b-button>
      </b-card-header>
      <b-collapse id="accordion-1" visible accordion="my-accordion" role="tabpanel">
        <b-card-body>
          <b-card-text>I start opened because <code>visible</code> is <code>true</code></b-card-text>
          <b-card-text>{{ text }}</b-card-text>
        </b-card-body>
      </b-collapse>
    </b-card>

    <b-card no-body class="mb-1" style="width:500px">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-button block v-b-toggle.accordion-2 variant="outline-secondary">Accordion 2</b-button>
      </b-card-header>
      <b-collapse id="accordion-2" accordion="my-accordion" role="tabpanel">
        <b-card-body>
          <b-card-text>{{ text }}</b-card-text>
        </b-card-body>
      </b-collapse>
    </b-card>

    <b-card no-body class="mb-1" style="width:500px">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-button block v-b-toggle.accordion-3 variant="outline-secondary">Accordion 3</b-button>
      </b-card-header>
      <b-collapse id="accordion-3" accordion="my-accordion" role="tabpanel">
        <b-card-body>
          <b-card-text>{{ text }}</b-card-text>
        </b-card-body>
      </b-collapse>
    </b-card>
  </div> -->

            <!-- <div class="basicInfo">
              <h4 style="margin-bottom:30px">参考选取</h4>
              <b-card no-body class="mb-1">
                <b-card-header header-tag="header" class="p-1" role="tab">
                  <b-button block v-b-toggle.accordion-1 variant="info"
                    >Accordion 1</b-button
                  >
                </b-card-header>
                <b-collapse
                  id="accordion-1"
                  visible
                  accordion="my-accordion"
                  role="tabpanel"
                >
                  <b-card-body>
                    <b-card-text
                      >I start opened because <code>visible</code> is
                      <code>true</code></b-card-text
                    >
                    <b-card-text>{{ text }}</b-card-text>
                  </b-card-body>
                </b-collapse>
              </b-card>

              <b-card no-body class="mb-1">
                <b-card-header header-tag="header" class="p-1" role="tab">
                  <b-button block v-b-toggle.accordion-2 variant="info"
                    >Accordion 2</b-button
                  >
                </b-card-header>
                <b-collapse
                  id="accordion-2"
                  accordion="my-accordion"
                  role="tabpanel"
                >
                  <b-card-body>
                    <b-card-text>{{ text }}</b-card-text>
                  </b-card-body>
                </b-collapse>
              </b-card>

              <b-card no-body class="mb-1">
                <b-card-header header-tag="header" class="p-1" role="tab">
                  <b-button block v-b-toggle.accordion-3 variant="info"
                    >Accordion 3</b-button
                  >
                </b-card-header>
                <b-collapse
                  id="accordion-3"
                  accordion="my-accordion"
                  role="tabpanel"
                >
                  <b-card-body>
                    <b-card-text>{{ text }}</b-card-text>
                  </b-card-body>
                </b-collapse>
              </b-card>
            </div> -->

            <!-- <b-card class="btnGroup">
              <b-button variant="outline-primary">数据选取</b-button>
              <b-button variant="outline-primary">参考选取</b-button>
              <b-button variant="outline-primary">保存</b-button>
              <b-button variant="danger">分析</b-button>
            </b-card> -->

            <!-- <b-card class="analysisConfig" title="">
                <b-table hover :items="inputs" :fields="inputs_fields">
                  <template v-slot:cell(数值)="">
                    <b-form-input size="sm"></b-form-input>
                  </template>
                  <template v-slot:cell(操作)="row">
                    <b-button
                      @click="delConfig(row)"
                      size="sm"
                      variant="outline-danger"
                      >删除</b-button
                    >
                  </template>
                </b-table>
                <b-button
                  size="sm"
                  style="float: right; margin-right: 10px"
                  variant="outline-success"
                  @click="addConfig"
                  >增加</b-button
                >
              </b-card> -->
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
import XLSX from 'xlsx'
export default {
  name: 'Desc01',
  components: { BreadCrumb },
  data() {
    return {
      breadCrumb: [
        { href: '', name: '传感染mNGS临床检测分析', isActive: true }
      ],
      basicForm: {
        name: '',
        age: '',
        gender: '',
        no: '',
        samType: '',
        reportType: ''
      },
      projectSelected: [],
      projectList: [],
      project_fields: ['选择', '客户/代理/销售名称', '客户编号', '诺因编号', '样本类型'],
      inputs_fields: ['参数名', '数值', '操作'],
      inputs: [
        { 参数名: 'MQ' },
        { 参数名: 'BQ' },
        { 参数名: 'AD' }
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
  methods: {
    clearFiles() {
      this.$refs['file-proj'].reset()
    },
    projOnSelect() {
      const proj = this.projectSelected[0]
      this.basicForm = {
        name: proj['客户/代理/销售名称'],
        age: proj['年龄'],
        gender: proj['性别'],
        no: proj['诺因编号'],
        samType: proj['样本类型'],
        reportType: proj['报告版式']
      }
      console.log(this.basicForm)

      this.$refs['proj-modal'].hide()
    },
    readExcel(e) {
      const files = e.target.files
      const fileReader = new FileReader()
      fileReader.onload = ev => {
        try {
          const data = ev.target.result
          const workbook = XLSX.read(data, { type: 'binary' })
          const sheet = workbook.SheetNames[0] // 取第一张表 Sheet1
          const ws = XLSX.utils.sheet_to_json(workbook.Sheets[sheet]) // 生成json表格内容
          this.projectList = []
          ws.forEach((item) => { this.projectList.push(item) })
          // console.log(this.projectList)
          // this.projectList = ws
          const selectButton = document.querySelector('#selectProj')
          selectButton.click()
        } catch (e) {
          return false
        }
      }
      fileReader.readAsBinaryString(files[0])
    },
    onRowSelected(items) {
      this.projectSelected = items
    },
    parseBasicData(file) {
      console.log(file)
    },
    delConfig(row) {
      this.inputs.splice(row.index, 1)
    },
    addConfig(row) {
      this.inputs.push({ 参数名: 'AD' })
    }
  }
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
  // border: 2px solid rgba(0, 0, 0, 0.125);
  .card-body {
    .ways {
      text-align: center;
      button {
        margin: 0 30px;
      }
    }
    .basicInfo {
      max-width: 50%;
      float: left;
      margin-left: 50px;
      margin-right: 50px;
      margin-bottom: 40px;
    }
    .btnGroup {
      max-width: 40%;
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
