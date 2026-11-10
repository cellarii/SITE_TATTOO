<script setup>
import {computed, onBeforeMount, ref} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const services = ref([])
const loading = ref(false)

const serviceToAdd = ref([])

async function fetchServices() {
  loading.value = true;
  services.value=[];
    setTimeout(async () => {
        const r = await axios.get('/api/services/');
        console.log(r.data);
        services.value = r.data;
        loading.value = false;
    }, 500)
}

async function onLoadClick(){
  await fetchServices()
}

onBeforeMount(async () => {
  await fetchServices()
})

</script>

<template>
  <div>
    <input type="text">
    <input type="text">
  </div>

  <div v-if="loading">♡♡♡Грузится♡♡♡</div>
  <div>
    <div v-for="item in services" class="student-item">
      {{ item.name }}♡♡ Стоимость: {{item.price}} Длительность: {{item.duration}} минут<br>
    </div>
    <button @click="onLoadClick">Загрузить</button>
  </div>
</template>

<style lange="scsss" scoped>
.student-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    border-radius: 8px;
}
</style>
