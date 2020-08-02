import axioslib from 'axios'
const axios = axioslib.create({ baseURL: 'http://localhost:5000' })

// Wrapper arround axios to add auth headers. I couldn't figure out a better way to do this...
export default {
  ...axios,
  post: (path, data, vue) => {
    const headers = vue && vue.$store.state.jwt ? { headers: { Authorization: `Bearer: ${vue.$store.state.jwt}` } } : {}
    return axios.post(path, data, headers)
  }
}