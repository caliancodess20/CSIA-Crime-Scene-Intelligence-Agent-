import axios from 'axios'

// Toggle this to false once a teammate's backend route is actually live.
// Each api/*.js file below checks its own MOCK flag so you can flip them
// on one at a time as Yojit / Anwesha / Anmol / Tanya / Sanskruti ship.
export const MOCK_MODE = true

export const apiClient = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

// Small helper so mock functions can pretend to be a network call
// (keeps loading states / skeletons honest during dev).
export const fakeDelay = (ms = 400) => new Promise((res) => setTimeout(res, ms))
