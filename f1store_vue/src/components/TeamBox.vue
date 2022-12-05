<template>
    <div class="column is-3">
        <div class="box">
          <router-link v-bind:to="team.get_absolute_url">
            <figure class="image mb-4">
                <img v-bind:src="team.get_thumbnail">
            </figure>
          </router-link>
            <router-link v-bind:to="team.get_absolute_url" class="button is-dark mt-4">View products</router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TeamBox',
    props: {
        team: Object
    }
}
</script>

<style scoped>
  .image {
    margin-top: -1.25rem;
    margin-left: -1.25rem;
    margin-right: -1.25rem;
  }
  .center {
    text-align:  center;
  }
</style>
