<template>
    <div class="page-category">
        <div class="columns is-multiline">
            <div class="column is-12">
                <div class="container">
                    <figure class="image is-centered">
                        <img class="is-centered" v-bind:src="teamLogo">
                    </figure>
                    <router-link to="/teams" class="button is-dark is-small mt-4">Back to all teams</router-link>
                </div>
            </div>

            <ProductBox 
            v-for="product in teamProducts"
            v-bind:key="product.id"
            v-bind:product="product" />
    
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

import ProductBox from '@/components/ProductBox.vue'

export default {
    name: 'TeamProducts',
    components: {
        ProductBox
    },
    data() {
        return {
            teamProducts: [],
            teamId: '',
            teamName: '',
            teamLogo: ''
        }
    },
    async created() {
        // Getting team name from slug
        const teamSlug = this.$route.params.team_slug
        axios
        .get(`products/teams/${teamSlug}/`)
        .then(response => {
            this.teamId = response.data[0].team;
        });

        axios
        .get(`products/teams/`)
        .then(response => {
            let responseData = response.data
            responseData.forEach(team => {
                if (team.id == this.teamId) {
                    this.teamName = team.name;
                    this.teamLogo = team.get_thumbnail;
                }
            });
        });

    },
    mounted() {
        this.getTeamProducts()
    },
    watch: {
        $route(to, from) {
            if (to.name === 'TeamProducts') {
                this.getTeamProducts()
            }
        }
    },
    methods: {
        async getTeamProducts() {
            const teamSlug = this.$route.params.team_slug
            this.$store.commit('setIsLoading', true)
            axios
                .get(`products/teams/${teamSlug}/`)
                .then(response => {
                    this.teamProducts = response.data
                    document.title = this.teamName + ' | F1 Store'
                })
                .catch(error => {
                    console.log(error)
                    toast({
                        message: 'Something went wrong. Please try again.',
                        type: 'is-danger',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'bottom-right',
                    })
                })
            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>

<style scoped>
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
  }
  .image {
    height: 256px;
    width: 256px;
  }
</style>