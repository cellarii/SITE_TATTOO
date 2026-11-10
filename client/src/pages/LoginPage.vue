<script setup>
import {ref} from 'vue';
import axios from 'axios';
import useProfileStore from '@/stores/profileStore';
import { storeToRefs } from 'pinia';

const username = ref('')
const password = ref('')

const profileStore = useProfileStore();

async function onLoginClic() {
  profileStore.login(username.value, password.value);
}

</script>

<template>
  <div class="d-flex justify-content-center p-4">
    <form style="width: 350px" @submit.prevent.stop="onLoginClic">
      <div class="mb-3">
        <label class="form-label">Логин</label>
        <input v-model="username" required type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
      </div>
      <div class="mb-3">
        <label class="form-label">Пароль</label>
        <input v-model="password" required type="password" class="form-control" id="exampleInputPassword1">
      </div>
      <button class="btn btn-primary">Войти</button>
    </form>
  </div>
</template>

<style scoped>
</style>
