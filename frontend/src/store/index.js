import { createStore } from 'vuex'
import auth from './modules/auth'
import ui from './modules/ui'

export default createStore({
    modules: {
        auth,
        ui
    }
})