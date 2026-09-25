<script setup>
defineProps({
  result: { type: Object, default: null },
})
</script>
<template>
  <div v-if="result" class="order-summary">
    <div class="hero">{{ result.order_count }} 片</div>
    <ul>
      <li>净用量 {{ result.raw_count }} 片，损耗 {{ result.waste_pct }}%</li>
      <li>地面 {{ result.area_m2 }} m²，单砖 {{ result.piece_m2 }} m²</li>
      <li>旋向：<strong>{{ result.rotated ? '旋转 90° 铺' : '正向铺（不旋转）' }}</strong></li>
    </ul>
  </div>
</template>
