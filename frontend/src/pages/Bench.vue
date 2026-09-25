<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
import OrderSummary from '../components/OrderSummary.vue'
import TileGridPreview from '../components/TileGridPreview.vue'

const rooms = ref([])
const tiles = ref([])
const roomId = ref(1)
const tileId = ref(1)
// '' = 跟随砖型默认（请求不带 rotated，由后端按 砖型偏好 > 系统默认 解析）
const rotated = ref('')
const result = ref(null)
const err = ref('')
const ready = ref(false)
let reqSeq = 0

onMounted(async () => {
  rooms.value = (await getJSON('/api/rooms')).items.filter(r => r.data_quality === 'clean')
  tiles.value = (await getJSON('/api/tiles')).items.filter(t => t.data_quality === 'clean')
  if (rooms.value.length) roomId.value = rooms.value[0].id
  if (tiles.value.length) tileId.value = tiles.value[0].id
  ready.value = true
  await preview()
})

// 切换砖型时旋向重置为“跟随默认”：若旋向原本非默认，由 rotated 的 watcher
// 顺带完成刷新；否则由砖型 watcher 刷新，避免并发请求竞态。
watch(tileId, async () => {
  if (!ready.value) return
  if (rotated.value !== '') rotated.value = ''
  else await preview()
})
watch(roomId, async () => { if (ready.value) await preview() })
// 旋向切换立即刷新预览与片数
watch(rotated, async () => { if (ready.value) await preview() })

function rotatedQuery() {
  return rotated.value === '' ? '' : `&rotated=${rotated.value}`
}

async function preview() {
  err.value = ''
  const seq = ++reqSeq
  try {
    const r = await getJSON(
      `/api/estimate?room_id=${roomId.value}&tile_id=${tileId.value}${rotatedQuery()}`
    )
    if (seq === reqSeq) result.value = r
  } catch (e) {
    if (seq === reqSeq) { err.value = e.message; result.value = null }
  }
}

async function saveRun() {
  err.value = ''
  try {
    const payload = {
      room_id: roomId.value,
      tile_id: tileId.value,
      save: true,
      note: '前端保存',
    }
    if (rotated.value !== '') payload.rotated = rotated.value === 'true'
    result.value = await postJSON('/api/estimate', payload)
  } catch (e) {
    err.value = e.message
  }
}
</script>
<template>
  <div class="page">
    <h1>下单测算</h1>
    <label>房间 <select v-model.number="roomId"><option v-for="r in rooms" :key="r.id" :value="r.id">{{ r.name }}</option></select></label>
    <label>砖型 <select v-model.number="tileId"><option v-for="t in tiles" :key="t.id" :value="t.id">{{ t.name }}</option></select></label>
    <label>旋向
      <select v-model="rotated">
        <option value="">跟随砖型默认</option>
        <option value="false">正向铺（不旋转）</option>
        <option value="true">旋转 90° 铺</option>
      </select>
    </label>
    <button @click="preview">试算</button>
    <button @click="saveRun">保存记录</button>
    <p v-if="err" class="alert">{{ err }}</p>
    <OrderSummary :result="result" />
    <TileGridPreview v-if="result?.layout" :cols="result.layout.cols" :rows="result.layout.rows" :grid-count="result.layout.grid_count" :rotated="result.rotated" />
  </div>
</template>
