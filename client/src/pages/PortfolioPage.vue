<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const portfolios = ref([])
const services = ref({})
const masters = ref({})
const portfolioToAdd = ref({})
const portfolioToEdit = ref({})

const portfolioPictureRef = ref();
const portfolioAddImageUrl = ref();
const portfolioEditPictureRef = ref();
const portfolioEditImageUrl = ref();

const pictureToView = ref({})

async function onPictureClick(picture) {
    pictureToView.value = picture
}

async function fetchPortfolios() {
    const r = await axios.get('/api/portfolios/');
    console.log(r.data)
    portfolios.value = r.data;
}

async function fetchServices() {
    const r = await axios.get('/api/services/')
    services.value = r.data
}

async function fetchMasters() {
    const r = await axios.get('/api/profile/masters/')
    masters.value = r.data
}

async function portfolioAddPictureChange() {
    if (portfolioAddImageUrl.value) URL.revokeObjectURL(portfolioAddImageUrl.value);
    portfolioAddImageUrl.value = URL.createObjectURL(portfolioPictureRef.value.files[0]);
}

function portfolioEditPictureChange() {
    if (portfolioEditImageUrl.value) URL.revokeObjectURL(portfolioEditImageUrl.value);
    portfolioEditImageUrl.value = URL.createObjectURL(portfolioEditPictureRef.value.files[0]);
}

async function onPortfolioAdd() {
    const formData = new FormData();
    formData.append('image', portfolioPictureRef.value.files[0]);
    formData.set('service', portfolioToAdd.value.service)
    formData.set('master', portfolioToAdd.value.master)

    await axios.post('/api/portfolios/', formData);
    await fetchPortfolios()
}

async function onPortfolioDelete(portfolio) {
    await axios.delete(`/api/portfolios/${portfolio.id}/`);
    fetchPortfolios()
}

async function onPortfolioEdit(portfolio) {
    portfolioToEdit.value = { ...portfolio, service: portfolio.service.id, master: portfolio.master.id };
    if (portfolioEditImageUrl.value) URL.revokeObjectURL(portfolioEditImageUrl.value);
    portfolioEditImageUrl.value = portfolio.image;
    if (portfolioEditPictureRef.value) {
        portfolioEditPictureRef.value.value = '';
    }
}

async function onPortfolioUpdate(params) {
    const formData = new FormData();

    formData.set('service', portfolioToEdit.value.service);
    formData.set('master', portfolioToEdit.value.master);

    if (portfolioEditPictureRef.value.files[0]) {
        formData.set('image', portfolioEditPictureRef.value.files[0]);
    }

    await axios.patch(`/api/portfolios/${portfolioToEdit.value.id}/`, formData);
    await fetchPortfolios();
}

onBeforeMount(async () => {
    await fetchPortfolios();
    await fetchServices();
    await fetchMasters();
})

</script>

<template>
    <div class="p-2">
        <form @submit.prevent.stop="onPortfolioAdd">
            <div class="row">
                <div class="col">
                    <div class="form-floating">
                        <select class="form-select" v-model="portfolioToAdd.service" required>
                            <option :value="s.id" v-for="s in services">{{ s.name }}</option>
                        </select>
                        <label for="floatingInput">Услуга</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <select class="form-select" v-model="portfolioToAdd.master" required>
                            <option :value="m.id" v-for="m in masters">{{ m.username }}</option>
                        </select>
                        <label for="floatingInput">Мастер</label>
                    </div>
                </div>
                <div class="col-auto">
                    <input type="file" class="form-control" ref="portfolioPictureRef"
                        @change="portfolioAddPictureChange">
                </div>
                <div class="col-auto">
                    <img :src="portfolioAddImageUrl" style="max-height: 60px;" alt="">
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary">Добавить</button>
                </div>
            </div>
        </form>

        <div>
            <div v-for="item in portfolios" class="item row align-items-center">
                <div class="col">
                    Услуга: {{ item.service.name }}<br>
                    Мастер: {{ item.master.username }}<br>
                    <div style="text-align: center;">
                        <img :src="item.image" alt="" width="300" height="200" @click="onPictureClick(item)"
                            data-bs-target="#clickPicture" data-bs-toggle="modal" />
                    </div>
                </div>
                <div class="col-auto">
                    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#editPortfolio"
                        @click="onPortfolioEdit(item)">
                        <i class="bi bi-pen"></i>
                    </button>
                </div>
                <div class="col-auto">
                    <button class="btn btn-danger" @click="onPortfolioDelete(item)">
                        <i class="bi bi-trash2"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="editPortfolio" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
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
                                <select class="form-select" v-model="portfolioToEdit.service" required>
                                    <option :value="s.id" v-for="s in services">{{ s.name }}</option>
                                </select>
                                <label for="floatingInput">Услуга</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <select class="form-select" v-model="portfolioToEdit.master" required>
                                    <option :value="m.id" v-for="m in masters">{{ m.username }}</option>
                                </select>
                                <label for="floatingInput">Мастер</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <input type="file" class="form-control" ref="portfolioEditPictureRef"
                                @change="portfolioEditPictureChange">
                        </div>
                        <div class="col-auto">
                            <img :src="portfolioEditImageUrl" style="max-height: 60px;" alt="">
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                        @click="onPortfolioUpdate()">Сохранить</button>
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
