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
// Delete a transaction by ID
export async function deleteTransaction(transactionId) {
  const token = localStorage.getItem('token')
  const res = await API.delete(`/student/finance/transactions/${transactionId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  return res.data
}

// Update an existing transaction
export async function updateTransaction(transactionId, updatedData) {
  const token = localStorage.getItem('token') // or however you store it
  try {
    const res = await API.put(`/student/finance/transactions/${transactionId}`, updatedData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    return res.data
  } catch (err) {
    console.error('Error updating transaction:', err)
    throw err
  }
}
// export async function updateTransaction(id, data) {
//   const token = localStorage.getItem('token');
//   const { data: res } = await API.put(`/student/finance/transactions/${id}`, data, {
//     headers: { Authorization: `Bearer ${token}` }
//   });
//   return res;
// }


export async function getTransaction(transactionId) {
  const token = localStorage.getItem('token')
  const { data } = await API.get(`/student/finance/transactions/${transactionId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  return data
}

// Create a new savings goal
export async function createSavingsGoal(goalData) {
  const token = localStorage.getItem('token'); // or however you store it
  const res = await axios.post('/student/finance/savings-goals', goalData, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.data;
}

// Contribute to goal
export async function contributeToGoal(goal, amount) {
  const token = localStorage.getItem('token') // or however you store it
  try {
    const res = await API.post(`/student/finance/savings-goals/contribute/${goal}?amount=${amount}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    return res.data
  } catch (err) {
    console.error('Error updating transaction:', err)
    throw err
  }
}

// Delete goal
export async function deleteGoal(goalId) {
  const token = localStorage.getItem('token') // or however you store it
  try {
    const res = await API.delete(`/student/finance/deletegoal/${goalId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    return res.data
  } catch (err) {
    console.error('Error deleting goal:', err)
    throw err
  }
}


export async function updateGoal(goalId, updatedData) {
  try {
    const { data } = await API.put(
      `/student/finance/editgoal/${goalId}`,
      updatedData // Must be a plain object { title: "", target_amount: 100, saved_amount: 50 }
    );
    return data;
  } catch (error) {
    console.error("Failed to update goal:", error.response?.data || error);
    throw error;
  }
}