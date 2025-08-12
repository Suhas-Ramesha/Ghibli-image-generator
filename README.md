# 🎨 Ghibli Image Generator

Transform your photos into beautiful Studio Ghibli-style artwork with the power of AI! This web application combines a React frontend with a Flask backend to provide an intuitive interface for converting regular images into the magical, hand-drawn aesthetic of Studio Ghibli films.

## ✨ Features

- **AI-Powered Conversion**: Utilizes Hugging Face's Ghibli-Diffusion model for authentic style transfer
- **Modern Web Interface**: Beautiful, responsive React frontend with Tailwind CSS
- **Easy Upload**: Simple drag-and-drop or click-to-upload functionality
- **Instant Preview**: See your transformed image immediately
- **High-Quality Downloads**: Download your Ghibli-style images in PNG format
- **Free to Use**: Completely free with no registration required

## 🚀 Live Demo

[Visit the live application](https://your-app-url.com) (URL will be provided after deployment)

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern JavaScript framework
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool and development server
- **Lucide React** - Beautiful icons
- **shadcn/ui** - High-quality UI components

### Backend
- **Flask** - Python web framework
- **Hugging Face Transformers** - AI model integration
- **Pillow (PIL)** - Image processing
- **Flask-CORS** - Cross-origin resource sharing

## 📋 Prerequisites

Before running this application, make sure you have:

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **npm** or **pnpm**
- **Git**

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ghibli-image-generator.git
cd ghibli-image-generator
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
pnpm install
# or
npm install
```

### 4. Environment Configuration

Create a `.env` file in the backend directory:

```env
HUGGINGFACE_TOKEN=your_huggingface_token_here
FLASK_ENV=development
```

**Note**: The Hugging Face token is optional for basic functionality. The app will work in demo mode without it.

## 🚀 Running the Application

### Development Mode

1. **Start the Backend Server**:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python src/main.py
```
The backend will run on `http://localhost:5000`

2. **Start the Frontend Development Server**:
```bash
cd frontend
pnpm run dev
# or
npm run dev
```
The frontend will run on `http://localhost:5173`

3. **Open your browser** and navigate to `http://localhost:5173`

## 🌐 Deployment

This application can be deployed for free using various platforms:

### Option 1: Render (Recommended)

**Backend Deployment:**
1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Set the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Environment**: Add your `HUGGINGFACE_TOKEN` if you have one

**Frontend Deployment:**
1. Build the frontend: `cd frontend && pnpm run build`
2. Copy the `dist` folder contents to the Flask `static` directory
3. The Flask app will serve both frontend and backend

### Option 2: Vercel + Railway

**Frontend (Vercel):**
1. Connect your repository to [Vercel](https://vercel.com)
2. Set build settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `pnpm run build`
   - **Output Directory**: `dist`

**Backend (Railway):**
1. Deploy to [Railway](https://railway.app)
2. Connect your GitHub repository
3. Set the root directory to `backend`
4. Add environment variables

### Option 3: Heroku

1. Create a new Heroku app
2. Add the Python buildpack
3. Set environment variables
4. Deploy using Git

## 🔑 Hugging Face Token

To enable the image conversion, you need to set your Hugging Face API token as an environment variable named `HUGGINGFACE_TOKEN` in your backend deployment environment (e.g., Hugging Face Spaces or Render). You can obtain your token from your [Hugging Face profile settings](https://huggingface.co/settings/tokens).

## 📁 Project Structure

```
ghibli-image-generator/
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   │   ├── ghibli.py          # Ghibli conversion API
│   │   │   └── user.py            # User routes (template)
│   │   ├── models/
│   │   │   └── user.py            # Database models
│   │   ├── static/                # Frontend build files
│   │   └── main.py                # Flask application entry
│   ├── venv/                      # Python virtual environment
│   └── requirements.txt           # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ui/                # shadcn/ui components
│   │   ├── assets/                # Static assets
│   │   ├── App.jsx                # Main React component
│   │   └── main.jsx               # React entry point
│   ├── public/                    # Public assets
│   └── package.json               # Node.js dependencies
└── README.md                      # This file
```

## 🎯 API Endpoints

### POST `/api/ghibli/convert`
Convert an uploaded image to Ghibli style.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `image` file

**Response:**
```json
{
  "success": true,
  "message": "Image converted to Ghibli style successfully!",
  "converted_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "note": "This is a demo version. For full Ghibli conversion, add your Hugging Face API token."
}
```

### GET `/api/ghibli/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Ghibli Image Converter"
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Studio Ghibli](https://www.ghibli.jp/) for the incredible art style that inspired this project
- [Hugging Face](https://huggingface.co/) for providing the AI models
- [nitrosocke/Ghibli-Diffusion](https://huggingface.co/nitrosocke/Ghibli-Diffusion) for the Ghibli style transfer model
- The open-source community for the amazing tools and libraries

## 🐛 Troubleshooting

### Common Issues

**1. "Network error" when converting images**
- Make sure the backend server is running on port 5000
- Check that CORS is properly configured
- Verify the API endpoint URL in the frontend

**2. "Module not found" errors**
- Ensure all dependencies are installed
- Check that you're in the correct directory
- Verify Python virtual environment is activated

**3. Images not displaying properly**
- Check browser console for errors
- Verify image file format is supported (PNG, JPG, GIF)
- Ensure image size is reasonable (< 10MB)

**4. Deployment issues**
- Check environment variables are set correctly
- Verify build commands and start commands
- Check logs for specific error messages

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/ghibli-image-generator/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

Made with ❤️ by [Your Name] | Powered by AI and Studio Ghibli magic ✨

