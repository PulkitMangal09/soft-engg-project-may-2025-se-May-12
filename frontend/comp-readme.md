# Component Documentation

This document provides detailed information about all reusable components in the GrowthGeine project.

## 🎨 UI Components

### AppButton

A versatile button component with multiple variants and states.

**Location**: `src/components/ui/AppButton.vue`

**Props**:
- `label` (String, required): Button text
- `variant` (String, default: 'primary'): Button style variant
  - Options: `primary`, `secondary`, `success`, `warning`, `error`
- `size` (String, default: 'md'): Button size
  - Options: `sm`, `md`, `lg`
- `icon` (String): Emoji or icon to display
- `loading` (Boolean, default: false): Show loading spinner
- `disabled` (Boolean, default: false): Disable button
- `fullWidth` (Boolean, default: false): Make button full width

**Events**:
- `@click`: Emitted when button is clicked

**Example Usage**:
```vue
<template>
  <div>
    <!-- Primary button -->
    <AppButton 
      label="Save Changes" 
      variant="primary" 
      @click="handleSave" 
    />
    
    <!-- Loading button -->
    <AppButton 
      label="Submitting..." 
      :loading="isSubmitting" 
      disabled
    />
    
    <!-- Button with icon -->
    <AppButton 
      label="Add Task" 
      icon="➕" 
      variant="success"
      size="lg"
    />
  </div>
</template>
```

### AppCard

A flexible card container for content organization.

**Location**: `src/components/ui/AppCard.vue`

**Props**:
- `title` (String): Card header title
- `subtitle` (String): Card header subtitle
- `icon` (String): Header icon
- `variant` (String, default: 'default'): Card style
  - Options: `default`, `success`, `warning`, `error`
- `padding` (String, default: 'normal'): Content padding
  - Options: `none`, `sm`, `normal`, `lg`

**Slots**:
- `default`: Main card content
- `action`: Header action buttons
- `footer`: Card footer content

**Example Usage**:
```vue
<template>
  <AppCard 
    title="Health Alert" 
    subtitle="Attention needed"
    icon="🚨" 
    variant="error"
  >
    <template #action>
      <AppButton label="View Details" size="sm" />
    </template>
    
    <p>Your blood sugar level is elevated.</p>
    
    <template #footer>
      <div class="flex justify-end">
        <AppButton label="Dismiss" variant="secondary" />
      </div>
    </template>
  </AppCard>
</template>
```

### AppInput

Form input component with validation support.

**Location**: `src/components/ui/AppInput.vue`

**Props**:
- `modelValue` (String|Number): v-model value
- `type` (String, default: 'text'): Input type
- `label` (String): Field label
- `placeholder` (String): Placeholder text
- `icon` (String): Left side icon
- `error` (String): Error message
- `hint` (String): Help text
- `required` (Boolean, default: false): Required field
- `disabled` (Boolean, default: false): Disable input

**Events**:
- `@update:modelValue`: v-model update
- `@focus`: Input focused
- `@blur`: Input blurred

**Example Usage**:
```vue
<template>
  <AppInput
    v-model="form.email"
    type="email"
    label="Email Address"
    placeholder="Enter your email"
    icon="📧"
    :error="emailError"
    required
  />
</template>

<script>
export default {
  data() {
    return {
      form: { email: '' },
      emailError: ''
    }
  }
}
</script>
```

### AppSelect

Dropdown select component.

**Location**: `src/components/ui/AppSelect.vue`

**Props**:
- `modelValue` (String|Number): v-model value
- `options` (Array, required): Option list
- `valueKey` (String, default: 'value'): Key for option value
- `labelKey` (String, default: 'label'): Key for option label
- `label` (String): Field label
- `placeholder` (String): Placeholder text
- `error` (String): Error message
- `hint` (String): Help text
- `required` (Boolean): Required field
- `disabled` (Boolean): Disable select

**Example Usage**:
```vue
<template>
  <AppSelect
    v-model="selectedRole"
    :options="roleOptions"
    label="User Role"
    placeholder="Select a role"
  />
</template>

<script>
export default {
  data() {
    return {
      selectedRole: '',
      roleOptions: [
        { value: 'student', label: 'Student' },
        { value: 'teacher', label: 'Teacher' },
        { value: 'parent', label: 'Parent' }
      ]
    }
  }
}
</script>
```

### AppModal

Modal dialog component.

**Location**: `src/components/ui/AppModal.vue`

**Props**:
- `show` (Boolean, required): Show/hide modal
- `title` (String): Modal title
- `subtitle` (String): Modal subtitle
- `size` (String, default: 'md'): Modal size
  - Options: `sm`, `md`, `lg`, `xl`
- `closeOnBackdrop` (Boolean, default: true): Close on backdrop click

**Events**:
- `@close`: Emitted when modal should close

**Slots**:
- `default`: Modal body content
- `header`: Custom header content
- `footer`: Modal footer content

**Example Usage**:
```vue
<template>
  <div>
    <AppButton label="Open Modal" @click="showModal = true" />
    
    <AppModal
      :show="showModal"
      title="Confirm Action"
      subtitle="Are you sure you want to proceed?"
      @close="showModal = false"
    >
      <p>This action cannot be undone.</p>
      
      <template #footer>
        <AppButton label="Cancel" variant="secondary" @click="showModal = false" />
        <AppButton label="Confirm" variant="error" @click="confirmAction" />
      </template>
    </AppModal>
  </div>
</template>
```

### AppBadge

Small status or category indicator.

**Location**: `src/components/ui/AppBadge.vue`

**Props**:
- `variant` (String, default: 'default'): Badge style
  - Options: `default`, `success`, `warning`, `error`, `info`
- `size` (String, default: 'md'): Badge size
  - Options: `sm`, `md`, `lg`
- `icon` (String): Badge icon
- `rounded` (Boolean, default: false): Fully rounded badge

**Example Usage**:
```vue
<template>
  <div>
    <AppBadge variant="success" icon="✅">Completed</AppBadge>
    <AppBadge variant="warning" rounded>3</AppBadge>
  </div>
</template>
```

### AppToast

Toast notification system.

**Location**: `src/components/ui/AppToast.vue`

**Usage**: Automatically displays toasts from Vuex store.

**Store Actions**:
```javascript
// Show a toast
this.$store.dispatch('ui/showToast', {
  type: 'success', // success, error, warning, info
  title: 'Success!',
  message: 'Operation completed successfully.'
})
```

## 🧭 Layout Components

### AppHeader

Application header with navigation and user menu.

**Location**: `src/components/layout/AppHeader.vue`

**Props**:
- `title` (String, required): Page title
- `subtitle` (String): Page subtitle
- `showMenuButton` (Boolean, default: true): Show hamburger menu
- `showNotifications` (Boolean, default: true): Show notification bell
- `notificationCount` (Number, default: 0): Notification count

**Example Usage**:
```vue
<template>
  <AppHeader 
    title="Student Dashboard" 
    subtitle="Welcome back!"
    :notification-count="3"
  />
</template>
```

### AppBottomNav

Bottom navigation for mobile interfaces.

**Location**: `src/components/layout/AppBottomNav.vue`

**Features**:
- Automatically adapts navigation items based on user role
- Highlights active route
- Responsive design

**Example Usage**:
```vue
<template>
  <div>
    <!-- Your page content -->
    <AppBottomNav />
  </div>
</template>
```

## 🔧 Usage Guidelines

### Global Component Registration

Some components are globally registered and can be used without importing:

```vue
<template>
  <div>
    <!-- No import needed for globally registered components -->
    <AppButton label="Click me" />
    <AppCard title="My Card">Content here</AppCard>
  </div>
</template>
```

### Local Component Usage

For components not globally registered:

```vue
<template>
  <div>
    <MyCustomComponent />
  </div>
</template>

<script>
import MyCustomComponent from '@/components/MyCustomComponent.vue'

export default {
  components: {
    MyCustomComponent
  }
}
</script>
```

### Styling Guidelines

- Use Tailwind CSS classes for styling
- Follow consistent spacing patterns
- Use design tokens defined in `tailwind.config.js`
- Prefer component variants over custom styling

### Accessibility

- All interactive components support keyboard navigation
- Proper ARIA labels are included
- Color contrast meets WCAG guidelines
- Focus states are clearly visible

## 🎨 Design Tokens

The following design tokens are available through Tailwind:

**Colors**:
- `primary-*`: Main brand colors
- `student-*`: Student theme colors
- `teacher-*`: Teacher theme colors  
- `parent-*`: Parent theme colors

**Spacing**: Standard Tailwind spacing scale
**Typography**: Inter font family with standard weights
**Shadows**: Subtle elevation system
**Border Radius**: Consistent rounding system

## 🔄 State Management

Components integrate with Vuex for:
- Authentication state
- UI state (modals, toasts, loading)
- Application data

Example:
```javascript
// In component
computed: {
  ...mapState('ui', ['loading']),
  ...mapGetters('auth', ['currentUser'])
},

methods: {
  ...mapActions('ui', ['showToast'])
}
```