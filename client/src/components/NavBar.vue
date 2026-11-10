<script setup>
import axios from 'axios';
import { onBeforeMount, ref } from 'vue';
import Cookies from 'js-cookie';
import useProfileStore from '@/stores/profileStore';
import { storeToRefs } from 'pinia';

const profileStore = useProfileStore();
const {
    isAuthenticated,
    userName
} = storeToRefs(profileStore)

async function onLogoutButton() {
    profileStore.logout();
}
</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Navbar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse w-100 justify-content-between" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link to="/" class="nav-link">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/login" class="nav-link">Login</router-link>
                    </li>
                    <li class="nav-item">
                        <a href="/admin" class="nav-link">Admin</a>
                    </li>
                    <li class="nav-item">
                        <router-link to="/service" class="nav-link">Service</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/appointment" class="nav-link">Appointment</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/review" class="nav-link">Review</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/portfolio" class="nav-link">Portfolio</router-link>
                    </li>
                </ul>
                <div role="search">
                    {{ userName }}
                    <button v-if="isAuthenticated" class="btn btn-outline-success" @click="onLogoutButton">
                        Выход
                    </button>
                </div>
            </div>
        </div>
        </nav>
</template>