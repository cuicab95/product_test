import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import Loading from 'vue-loading-overlay';
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(Vuex)
Vue.prototype.$axios = axios

Vue.use(Loading, {
  // props
      color: 'blue'
},{
  // slots
});

Vue.filter("formatPercentage", function (value){
    if (!value) {
        value = 0
    }

    value = value * 100;
    value = Math.round(value);
    value = value + '%';
    return value;
})
// Obtenemos el valor de las cookies.
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

// Enviamos CSRFToken
axios.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');
// Vue.config.delimiters = ['[[', ']]'];  // No funciona

let VueParent = Vue.extend({
    delimiters: ['[[', ']]'],
    components:{
        Loading
    }
});



export default VueParent;

