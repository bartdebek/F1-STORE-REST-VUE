<template>
    <div class="page-my-account">
      <div class="columns is-multiline">
        <div class="column is-12">
            <h2 class="is-size-2 has-text-centered">Shop by Team</h2>
        </div>
  
        <TeamBox
          v-for="team in teamList"
          v-bind:key="team.id"
          v-bind:team="team" />
        
       </div>
    </div>
  </template>
  
  <script>
  
  import axios from 'axios'
  
  import TeamBox from '@/components/TeamBox.vue'
  
  export default {
    name: 'Teams',
    data() {
      return {
        teamList: []
      }
    },
    components: {
      TeamBox
    },
    mounted() {
      this.getTeamList() 
    },
    methods: {
      async getTeamList() {
        this.$store.commit('setIsLoading', true)
  
        await axios
          .get('https://orca-app-kgbd6.ondigitalocean.app/api/v1/products/teams/')
          .then(response => {
            this.teamList = response.data
            document.title = 'Teams | F1 Store'
          })
          .catch(error => {
            console.log(error)
          })
  
        this.$store.commit('setIsLoading', false)
      }
    }
  }
  </script>
  