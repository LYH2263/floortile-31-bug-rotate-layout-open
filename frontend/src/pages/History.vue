<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const expanded = ref(null)
const detail = ref(null)
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })

function orientOf(r) {
  return r.result?.rotated === true
}
async function toggle(r) {
  if (expanded.value === r.id) { expanded.value = null; detail.value = null; return }
  expanded.value = r.id
  detail.value = await getJSON(`/api/runs/${r.id}`)
}
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>片数</th><th>旋向</th><th></th></tr></thead>
      <tbody>
        <template v-for="r in items" :key="r.id">
          <tr>
            <td>{{ r.created_at?.slice(0, 19) }}</td>
            <td>{{ r.room_name }}</td>
            <td>{{ r.tile_name }}</td>
            <td>{{ r.result?.order_count }}</td>
            <td>{{ orientOf(r) ? '旋转 90°' : '正向铺' }}</td>
            <td><button class="link-btn" @click="toggle(r)">{{ expanded === r.id ? '收起' : '详情' }}</button></td>
          </tr>
          <tr v-if="expanded === r.id && detail" class="detail-row">
            <td colspan="6">
              <ul>
                <li>当时旋向：<strong>{{ orientOf(detail) ? '旋转 90°' : '正向铺（不旋转）' }}</strong></li>
                <li>下单片数（order）：{{ detail.result?.order_count }}，净用量：{{ detail.result?.raw_count }}，损耗：{{ detail.result?.waste_pct }}%</li>
                <li v-if="detail.result?.layout">
                  当时网格（layout）：{{ detail.result.layout.cols }} 列 × {{ detail.result.layout.rows }} 行，共 {{ detail.result.layout.grid_count }} 块
                </li>
              </ul>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
