//  import isValidJWT from '../util/auth'
import axios from 'axios'

export const state = () => ({
  jwt: '',
  userData: {}
})

export const mutations = {
  setJWT (state, token) {
    localStorage.setItem('jwt', token)
    state.jwt = token
  },
  setUserData (state, data) {
    state.userData = data
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
    })
    .catch((err) => {
      return { registered: false, message: err }
    })
  },
}

export const getters = {
  JWTProperty: state => (prop) => {
    return JSON.parse(atob(state.jwt.split('.')[1]))[prop] // decode property from jwt
  },
  isValidJson: (state) => {
    const jwt = state.jwt
    if (!jwt || jwt.split('.').length < 3) {
      return false
    }
    const data = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    return now < exp
  }
}
