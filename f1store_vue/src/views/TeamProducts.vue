<template>
    <div class="page-category">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h2 class="is-size-2 has-text-centered">Products</h2>
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
            teamProducts: []
        }
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
                .get(`/api/v1/products/teams/${teamSlug}/`)
                .then(response => {
                    this.teamProducts = response.data
                    document.title = teamSlug + ' | F1 Store'
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