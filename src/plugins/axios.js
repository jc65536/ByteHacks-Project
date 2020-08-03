import axioslib from 'axios'
const axios = axioslib.create({ baseURL: `http://${window.location.hostname}:5000` })

// Wrapper arround axios to add auth headers and stuff. I couldn't figure out a better way to do this...
export default {
  ...axios,
  get: (path, data, vue) => {
    const headers = (vue && vue.$store.state.jwt) ? { Authorization: `Bearer: ${vue.$store.state.jwt}` } : {}
    return axios.get(path, { params: data, headers })
  },
  post: (path, data, vue) => {
    const headers = (vue && vue.$store.state.jwt) ? { Authorization: `Bearer: ${vue.$store.state.jwt}` } : {}
    return axios.post(path, data, { headers })
  }
}
