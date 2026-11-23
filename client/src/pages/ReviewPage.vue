<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const services = ref([])
const appointments = ref([])
const reviewToAdd = ref({})
const reviewToEdit = ref({})

const rating = [1, 2, 3, 4, 5]


async function fetchReviews() {
    const r = await axios.get('/api/reviews/');
    console.log(r.data);
    services.value = r.data;
}

async function fetchAppointments() {
    const r = await axios.get('/api/appointments/')
    appointments.value = r.data
}

async function onReviewAdd() {
    await axios.post('/api/reviews/', reviewToAdd.value);
    fetchReviews()
}

async function onReviewDelete(review) {
    await axios.delete(`/api/reviews/${review.id}/`);
    fetchReviews()
}

async function onReviewEdit(review) {
    reviewToEdit.value = { ...review };
}

async function onReviewUpdate(params) {
    const { appointment, ...review } = reviewToEdit.value;
    await axios.put(`/api/reviews/${reviewToEdit.value.id}/`, {
        ...review,
        appointment: appointment.id
    });
    fetchReviews()
}

onBeforeMount(async () => {
    await fetchReviews();
    await fetchAppointments();
})

</script>

<template>
    <div class="p-2">
        <form @submit.prevent.stop="onReviewAdd">
            <div class="row">
                <div class="col">
                    <div class="form-floating">
                        <input type="" class="form-control" v-model="reviewToAdd.comment" required>
                        <label for="floatingInput">Комментарий</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <select class="form-select" v-model="reviewToAdd.rating" required>
                            <option :value="r" v-for="r in rating">{{ r }}</option>
                        </select>
                        <label for="floatingInput">Оценка</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <select class="form-select" v-model="reviewToAdd.appointment" required>
                            <option :value="a.id" v-for="a in appointments">{{ a.date }} {{ a.time }} {{ a.service.name
                            }}</option>
                        </select>
                        <label for="floatingInput">Запись</label>
                    </div>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary">Добавить</button>
                </div>
            </div>
        </form>

        <div>
            <div v-for="item in services" class="item row align-items-center">
                <div class="col">
                    {{ item.appointment.client.username }}<br>
                    {{ item.appointment.date }}, {{ item.appointment.service.name }}<br>
                    Оценка: {{ item.rating }}<br>
                    {{ item.comment }}<br>
                </div>
                <div class="col-auto">
                    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#editReview"
                        @click="onReviewEdit(item)">
                        <i class="bi bi-pen"></i>
                    </button>
                </div>
                <div class="col-auto">
                    <button class="btn btn-danger" @click="onReviewDelete(item)">
                        <i class="bi bi-trash2"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="editReview" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
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
                                <input type="" class="form-control" v-model="reviewToEdit.comment">
                                <label for="floatingInput">Комментарий</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <select class="form-select" v-model="reviewToEdit.rating">
                                    <option :value="r" v-for="r in rating">{{ r }}</option>
                                </select>
                                <label for="floatingInput">Оценка</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <select class="form-select" v-model="reviewToEdit.appointment">
                                    <option :value="a" v-for="a in appointments">{{ a.date }} {{ a.time }} {{
                                        a.service.name
                                        }}</option>
                                </select>
                                <label for="floatingInput">Запись</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onReviewUpdate()">Сохранить</button>
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
