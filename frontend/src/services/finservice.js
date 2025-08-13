// services/transactions.js
import axios from 'axios'

const API = axios
// import API from './api' // your axios instance

export async function createTransaction(transactionData) {
    const token = localStorage.getItem('token') // or however you store it
    const res = await axios.post('/student/finance/transactions', transactionData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    return res.data
  }
export async function fetchDashboardData(params = {}) {
  const token = localStorage.getItem("token"); // stored at login

  const response = await axios.get("/student/finance/dashboard", {
    headers: { Authorization: `Bearer ${token}` },
    params // This sends { from_date: ..., to_date: ... } to backend
  });

  return response.data;
}
export async function listTransactions() {
  const { data } = await API.get('/student/finance/transactions')
  return data || []
}

export async function deleteTransaction(transactionId) {
  await API.delete(`/student/finance/transactions/${transactionId}`)
}
