# GrowthGeine - Student Life Management Platform

GrowthGeine is a comprehensive platform designed to help students manage their academic tasks, finances, health, and emotional well-being while providing monitoring capabilities for parents and teachers.

## 🚀 Features

- **Multi-Role System**: Student, Parent, and Teacher dashboards
- **Task Management**: Create, assign, and track academic and personal tasks
- **Financial Literacy**: Track expenses, set savings goals, and learn money management
- **Health Monitoring**: Log diet, medications, and health conditions with parental oversight
- **Emotional Wellbeing**: Private emotional diary with AI chat support
- **Family Groups**: Connect students with parents for monitoring and support
- **Classroom Management**: Teachers can monitor student progress and assign tasks

## 🛠 Tech Stack

- **Frontend**: Vue.js 3 (Options API)
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: Vuex 4
- **Routing**: Vue Router 4
- **Icons**: Heroicons

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 16.0 or higher)
- **npm** (version 7.0 or higher)
- **Git**

You can check your versions by running:
```bash
node --version
npm --version
git --version
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/PulkitMangal09/soft-engg-project-may-2025-se-May-12.git
cd soft-engg-project-may-2025-se-May-12
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Setup Environment Variables

Create a `.env` file in the root directory (optional for now):

```bash
# API Configuration (when backend is ready)
VITE_API_URL=http://localhost:3000/api

# App Configuration
VITE_APP_NAME=GrowthGeine
VITE_APP_ENV=development
```

### 4. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### 5. Build for Production

```bash
npm run build
```

### 6. Preview Production Build

```bash
npm run preview
```

## 📁 Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── ui/              # Basic UI components (buttons, inputs, etc.)
│   └── layout/          # Layout components (header, navigation, etc.)
├── views/               # Page components
│   ├── auth/            # Authentication pages
│   ├── student/         # Student dashboard and features
│   ├── parent/          # Parent dashboard and monitoring
│   └── teacher/         # Teacher classroom management
├── router/              # Vue Router configuration
├── store/               # Vuex store modules
│   └── modules/         # Individual state modules
├── assets/              # Static assets
└── style.css           # Global styles and Tailwind imports
```

## 🎨 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint (if configured)

## 🧩 Component Usage

See [comp-readme.md](./comp-readme.md) for detailed component documentation.

## 📱 Views Documentation

See [view-readme.md](./view-readme.md) for information about all application views.

## 🔧 Development Guidelines

### Code Style

- Use Vue 3 Options API
- Follow component naming conventions (PascalCase for components)
- Use Tailwind CSS for styling
- Keep components small and focused

### Git Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes and commit: `git commit -m "Add feature description"`
3. Push to your branch: `git push origin feature/your-feature-name`
4. Create a Pull Request

### Commit Message Format

```
type(scope): description

Examples:
feat(auth): add student login functionality
fix(ui): resolve button styling issues
docs(readme): update installation instructions
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**1. Tailwind CSS not working**
```bash
# Reinstall Tailwind CSS
npm uninstall tailwindcss postcss autoprefixer
npm install -D tailwindcss@^3.4.0 postcss autoprefixer
npx tailwindcss init -p
```

**2. Module resolution errors**
- Ensure all file paths use `@/` for src directory
- Check that imported files exist
- Restart the development server

**3. Vuex store errors**
- Check that all store modules are properly imported
- Ensure store is properly initialized in main.js

### Getting Help

- Check existing [Issues](https://github.com/PulkitMangal09/soft-engg-project-may-2025-se-May-12/issues)
- Create a new issue with detailed description
- Join our development discussions

## 👥 Team

- **Project Lead**: [Pulkit Mangal](https://github.com/PulkitMangal09)
- **Frontend Dev**: [Rajnish Kumar](https://github.com/0rajnishk)
...
...

## 🗺 Roadmap

- [ ] Complete authentication system
- [ ] Implement task management for all roles
- [ ] Add financial tracking features
- [ ] Build health monitoring system
- [ ] Create emotional wellbeing tools
- [ ] Add real-time notifications
- [ ] Implement family group features
- [ ] Add mobile responsiveness
- [ ] Backend API integration

---