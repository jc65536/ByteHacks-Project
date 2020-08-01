//  import isValidJWT from '../util/auth'
import axioslib from 'axios'
const axios = axioslib.create({ baseURL: 'http://localhost:5000' })

export const state = () => ({
  jwt: '',
  user: null
})

export const mutations = {
  setJWT (state, token) {
    localStorage.setItem('jwt', token)
    state.jwt = token
  },
  setUserData (state, data) {
    state.user = data
  },
  clearUser (state) {
    state.user = null
    state.jwt = null
  }
}

export const actions = {
  login (ctx, loginData) {
    return axios.post('/api/login', loginData)
    .then((res) => {
      if (!res.data.authenticated) return res.data
      ctx.commit('setJWT', res.data.token)
      ctx.commit('setUserData', {
        email: loginData.email,
        name: ctx.getters.JWTProperty('name')
      })
      return { authenticated: true }
    })
    .catch((err) => {
      return { authenticated: false, message: err }
    })
  },
  register (ctx, registerData) {
    return axios.post('/api/register', registerData)
    .then((res) => {
      if (!res.data.registered) return res.data
      return ctx.dispatch('login', registerData)
    })
    .then((res) => {
      if (!res.authenticated) return res
      return { registered: true }
    })
    .catch((err) => {
      return { registered: false, message: err }
    })
  },
  logout (ctx) {
    this.commit('clearUser')
    localStorage.clear()
    document.location.href = '/'
  }
}

export const getters = {
  JWTProperty: state => (prop) => {
    return JSON.parse(atob(state.jwt.split('.')[1]))[prop] // decode property from jwt
  },
  isValidJWT: state => (token) => {
    const jwt = state.jwt || token
    if (!jwt || jwt.split('.').length < 3) {
      return false
    }
    const data = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    return now < exp
  }
}
