import Vue from '@/js/vue-settings';
import axios from 'axios';
import _ from "lodash";

let appVue = new Vue({
  el: '#store',
  data: {
    orders: [],
    orderData: {},
    orderIdSelected: null
  },
  methods:{
    getOrdersList: async function (){
      try {
        const response = await this.$axios.get('/store/api/v1/create-order/?is_urgent=true&order_type=CD&customer_type=PTN&is_assortment=false')
        if (response.status === 200) {
          this.orders = response.data.data;
        } else {
          this.orders = []
        }

      } catch (e) {
        console.error('Error en la API', e)
      }
    },
    getOrderFromID: async function () {
      try {
        const response = await this.$axios.get('/store/api/v1/create-order/?id='+ this.orderIdSelected)
        if (response.status === 200) {
          this.orderData = response.data.data[0];
        } else {
          this.orderData = {};
        }
      } catch (e) {
        console.error('Error en la API', e)
      }
    }

  },
  mounted(){
    this.getOrdersList();
    this.orderIdSelected = _orderIdSelected;
  },
  watch:{
    orderIdSelected: function (val) {
      if(val) this.getOrderFromID();
    }
  },
});