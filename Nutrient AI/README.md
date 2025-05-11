# 🍎 Nutrient AI - Your Personal Nutrition Assistant

Nutrient AI is an intelligent nutrition assistant powered by artificial intelligence that helps users create personalized meal plans, generate food imagery, and receive tailored nutritional advice based on their specific needs.

## 🌟 Features

### 1. AI-Powered Nutrition Chat
- Interactive chat interface with a professional nutritionist AI
- Personalized dietary advice and recommendations
- Memory-enabled conversations for context-aware responses

### 2. Food Image Generation
- Create beautiful, high-quality food imagery
- Multiple style options (Photorealistic, Art illustration, Cartoon, Watercolor)
- Advanced prompt builder for detailed image customization
- Image gallery to save and view generated images

### 3. Personalized Meal Plan Generator
- Create meal plans based on specific nutrient deficiencies
- Customizable duration (3, 5, or 7 days)
- Support for dietary restrictions and preferences
- Detailed recipes with ingredients, instructions, and nutritional benefits
- Option to generate images for each meal

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- OpenAI API key
- Required Python packages (see Installation)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nutrient-ai.git
cd nutrient-ai
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run App.py
```

2. Open your web browser and navigate to:
```
http://localhost:8501
```

## 💻 Usage

### Chat with AI
- Select "Chat with AI" from the sidebar
- Type your nutrition-related questions
- Receive personalized advice and recommendations

### Generate Food Images
- Select "Generate Food Image" from the sidebar
- Enter a description of the food image you want to create
- Choose image style and size
- Use the advanced prompt builder for more detailed customization
- View and download generated images

### Create Meal Plans
- Select "Meal Plan Generator" from the sidebar
- Input your nutrient deficiencies
- Specify dietary restrictions and preferences
- Choose meal plan duration and included meals
- Generate and view your personalized meal plan
- Optionally generate images for each meal

## 🛠️ Technical Details

### Built With
- Streamlit - Web application framework
- OpenAI GPT-4 - AI language model
- OpenAI DALL-E - Image generation
- Python - Programming language

### Project Structure
```
nutrient-ai/
├── App.py              # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## ⚠️ Important Notes

- This application is for informational purposes only
- Always consult with healthcare professionals for medical advice
- The AI-generated content should be used as a guide, not a replacement for professional advice

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 and DALL-E APIs
- Streamlit for the web application framework
- All contributors and users of the application 