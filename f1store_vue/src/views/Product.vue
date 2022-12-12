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
                <h2 class="subtitle">Product available</h2>

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
                        <template v-if="review.active==true">
                            <strong>{{ review.body }}</strong>
                            <div class="is-size-7">
                                {{ review.author_name }}<br>
                                {{ review.time }}<br>
                                <!-- <div class="control">
                                    <a class="button is-danger" @click="deleteReview(review.id)">Delete review</a>
                                </div> -->
                            </div>
                            <hr>
                        </template>
                    </li>
                </ul>
                <template v-if="$store.state.isAuthenticated">
                <form v-on:submit.prevent="addReview">
                    <div class="field">
                        <label>Give us your opinion about the product</label>
                        <div class="control">
                            <textarea class="textarea" placeholder="Write a review" v-model="body">
                            </textarea>
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Post</button>
                        </div>
                    </div>
                </form>
                </template>
                <template v-else>
                    <div class="field">
                        <label>You need to be logged in to post a review.</label>
                    </div>
                </template>
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
            reviews: [],
            body: '',
            errors: []
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
        async addReview() {
            const formData = {
                body: this.body
            }
            const product_slug = this.$route.params.product_slug
            await axios
                .post(`api/v1/reviews/${product_slug}/`, formData)
                .then(
                    response => {
                        this.reviews.push(response.data),
                        toast({
                            message: 'Review will be added after verification. Thank you!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3000,
                            position: 'bottom-right',
                        })
                        this.body = ""
                    }
                )
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${error.response.data[property]}`)
                        }
                        this.body = ""
                    } else {
                        this.errors.push('Something went wrong. Please try again')
                        this.body = ""
                        console.log(JSON.stringify(error))
                    }
                })
        },
        async deleteReview(paramid) {
            const item = {
                pk: paramid,
            };
            await axios
                .delete(`api/v1/reviews/detail/${paramid}/`, item)
                .then(
                    response => {
                        this.reviews = this.reviews.filter(review => review.id !== paramid);
                        this.$forceUpdate();
                        toast({
                            message: 'Review has been deleted!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3000,
                            position: 'bottom-right',
                        })
                    }
                )
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${error.response.data[property]}`)
                        }
                        this.body = ""
                    } else {
                        this.errors.push('Something went wrong. Please try again')
                        this.body = ""
                        console.log(JSON.stringify(error))
                    }
                })
        }
    }
}



</script>