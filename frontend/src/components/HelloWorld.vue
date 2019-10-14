<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
      <v-flex>
        <!-- IMPORTANT PART! -->
<form>
          <v-text-field
            v-model="twitter_handle"
            label="Submit Twitter Handle"
            required
          ></v-text-field>
<v-btn @click="submit">submit</v-btn>
          <v-btn @click="clear">clear</v-btn>
        </form>
<br/>
        <br/>
<h1 v-if="results">Results: {{ results }}</h1>
<!-- END: IMPORTANT PART! -->
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
  import axios from 'axios'
export default {
    name: 'HelloWorld',
    data: () => ({
      twitter_handle: '',
      results : ''
    }),
    methods: {
    submit () {
      axios.post('http://127.0.0.1:5000/predict', {
        twitter_handle: this.twitter_handle
      })
      .then((response) => {
        this.results = response.data.class
      })
    },
    clear () {
      this.twitter_handle = ''
    }
  }
}
</script>
