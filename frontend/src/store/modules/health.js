export default {
    namespaced: true,
    state: {
        healthData: {},
        alerts: []
    },

    mutations: {
        SET_HEALTH_DATA(state, data) {
            state.healthData = data
        },
        SET_ALERTS(state, alerts) {
            state.alerts = alerts
        }
    },

    actions: {
        async fetchHealthData({ commit }) {
            try {
                // API calls here
                commit('SET_HEALTH_DATA', {})
                commit('SET_ALERTS', [])
            } catch (error) {
                console.error('Error fetching health data:', error)
            }
        }
    }
}