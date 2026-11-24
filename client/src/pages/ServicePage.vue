<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const services = ref([])
const loading = ref(false)

const serviceToAdd = ref({})
const serviceToEdit = ref({})

const serviceAddPictureRef = ref()
const serviceAddImageUrl = ref()

const serviceEditPictureRef = ref()
const serviceEditImageUrl = ref()

const pictureToView = ref({})

async function onPictureClick(picture) {
  pictureToView.value = picture
}

async function fetchServices() {
  const r = await axios.get('/api/services/');
  services.value = r.data;
}

async function serviceAddPictureChange() {
  if (serviceAddImageUrl.value) URL.revokeObjectURL(serviceAddImageUrl.value);
  serviceAddImageUrl.value = URL.createObjectURL(serviceAddPictureRef.value.files[0]);
}

async function serviceEditPictureChange() {
  if (serviceEditImageUrl.value) URL.revokeObjectURL(serviceEditImageUrl.value);
  serviceEditImageUrl.value = URL.createObjectURL(serviceEditPictureRef.value.files[0]);
}

async function onServiceAdd() {
  const formData = new FormData();
  formData.append('image', serviceAddPictureRef.value.files[0]);
  formData.set('name', serviceToAdd.value.name)
  formData.set('price', serviceToAdd.value.price)
  formData.set('duration', serviceToAdd.value.duration)

  await axios.post('/api/services/', formData)
  fetchServices()
}

async function onServiceDelete(item) {
  await axios.delete(`/api/services/${item.id}/`)
  fetchServices()
}

async function onServiceEdit(service) {
  serviceToEdit.value = { ...service };
  if (serviceEditImageUrl.value) URL.revokeObjectURL(serviceEditImageUrl.value);
  serviceEditImageUrl.value = service.image;
  if (serviceEditPictureRef.value) {
    serviceEditPictureRef.value.value = '';
  }
}

async function onServiceUpdate(params) {
  const formData = new FormData();

  formData.set('name', serviceToEdit.value.name)
  formData.set('price', serviceToEdit.value.price)
  formData.set('duration', serviceToEdit.value.duration)

  if (serviceEditPictureRef.value.files[0]) {
    formData.set('image', serviceEditPictureRef.value.files[0]);
  }

  await axios.put(`/api/services/${serviceToEdit.value.id}/`, formData);
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
          <input type="file" class="form-control" ref="serviceAddPictureRef" @change="serviceAddPictureChange">
        </div>
        <div class="col-auto">
          <img :src="serviceAddImageUrl" style="max-height: 60px;" alt="">
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div>
      <div v-for="item in services" class="item row align-items-center">
        <div class="col">
          {{ item.name }} ♡♡♡ Стоимость: {{ item.price }}, Длительность: {{ item.duration }}
        </div>
        <div style="text-align: center;">
          <img :src="item.image" alt="" style="max-height: 200px;" data-bs-target="#clickPicture" data-bs-toggle="modal"
            @click="onPictureClick(item)" />
        </div>
        <div class="col-auto">
          <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#editService"
            @click="onServiceEdit(item)">
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

  <div class="modal fade" id="editService" aria-hidden="true">
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
            <div class="col-auto">
              <input type="file" class="form-control" ref="serviceEditPictureRef" @change="serviceEditPictureChange">
            </div>
            <div class="col-auto">
              <img :src="serviceEditImageUrl" style="max-height: 60px;" alt="">
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

  <div class="modal fade" id="clickPicture" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" style="max-width: fit-content; width: auto;">
      <div class="modal-content" style="width: auto;">
        <div class="modal-body">
          <img :src="pictureToView.image" alt="" style="display: block; max-width: 500px; max-height: 500px;">
        </div>
      </div>
    </div>
  </div>
</template>

<style lange="scsss" scoped>
.item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
}
</style>
