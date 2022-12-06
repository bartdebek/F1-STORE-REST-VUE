<template>
 <div class="page-product">
        <div class="columns is-multiline">
            <div class="column is-7">
                <figure class="image mb-6">
                    <img v-bind:src="product.get_image">
                </figure>

                <h1 class="title">{{ product.name }}</h1>

                <p>{{ product.description }}</p>
            </div>

            <div class="column is-3">
                <h2 class="subtitle">Information</h2>

                <p><strong>Price: </strong>${{ product.price }}</p>

                <div class="field has-addons mt-6">
                    <div class="control">
                        <input type="number" class="input" min="1" v-model="quantity">
                    </div>

                    <div class="control">
                        <a class="button is-dark" @click="addToCart()">Add to cart</a>
                    </div>
                </div>
                <h2 class="subtitle">Reviews</h2>
                <ul>
                    <li v-for="review in reviews">
                        <strong>{{ review.body }}</strong>
                        <div class="is-size-7">
                            {{ review.author_name }}<br>
                            {{ review.time }}
                        </div>
                        <hr>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
    name: 'Product',
    data() {
        return {
            product: {},
            quantity: 1,
            reviews: []
        }
    },
    mounted() {
        this.getProduct()
        this.getReviews()
    }, 
    methods: {
        async getProduct() {
            this.$store.commit('setIsLoading', true)

            const category_slug = this.$route.params.category_slug
            const product_slug = this.$route.params.product_slug

            await axios
                .get(`api/v1/products/${category_slug}/${product_slug}/`)
                .then(response => {
                    this.product = response.data
                    document.title = this.product.name + ' | F1 Store'
                })
                .catch(error => {
                    console.log(error)
                })

                this.$store.commit('setIsLoading', false)
        },
        addToCart() {
            if (isNaN(this.quantity) || this.quantity < 1) {
                this.quantity = 1
            }
            const item = {
                product: this.product,
                quantity: this.quantity
            }
            this.$store.commit('addToCart', item)
            toast({
                message: 'The product was added to the cart',
                type: 'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration: 4000,
                position: 'bottom-right',
            })
        },
        async getReviews() {
            this.$store.commit('setIsLoading', true)

            const product_slug = this.$route.params.product_slug

            await axios
                .get(`api/v1/reviews/${product_slug}/`)
                .then(response => {
                    this.reviews = response.data
                })
                .catch(error => {
                    console.log(error)
                })

                this.$store.commit('setIsLoading', false)
        },
    }
}



</script>