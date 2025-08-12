# Ghibli Image Generator Project Structure

This document outlines the complete file and directory structure of the Ghibli Image Generator project, along with a brief description of each component.

```
ghibli-image-generator
├── DEPLOYMENT.md
├── DEPLOYMENT_GUIDE.md
├── LICENSE
├── README.md
├── backend
│   ├── README.md
│   ├── app.py
│   ├── requirements-hf.txt
│   ├── requirements.txt
│   └── src
│       ├── __init__.py
│       ├── __pycache__
│       ├── database
│       │   └── app.db
│       ├── main.py
│       ├── models
│       │   ├── __pycache__
│       │   └── user.py
│       ├── routes
│       │   ├── __pycache__
│       │   ├── ghibli.py
│       │   └── user.py
│       └── static
│           ├── assets
│           │   ├── index-B2__64WI.js
│           │   └── index-BqbC0PZJ.css
│           ├── favicon.ico
│           └── index.html
├── frontend
│   ├── components.json
│   ├── eslint.config.js
│   ├── index.html
│   ├── jsconfig.json
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── public
│   │   └── favicon.ico
│   ├── src
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── assets
│   │   │   ├── react.svg
│   │   │   └── test-landscape.jpg
│   │   ├── components
│   │   │   └── ui
│   │   │       ├── accordion.jsx
│   │   │       ├── alert-dialog.jsx
│   │   │       ├── alert.jsx
│   │   │       ├── aspect-ratio.jsx
│   │   │       ├── avatar.jsx
│   │   │       ├── badge.jsx
│   │   │       ├── breadcrumb.jsx
│   │   │       ├── button.jsx
│   │   │       ├── calendar.jsx
│   │   │       ├── card.jsx
│   │   │       ├── carousel.jsx
│   │   │       ├── chart.jsx
│   │   │       ├── checkbox.jsx
│   │   │       ├── collapsible.jsx
│   │   │       ├── command.jsx
│   │   │       ├── context-menu.jsx
│   │   │       ├── dialog.jsx
│   │   │       ├── drawer.jsx
│   │   │       ├── dropdown-menu.jsx
│   │   │       ├── form.jsx
│   │   │       ├── hover-card.jsx
│   │   │       ├── input-otp.jsx
│   │   │       ├── input.jsx
│   │   │       ├── label.jsx
│   │   │       ├── menubar.jsx
│   │   │       ├── navigation-menu.jsx
│   │   │       ├── pagination.jsx
│   │   │       ├── popover.jsx
│   │   │       ├── progress.jsx
│   │   │       ├── radio-group.jsx
│   │   │       ├── resizable.jsx
│   │   │       ├── scroll-area.jsx
│   │   │       ├── select.jsx
│   │   │       ├── separator.jsx
│   │   │       ├── sheet.jsx
│   │   │       ├── sidebar.jsx
│   │   │       ├── skeleton.jsx
│   │   │       ├── slider.jsx
│   │   │       ├── sonner.jsx
│   │   │       ├── switch.jsx
│   │   │       ├── table.jsx
│   │   │       ├── tabs.jsx
│   │   │       ├── textarea.jsx
│   │   │       ├── toggle-group.jsx
│   │   │       ├── toggle.jsx
│   │   │       └── tooltip.jsx
│   │   ├── hooks
│   │   │   └── use-mobile.js
│   │   ├── index.css
│   │   ├── lib
│   │   │   └── utils.js
│   │   └── main.jsx
│   └── vite.config.js
├── todo.md
└── vercel.json
```

## Root Directory Files

- `DEPLOYMENT.md`: (Deprecated, replaced by `DEPLOYMENT_GUIDE.md`) Contains general deployment instructions.
- `DEPLOYMENT_GUIDE.md`: Comprehensive guide for deploying the application to specific platforms like Hugging Face Spaces, Vercel, and Netlify.
- `LICENSE`: The MIT License file, specifying the terms under which the project is distributed.
- `README.md`: The main project README file, providing an overview, features, technology stack, setup instructions, and API endpoints.
- `todo.md`: An internal file used by the agent to track task progress.
- `vercel.json`: Configuration file for Vercel deployments, defining build commands, output directories, and environment variables.

## Backend Directory (`ghibli-image-generator/backend/`)

- `README.md`: Specific README for the Hugging Face Spaces deployment, including metadata for the Space.
- `app.py`: The main application file for Hugging Face Spaces, implementing the Gradio interface for the Ghibli image conversion.
- `requirements-hf.txt`: Python dependencies specifically for the Hugging Face Spaces environment.
- `requirements.txt`: Python dependencies for the Flask backend, used in local development and other deployments.
- `src/`: Source code directory for the Flask backend.
  - `__init__.py`: Initializes the `src` directory as a Python package.
  - `__pycache__/`: Directory for Python bytecode cache files.
  - `database/`: Directory for database files.
    - `app.db`: SQLite database file.
  - `main.py`: The main Flask application entry point for local development and Render deployment.
  - `models/`: Contains database models.
    - `__pycache__/`: Directory for Python bytecode cache files.
    - `user.py`: Defines the User database model.
  - `routes/`: Contains API route definitions.
    - `__pycache__/`: Directory for Python bytecode cache files.
    - `ghibli.py`: Defines the API endpoint for Ghibli image conversion.
    - `user.py`: Defines API endpoints for user management (template).
  - `static/`: This directory will contain the built frontend files when deployed with the Flask backend.
    - `assets/`: Contains static assets for the frontend (e.g., JavaScript and CSS bundles).
      - `index-B2__64WI.js`: Frontend JavaScript bundle.
      - `index-BqbC0PZJ.css`: Frontend CSS bundle.
    - `favicon.ico`: Favicon for the web application.
    - `index.html`: The main HTML file for the frontend, served by the Flask backend.

## Frontend Directory (`ghibli-image-generator/frontend/`)

- `components.json`: Configuration file for `shadcn/ui` components.
- `eslint.config.js`: ESLint configuration file for code linting.
- `index.html`: The main HTML file for the React application.
- `jsconfig.json`: JavaScript configuration file for VS Code and other IDEs.
- `package.json`: Node.js project configuration, including scripts and dependencies.
- `pnpm-lock.yaml`: Lock file generated by pnpm, ensuring consistent dependency installations.
- `public/`: Directory for static assets that are served directly.
  - `favicon.ico`: Favicon for the web application.
- `src/`: Source code directory for the React frontend.
  - `App.css`: Custom CSS for the application, including gradient backgrounds and animations.
  - `App.jsx`: The main React component, containing the UI logic for the Ghibli image generator.
  - `assets/`: Contains static assets like images.
    - `react.svg`: Default React logo SVG.
    - `test-landscape.jpg`: An example image used for testing.
  - `components/`: Contains React components.
    - `ui/`: Directory for `shadcn/ui` components (e.g., `button.jsx`, `card.jsx`, etc.). These are generated using the `shadcn/ui` CLI.
  - `hooks/`: Contains custom React hooks.
    - `use-mobile.js`: A custom hook for mobile detection.
  - `index.css`: Global CSS styles.
  - `lib/`: Contains utility functions.
    - `utils.js`: Utility functions for the frontend.
  - `main.jsx`: The entry point for the React application.
- `vite.config.js`: Vite configuration file for the React project.

This comprehensive structure provides a clear overview of the project and its components. Let me know if you need any specific file content or further details!

