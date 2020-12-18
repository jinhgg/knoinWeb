<template>
  <div>
    <bread-crumb :breadCrumb="breadCrumb" />
    <b-card no-body>
      <b-tabs card>
        <b-tab title="分析结果" active>
          <b-table stacked :items="items_01"></b-table>
        </b-tab>
        <b-tab title="生成报告">
          <b-card-body>
            <ul class="progressbar">
              <li :class="{ active: step > 0 }">选择模板</li>
              <li :class="{ active: step > 1 }">筛选数据</li>
              <li :class="{ active: step > 2 }">生成报告</li>
            </ul>
            <div class="template select" v-show="step === 0">
              <!-- <b-form-radio-group
                  v-model="selected_template"
                  :options="options"
                  name="radios-stacked"
                  stacked
                ></b-form-radio-group> -->
              <b-form-group label="选择报告模板">
                <b-form-radio
                  v-model="selected_template"
                  name="template"
                  value="001"
                  >lung-report-001</b-form-radio
                >
                <b-form-radio
                  v-model="selected_template"
                  name="template"
                  value="002"
                  >lung-report-002</b-form-radio
                >
              </b-form-group>
              <b-button @click="step += 1" variant="success"> 下一步 </b-button>
            </div>
            <div class="data select" v-show="step === 1">
              <div class="tableWrapper">
                <b-table
                  ref="selectableTable_01"
                  selectable
                  :items="items_01"
                  :fields="fields"
                  @row-selected="onRowSelected_01"
                  responsive="sm"
                  caption-top
                >
                  <template #table-caption>SNV/InDel</template>
                  <template #cell(selected)="{ rowSelected }">
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
                <b-button size="sm" @click="selectAllRows_01">
                  {{ selected_01.length === items_01.length ? "取消" : "全选" }}
                </b-button>
              </div>

              <div class="tableWrapper">
                <b-table
                  ref="selectableTable_02"
                  selectable
                  :items="items_02"
                  :fields="fields"
                  @row-selected="onRowSelected_02"
                  responsive="sm"
                  caption-top
                >
                  <template #table-caption>融合基因</template>
                  <template #cell(selected)="{ rowSelected }">
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
                <b-button size="sm" @click="selectAllRows_02">
                  {{ selected_02.length === items_02.length ? "取消" : "全选" }}
                </b-button>
              </div>
              <div class="tableWrapper">
                <b-table
                  ref="selectableTable_03"
                  selectable
                  :items="items_03"
                  :fields="fields"
                  @row-selected="onRowSelected_03"
                  responsive="sm"
                  caption-top
                >
                  <template #table-caption>CNV</template>
                  <template #cell(selected)="{ rowSelected }">
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
                <b-button size="sm" @click="selectAllRows_03">
                  {{ selected_03.length === items_03.length ? "取消" : "全选" }}
                </b-button>
              </div>
              <b-button @click="step -= 1" variant="success"> 上一步 </b-button>
              <b-button @click="step += 1" variant="success"> 下一步 </b-button>
            </div>
            <div class="template select" v-show="step === 2">
              <h2>预览界面</h2>
              <b-button @click="step -= 1" variant="success"> 上一步 </b-button>
              <b-button variant="danger"> 生成报告 </b-button>
            </div>
          </b-card-body>
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import BreadCrumb from '@/components/BreadCrumb.vue'

export default {
  name: 'Result',
  components: { BreadCrumb },
  data() {
    return {
      breadCrumb: [
        { href: '/project-01', name: '传感染mNGS临床检测分析', isActive: false },
        { href: '', name: '结果', isActive: true }
      ],
      step: 0,
      selected_template: '001',
      fields: ['selected', 'isActive', 'age', 'first_name', 'last_name'],
      items_01: [
        { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
        { isActive: false, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
        { isActive: false, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
        { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
      ],
      items_02: [
        { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
        { isActive: false, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
        { isActive: false, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
        { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
      ],
      items_03: [
        { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
        { isActive: false, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
        { isActive: false, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
        { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
      ],
      selected_01: [],
      selected_02: [],
      selected_03: []

    }
  },
  mounted() {

  },
  methods: {
    selectAllRows_01() {
      const curTable = this.$refs.selectableTable_01
      if (curTable.items.length === this.selected_01.length) {
        curTable.clearSelected()
      } else {
        curTable.selectAllRows()
      }
    },
    selectAllRows_02() {
      const curTable = this.$refs.selectableTable_02
      if (curTable.items.length === this.selected_02.length) {
        curTable.clearSelected()
      } else {
        curTable.selectAllRows()
      }
    },
    selectAllRows_03() {
      const curTable = this.$refs.selectableTable_03
      if (curTable.items.length === this.selected_03.length) {
        curTable.clearSelected()
      } else {
        curTable.selectAllRows()
      }
    },
    onRowSelected_01(item) {
      this.selected_01 = item
    },
    onRowSelected_02(item) {
      this.selected_02 = item
    },
    onRowSelected_03(item) {
      this.selected_03 = item
    }
  }
}
</script>

<style lang="less" scoped>
.select {
  margin: 0 auto;
  padding-top: 120px;
  text-align: center;
}
.data {
  padding-top: 100px;
  text-align: center;
  .tableWrapper {
    display: inline-block;
    margin-bottom: 20px;
    text-align: left;
  }
}
.table-responsive-sm {
  margin: 0 15px;
  margin-bottom: 20px;
  // width:25%;
}

.progressbar {
  counter-reset: step;
}
.progressbar li {
  float: left;
  width: 33.3%;
  position: relative;
  text-align: center;
}
.progressbar li::before {
  content: counter(step);
  counter-increment: step;
  margin: 0 auto;
  width: 30px;
  height: 30px;
  border: 2px solid #ddd;
  display: block;
  text-align: center;
  line-height: 26px;
  border-radius: 50%;
  margin-bottom: 10px;
  background-color: #fff;
}
.progressbar li:not(:last-child):after {
  content: "";
  width: 100%;
  height: 1px;
  position: absolute;
  top: 15px;
  background-color: #ddd;
  left: 50%;
  margin-left: 15px;
}
.progressbar li.active::before {
  color: green;
  border-color: green;
}
.progressbar li.active {
  color: green;
}
.progressbar li.active::after {
  background-color: green;
}
</style>
