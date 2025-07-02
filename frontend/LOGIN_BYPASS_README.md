# Authentication Bypass for Development

## Overview
The login functionality has been modified to bypass authentication for development purposes while the backend is not ready.

## Changes Made

### 1. LoginView.vue (`src/views/auth/LoginView.vue`)
- **Modified `handleLogin()` method**: Now calls `loginWithoutValidation` instead of the regular login action
- **Removed form validation**: Email and password fields are now optional (no `required` attribute)
- **Updated placeholders**: Changed to indicate fields are optional
- **Added development notice**: Yellow warning box informing users that authentication is bypassed
- **Updated button text**: Now shows "Sign In (Dev Mode)" to indicate development mode

### 2. Auth Store (`src/store/modules/auth.js`)
- **Added `loginWithoutValidation` action**: Creates a mock user object and sets authentication state without backend validation
- **Mock user creation**: Generates a user object with the selected role
- **Token generation**: Creates a mock token with timestamp for uniqueness

## How It Works

1. **User selects role**: On the welcome page, user selects student, teacher, or parent
2. **Navigate to login**: User is taken to the role-specific login page
3. **Bypass authentication**: Clicking "Sign In (Dev Mode)" immediately:
   - Creates a mock user with the selected role
   - Sets authentication state in Vuex store
   - Stores mock token and role in localStorage
   - Navigates to the respective dashboard

## User Flow

### Student Login
- Go to `/login/student` or select "Student" on welcome page
- Click "Sign In (Dev Mode)"
- Redirected to `/student` dashboard

### Teacher Login
- Go to `/login/teacher` or select "Teacher" on welcome page
- Click "Sign In (Dev Mode)"
- Redirected to `/teacher` dashboard

### Parent Login
- Go to `/login/parent` or select "Parent" on welcome page
- Click "Sign In (Dev Mode)"
- Redirected to `/parent` dashboard

## Development Notice
The login form displays a yellow warning box with the message:
> **Development Mode:** Authentication is bypassed. Click "Sign In" to proceed directly to the dashboard.

## Reverting Changes
When the backend is ready, revert these changes by:
1. Restore the original `handleLogin()` method in `LoginView.vue`
2. Remove the `loginWithoutValidation` action from the auth store
3. Restore form validation (add `required` attributes back)
4. Remove the development notice
5. Update button text back to "Sign In"

## Files Modified
- `src/views/auth/LoginView.vue`
- `src/store/modules/auth.js` 