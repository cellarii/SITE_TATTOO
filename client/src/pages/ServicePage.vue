<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const services = ref([])
const loading = ref(false)

const serviceToAdd = ref({})
const serviceToEdit = ref({})

async function fetchServices() {
  const r = await axios.get('/api/services/');
  services.value = r.data;
}

async function onServiceAdd() {
  await axios.post('/api/services/', serviceToAdd.value)
  fetchServices()
}

async function onServiceDelete(item) {
  await axios.delete(`/api/services/${item.id}/`)
  fetchServices()
}

async function onServiceEdit(service) {
    serviceToEdit.value = { ...service };
}

async function onServiceUpdate(params) {
    const service = serviceToEdit.value;
    await axios.put(`/api/services/${serviceToEdit.value.id}/`, {
        ...service
    });
    fetchServices()
}

onBeforeMount(async () => {
  await fetchServices()
})

</script>

<template>
  <div class="p-2">
    <form @submit.prevent.stop="onServiceAdd">
      <div class="row">
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="serviceToAdd.name">
            <label for="floatingInput">Название услуги</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="number" class="form-control" v-model="serviceToAdd.price">
            <label for="floatingInput">Стоимость</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="number" class="form-control" v-model="serviceToAdd.duration">
            <label for="floatingInput">Длительность</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div>
      <div v-for="item in services" class="student-item row align-items-center">
        <div class="col">
          {{ item.name }} ♡♡♡ Стоимость: {{ item.price }}, Длительность: {{ item.duration }}
        </div>
        <div class="col-auto">
          <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#editService" @click="onServiceEdit(item)">
            <i class="bi bi-pen"></i>
          </button>
        </div>
        <div class="col-auto">
          <button class="btn btn-danger" @click="onServiceDelete(item)">
            <i class="bi bi-trash2"></i>
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="editService" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Редактирование</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col">
              <div class="form-floating">
                <input type="text" class="form-control" v-model="serviceToEdit.name">
                <label for="floatingInput">Название услуги</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <input type="number" class="form-control" v-model="serviceToEdit.price">
                <label for="floatingInput">Стоимость</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <input type="number" class="form-control" v-model="serviceToEdit.duration">
                <label for="floatingInput">Длительность</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
            @click="onServiceUpdate()">Сохранить</button>
        </div>
      </div>
    </div>
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
