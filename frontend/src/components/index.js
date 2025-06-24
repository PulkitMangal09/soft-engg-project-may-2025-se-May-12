// UI Components
import AppButton from './ui/AppButton.vue'
import AppCard from './ui/AppCard.vue'
import AppInput from './ui/AppInput.vue'
import AppSelect from './ui/AppSelect.vue'
import AppModal from './ui/AppModal.vue'
import AppBadge from './ui/AppBadge.vue'
import AppToast from './ui/AppToast.vue'

export default {
    install(app) {
        // Global registration of commonly used components
        app.component('AppButton', AppButton)
        app.component('AppCard', AppCard)
        app.component('AppInput', AppInput)
        app.component('AppSelect', AppSelect)
        app.component('AppModal', AppModal)
        app.component('AppBadge', AppBadge)
        app.component('AppToast', AppToast)
    }
}