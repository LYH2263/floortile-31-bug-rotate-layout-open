<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const systemDefault = ref(false)
onMounted(async () => {
  const [tiles, settings] = await Promise.all([getJSON('/api/tiles'), getJSON('/api/settings')])
  items.value = tiles.items
  systemDefault.value = settings.default_rotated === '1' || settings.default_rotated === true
})

function orientLabel(t) {
  if (t.default_rotated === 1 || t.default_rotated === true) return '默认旋转 90°'
  if (t.default_rotated === 0 || t.default_rotated === false) return '默认正向铺'
  return `跟随系统（系统默认${systemDefault.value ? '旋转 90°' : '正向铺'}）`
}
</script>
<template>
  <div class="page">
    <h1>砖型库</h1>
    <div class="tile-cards">
      <div v-for="t in items" :key="t.id" class="tile-card" :class="{ dirty: t.data_quality === 'dirty' }">
        <strong>{{ t.name }}</strong>
        <span>{{ t.tile_l }} × {{ t.tile_w }} m</span>
        <span class="orient-pref">旋向偏好：{{ orientLabel(t) }}</span>
        <em v-if="t.data_quality === 'dirty'">无效规格</em>
      </div>
    </div>
  </div>
</template>
