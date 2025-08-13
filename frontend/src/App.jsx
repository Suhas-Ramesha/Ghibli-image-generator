import { useState, useRef } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Upload, Download, Sparkles, Image as ImageIcon, Loader2 } from 'lucide-react'
import './App.css'

function App() {
  const [selectedImage, setSelectedImage] = useState(null)
  const [convertedImage, setConvertedImage] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const handleImageSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      if (file.type.startsWith('image/')) {
        const reader = new FileReader()
        reader.onload = (e) => {
          setSelectedImage({
            file: file,
            preview: e.target.result
          })
          setConvertedImage(null)
          setError(null)
        }
        reader.readAsDataURL(file)
      } else {
        setError('Please select a valid image file.')
      }
    }
  }

  const handleConvert = async () => {
    if (!selectedImage) {
      setError('Please select an image first.')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('image', selectedImage.file)

      const response = await fetch(`https://ghibli-backend-l3qt.onrender.com/api/ghibli/convert`, {
        method: 'POST',
        body: formData
      })

      const result = await response.json()

      if (result.success) {
        setConvertedImage(result.converted_image)
      } else {
        setError(result.error || 'Failed to convert image')
      }
    } catch (err) {
      setError('Network error. Please try again.')
      console.error('Conversion error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDownload = () => {
    if (convertedImage) {
      const link = document.createElement('a')
      link.href = convertedImage
      link.download = 'ghibli-style-image.png'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  const triggerFileInput = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute top-10 left-10 w-72 h-72 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-gradient-to-r from-purple-400 to-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-gradient-to-r from-pink-400 to-red-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-4000"></div>
      </div>
      
      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-6">
            <Sparkles className="w-10 h-10 text-yellow-400 animate-pulse" />
            <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-yellow-400 via-pink-400 to-purple-400 bg-clip-text text-transparent drop-shadow-lg">
              Ghibli Image Generator
            </h1>
            <Sparkles className="w-10 h-10 text-yellow-400 animate-pulse" />
          </div>
          <p className="text-xl text-gray-200 max-w-3xl mx-auto leading-relaxed">
            Transform your photos into beautiful Studio Ghibli-style artwork with the power of AI ✨
          </p>
          <div className="mt-4 inline-block px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full text-white text-sm font-medium shadow-lg">
            🎨 Powered by Advanced AI Models
          </div>
        </div>

        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Upload Section */}
            <Card className="h-fit backdrop-blur-lg bg-white/10 border-white/20 shadow-2xl">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-white">
                  <Upload className="w-6 h-6 text-cyan-400" />
                  Upload Your Image
                </CardTitle>
                <CardDescription className="text-gray-300">
                  Choose an image to transform into Ghibli style
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleImageSelect}
                  className="hidden"
                />
                
                <div 
                  onClick={triggerFileInput}
                  className="border-2 border-dashed border-cyan-400/50 rounded-xl p-8 text-center cursor-pointer hover:border-cyan-400 hover:bg-white/5 transition-all duration-300 backdrop-blur-sm"
                >
                  {selectedImage ? (
                    <div className="space-y-4">
                      <img 
                        src={selectedImage.preview} 
                        alt="Selected" 
                        className="max-w-full max-h-64 mx-auto rounded-lg shadow-lg border border-white/20"
                      />
                      <p className="text-sm text-gray-300">Click to change image</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <ImageIcon className="w-20 h-20 mx-auto text-cyan-400/70" />
                      <div>
                        <p className="text-lg font-medium text-white">Click to upload an image</p>
                        <p className="text-sm text-gray-400">PNG, JPG, GIF up to 10MB</p>
                      </div>
                    </div>
                  )}
                </div>

                <Button 
                  onClick={handleConvert}
                  disabled={!selectedImage || isLoading}
                  className="w-full bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 hover:from-cyan-600 hover:via-purple-600 hover:to-pink-600 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300"
                  size="lg"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Converting...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5 mr-2" />
                      Convert to Ghibli Style
                    </>
                  )}
                </Button>

                {error && (
                  <div className="p-4 bg-red-500/20 border border-red-500/30 rounded-lg backdrop-blur-sm">
                    <p className="text-red-200 text-sm">{error}</p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Result Section */}
            <Card className="h-fit backdrop-blur-lg bg-white/10 border-white/20 shadow-2xl">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-white">
                  <Sparkles className="w-6 h-6 text-yellow-400" />
                  Ghibli Style Result
                </CardTitle>
                <CardDescription className="text-gray-300">
                  Your transformed image will appear here
                </CardDescription>
              </CardHeader>
              <CardContent>
                {convertedImage ? (
                  <div className="space-y-4">
                    <div className="relative group">
                      <img 
                        src={convertedImage} 
                        alt="Converted to Ghibli style" 
                        className="w-full rounded-xl shadow-2xl border border-white/20 transition-transform duration-300 group-hover:scale-105"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/30 via-transparent to-transparent rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    </div>
                    <Button 
                      onClick={handleDownload}
                      className="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300"
                      size="lg"
                    >
                      <Download className="w-5 h-5 mr-2" />
                      Download Ghibli Image
                    </Button>
                  </div>
                ) : (
                  <div className="border-2 border-dashed border-yellow-400/30 rounded-xl p-12 text-center backdrop-blur-sm">
                    <Sparkles className="w-20 h-20 mx-auto text-yellow-400/50 mb-4 animate-pulse" />
                    <p className="text-gray-300">Your Ghibli-style image will appear here</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Features Section */}
          <div className="mt-20">
            <h2 className="text-3xl font-bold text-center mb-12 text-white">Why Choose Our Ghibli Generator?</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card className="text-center backdrop-blur-lg bg-white/10 border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105">
                <CardContent className="pt-8 pb-6">
                  <div className="w-16 h-16 mx-auto mb-6 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                    <Sparkles className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="font-semibold mb-3 text-white text-lg">AI-Powered</h3>
                  <p className="text-sm text-gray-300 leading-relaxed">Advanced machine learning models trained on Studio Ghibli artwork for authentic transformations</p>
                </CardContent>
              </Card>
              <Card className="text-center backdrop-blur-lg bg-white/10 border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105">
                <CardContent className="pt-8 pb-6">
                  <div className="w-16 h-16 mx-auto mb-6 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full flex items-center justify-center">
                    <Upload className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="font-semibold mb-3 text-white text-lg">Easy to Use</h3>
                  <p className="text-sm text-gray-300 leading-relaxed">Simply upload your image and let our AI do the magic - no technical knowledge required</p>
                </CardContent>
              </Card>
              <Card className="text-center backdrop-blur-lg bg-white/10 border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105">
                <CardContent className="pt-8 pb-6">
                  <div className="w-16 h-16 mx-auto mb-6 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full flex items-center justify-center">
                    <Download className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="font-semibold mb-3 text-white text-lg">High Quality</h3>
                  <p className="text-sm text-gray-300 leading-relaxed">Download your transformed images in high resolution with stunning Ghibli aesthetics</p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

