<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const appointments = ref([])
const services = ref([])
const masters = ref([])
const clients = ref([])

const appointmentToAdd = ref({})
const appointmentToEdit = ref({})

async function fetchAppointments() {
    const r = await axios.get('/api/appointments/');
    appointments.value = r.data;
}

async function fetchServices() {
    const r = await axios.get('/api/services')
    console.log(r.data)
    services.value = r.data
}

async function fetchMasters() {
    const r = await axios.get('/api/profile/masters/')
    console.log(r.data)
    masters.value = r.data
}

async function fetchClients() {
    const r = await axios.get('/api/profile/clients/')
    console.log(r.data)
    clients.value = r.data
}

async function onAppoinmentAdd() {
    await axios.post('/api/appointments/', appointmentToAdd.value)
    fetchAppointments()
}

async function onAppointmentDelete(item) {
    await axios.delete(`/api/appointments/${item.id}/`)
    fetchAppointments()
}

async function onAppointmentEdit(appointment) {
    appointmentToEdit.value = {
        ...appointment,
        service: appointment.service.id,
        master: appointment.master.id,
        client: appointment.client.id,
    };
}

async function onAppointmentUpdate(params) {
    const { service, master, client, ...appointment } = appointmentToEdit.value;
    await axios.put(`/api/appointments/${appointmentToEdit.value.id}/`, {
        ...appointment,
        service: service,
        master: master,
        client: client
    });
    fetchAppointments()
}

onBeforeMount(async () => {
    await fetchAppointments()
    await fetchServices()
    await fetchMasters()
    await fetchClients()
})

</script>
<template>
    <div class="p-2">
        <form @submit.prevent.stop="onAppoinmentAdd">
            <div class="row">
                <div class="col">
                    <div class="form-floating">
                        <input type="date" step="1" class="form-control" v-model="appointmentToAdd.date">
                        <label for="floatingInput">Дата</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <input type="time" class="form-control" v-model="appointmentToAdd.time">
                        <label for="floatingInput">Время</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <select class="form-select" v-model="appointmentToAdd.service">
                            <option :value="s.id" v-for="s in services">{{ s.name }}</option>
                        </select>
                        <label for="floatingInput">Услуга</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <select class="form-select" v-model="appointmentToAdd.master">
                            <option :value="m.id" v-for="m in masters">{{ m.username }}</option>
                        </select>
                        <label for="floatingInput">Мастер</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <select class="form-select" v-model="appointmentToAdd.client">
                            <option :value="c.id" v-for="c in clients">{{ c.username }}</option>
                        </select>
                        <label for="floatingInput">Клиент</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="appointmentToAdd.comment">
                        <label for="floatingInput">Комментарий</label>
                    </div>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary">Добавить</button>
                </div>
            </div>
        </form>

        <div>
            <div v-for="item in appointments" class="item row align-items-center">
                <div class="col">
                    Дата: {{ item.date }} {{ item.time }}<br>
                    Мастер: {{ item.master.username }}<br>
                    Услуга: {{ item.service.name }}<br>
                    Клиент: {{ item.client.username }}<br>
                    <div v-if="item.comment">{{ item.comment }}</div>
                </div>
                <div class="col-auto">
                    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#editAppointment"
                        @click="onAppointmentEdit(item)">
                        <i class="bi bi-pen"></i>
                    </button>
                </div>
                <div class="col-auto">
                    <button class="btn btn-danger" @click="onAppointmentDelete(item)">
                        <i class="bi bi-trash2"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="editAppointment" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
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
                                <input type="date" step="1" class="form-control" v-model="appointmentToEdit.date">
                                <label for="floatingInput">Дата</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <input type="time" class="form-control" v-model="appointmentToEdit.time">
                                <label for="floatingInput">Время</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <select class="form-select" v-model="appointmentToEdit.service">
                                    <option :value="s.id" v-for="s in services">{{ s.name }}</option>
                                </select>
                                <label for="floatingInput">Услуга</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <select class="form-select" v-model="appointmentToEdit.master">
                                    <option :value="m.id" v-for="m in masters">{{ m.username }}</option>
                                </select>
                                <label for="floatingInput">Мастер</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <select class="form-select" v-model="appointmentToEdit.client">
                                    <option :value="c.id" v-for="c in clients">{{ c.username }}</option>
                                </select>
                                <label for="floatingInput">Клиент</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="appointmentToEdit.comment">
                                <label for="floatingInput">Комментарий</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                        @click="onAppointmentUpdate()">Сохранить</button>
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
