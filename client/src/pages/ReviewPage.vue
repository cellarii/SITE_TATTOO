<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const services = ref([])
const appointments = ref([])
const reviewToAdd = ref({})

const loading = ref(false)
const rating = [1, 2, 3, 4, 5]


async function fetchReviews() {
    loading.value = true;
    services.value = [];
    setTimeout(async () => {
        const r = await axios.get('/api/reviews/');
        console.log(r.data);
        services.value = r.data;
        loading.value = false;
    }, 250)
}

async function fetchAppointments() {
    const r = await axios.get('/api/appointments/')
    appointments.value = r.data
}

async function onReviewAdd() {
    await axios.post('/api/reviews/', reviewToAdd.value);
    fetchReviews()
}

async function onReviewDelete(review){
    await axios.delete(`/api/reviews/${review.id}/`);
    fetchReviews()
}

onBeforeMount(async () => {
    await fetchReviews();
    await fetchAppointments();
})

</script>

<template>
    {{ reviewToAdd }}
    <div class="p-2">
        <div>
            <div class="row">
                <div class="col">
                    <div class="form-floating">
                        <input type="" class="form-control" v-model="reviewToAdd.comment">
                        <label for="floatingInput">Комментарий</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <select class="form-select" v-model="reviewToAdd.rating">
                            <option :value="r" v-for="r in rating">{{ r }}</option>
                        </select>
                        <label for="floatingInput">Оценка</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <select class="form-select" v-model="reviewToAdd.appointment">
                            <option :value="a.id" v-for="a in appointments">{{ a.date }} {{ a.time }} {{ a.service.name
                                }}</option>
                        </select>
                        <label for="floatingInput">Запись</label>
                    </div>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary" @click="onReviewAdd">Добавить</button>
                </div>
            </div>
        </div>

        <div v-if="loading">♡♡♡Грузится♡♡♡</div>
        <div>
            <div v-for="item in services" class="student-item row align-items-center">
                <div class="col">
                    {{ item.appointment.client.username }}<br>
                    {{ item.appointment.date }}, {{ item.appointment.service.name }}<br>
                    Оценка: {{ item.rating }}<br>
                    {{ item.comment }}<br>
                </div>
                <div class="col-auto"><button class="btn btn-danger" @click="onReviewDelete(item)"><i class="bi bi-trash2"></i></button></div>
                <div class="col-auto"><button class="btn btn-success"><i class="bi bi-pen"></i></button></div>
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
