<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
const settings = ref({})
const saving = ref(false)
const msg = ref('')

onMounted(load)
async function load() {
  settings.value = await getJSON('/api/settings')
}
async function save() {
  saving.value = true
  msg.value = ''
  try {
    settings.value = await patchJSON('/api/settings', {
      default_rotated: settings.value.default_rotated === '1' || settings.value.default_rotated === true,
    })
    msg.value = '已保存：仅影响之后的新测算，历史记录不重算。'
  } catch (e) {
    msg.value = '保存失败：' + e.message
  } finally {
    saving.value = false
  }
}
</script>
<template>
  <div class="page">
    <h1>参数</h1>
    <ul>
      <li v-for="(v, k) in settings" :key="k" v-show="k !== 'default_rotated'">{{ k }}：{{ v }}</li>
    </ul>
    <label class="setting-row">
      系统默认旋向：
      <select v-model="settings.default_rotated">
        <option value="0">正向铺（不旋转）</option>
        <option value="1">旋转 90° 铺</option>
      </select>
    </label>
    <p class="hint">砖型自身旋向偏好优先于本设置；修改默认不会重算任何历史测算。</p>
    <button :disabled="saving" @click="save">{{ saving ? '保存中…' : '保存默认旋向' }}</button>
    <p v-if="msg" class="alert" :class="{ ok: msg.startsWith('已保存') }">{{ msg }}</p>
  </div>
</template>
