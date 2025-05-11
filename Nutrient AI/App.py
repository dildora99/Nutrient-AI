import streamlit as st
from openai import OpenAI
import os
from typing import List
from PIL import Image
import io
import base64
import requests
from datetime import datetime

# ========== Streamlit App Configuration ==========
st.set_page_config(
    page_title="Nutrient AI System",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== Custom CSS Styling ==========
st.markdown("""
<style>
    /* Main Container Styling */
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: 2px solid #e0e0e0;
    }
    
    /* Sub-header Styling */
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 1.5rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid #e0e0e0;
    }
    
    /* Sidebar Styling */
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Chat Container Styling */
    .chat-container {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Message Styling */
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #4caf50;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Input Styling */
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 1px solid #e0e0e0;
        padding: 0.5rem;
    }
    
    /* Select Box Styling */
    .stSelectbox>div>div>div {
        border-radius: 5px;
        border: 1px solid #e0e0e0;
    }
    
    /* Image Container Styling */
    .image-container {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Card Styling */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 1rem;
        background-color: #f8f9fa;
        border-top: 1px solid #e0e0e0;
        margin-top: 2rem;
    }
    
    /* Nutrient Profile Card */
    .nutrient-profile {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Meal Plan Card */
    .meal-plan {
        background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== Initialize OpenAI Client ==========
client = OpenAI(api_key="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")

# ========== Header ==========
st.markdown('<div class="main-header">🍎 Nutrient AI 💊</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #666; margin-bottom: 2rem;">Your Personal Nutrition Assistant for Optimal Health</div>', unsafe_allow_html=True)

# ========== Sidebar ==========
with st.sidebar:
    st.markdown('<div class="sidebar-header">Navigation</div>', unsafe_allow_html=True)
    option = st.selectbox("Choose an option:", ("Chat with AI", "Generate Food Image", "Meal Plan Generator"))
    
    st.markdown("---")
    
    if st.button("Clear Conversation History"):
        st.session_state.conversation_history = []
        st.session_state.saved_images = []
    
    st.markdown("---")
    
    with st.expander("About Nutrient AI"):
        st.markdown("""
        <div style="color: #666;">
        Nutrient AI is your personal nutrition assistant that helps you:
        - Get tailored nutritional advice based on your deficiencies
        - Generate personalized meal plans
        - Create beautiful food imagery
        - Learn about healthy eating habits
        </div>
        """, unsafe_allow_html=True)

# ========== Block 1: Few-Shot Prompting Function With Memory ==========
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [
        {"role": "system", "content": """You are a professional nutritionist AI that specializes in creating meal plans based on nutrient deficiencies. 
        When users mention their nutrient deficiencies, provide:
        1. A detailed 7-day meal plan focusing on those nutrients
        2. Specific food recommendations rich in the deficient nutrients
        3. Cooking tips and preparation methods
        4. Portion sizes and serving suggestions
        Always consider dietary restrictions and preferences when making recommendations.
        Be specific, evidence-based, and practical in your suggestions."""}
    ]

if "saved_images" not in st.session_state:
    st.session_state.saved_images = []

if "meal_plans" not in st.session_state:
    st.session_state.meal_plans = []

def update_conversation(role: str, content: str):
    """Store conversation history for memory."""
    st.session_state.conversation_history.append({"role": role, "content": content})
    # Optional: Limit conversation history to last N messages
    if len(st.session_state.conversation_history) > 20:  # Keep last 20 messages
        st.session_state.conversation_history = st.session_state.conversation_history[-20:]

# ========== Block 2: Chatbot Interaction ==========
if option == "Chat with AI":
    st.markdown('<div class="sub-header">💬 Chat with the Nutrition Assistant</div>', unsafe_allow_html=True)
    
    with st.container():
        # Display conversation history in a more appealing format
        if len(st.session_state.conversation_history) > 1:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in st.session_state.conversation_history[1:]:  # Skip system message
                if msg['role'] == 'user':
                    st.markdown(f'<div class="user-message"><strong>You:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="assistant-message"><strong>AI:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # User input area
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input("Ask about nutrition, meal plans, or dietary advice:", placeholder="E.g., Can you suggest a high-protein vegetarian meal plan?")
        with col2:
            send_button = st.button("Send")
    
        if send_button and user_input:
            # Add the user's message to the conversation history
            update_conversation("user", user_input)
           
            try:
                with st.spinner("Thinking..."):
                    # Send the conversation history to the model
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=st.session_state.conversation_history
                    )
                   
                    # Extract the AI's response
                    chatbot_response = response.choices[0].message.content
                   
                    # Store the AI's response in the conversation history
                    update_conversation("assistant", chatbot_response)
                
                # Force a rerun to show the updated conversation
                st.rerun()
    
            except Exception as e:
                st.error(f"Error: {e}")

# ========== Block 3: Improved Text-to-Image Generation ==========
if option == "Generate Food Image":
    st.markdown('<div class="sub-header">🍽️ Generate Food & Nutrition Imagery</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            description = st.text_area(
                "Describe the food or nutrition image you want to generate:",
                placeholder="Example: A colorful Mediterranean salad with fresh vegetables, feta cheese, olives, and a drizzle of olive oil on a rustic wooden table",
                height=100
            )
            
            # Add presets to help users with image generation
            st.markdown("#### Quick Image Presets:")
            preset_cols = st.columns(3)
            
            preset_options = [
                "A healthy breakfast bowl with fruits, yogurt, and granola",
                "A rainbow plate of grilled vegetables with herbs",
                "A protein-rich dinner with salmon, quinoa, and green vegetables"
            ]
            
            for i, preset in enumerate(preset_options):
                if preset_cols[i % 3].button(f"Preset {i+1}"):
                    description = preset
                    st.session_state.description = preset
                    st.experimental_rerun()
                    
        with col2:
            st.markdown("#### Image Options")
            
            image_style = st.selectbox(
                "Select image style:",
                ["Photorealistic", "Art illustration", "Cartoon", "Watercolor painting"]
            )
            
            image_size = st.selectbox(
                "Select image size:",
                ["512x512", "1024x1024"]
            )
        
        # Add a detailed prompt builder
        with st.expander("Advanced Prompt Builder"):
            lighting = st.selectbox("Lighting style:", ["Natural light", "Studio lighting", "Dramatic shadows", "Soft diffused light"])
            angle = st.selectbox("Camera angle:", ["Top-down (flat lay)", "45-degree angle", "Straight on", "Close-up"])
            background = st.selectbox("Background:", ["Plain white", "Rustic wood", "Marble", "Black", "Kitchen setting"])
            
            # Update the description with selected advanced options
            if st.button("Update Prompt with Selected Options"):
                advanced_details = f" Shot with {lighting}, from a {angle} perspective, with a {background} background."
                if description:
                    description += advanced_details
                else:
                    description = f"A healthy meal plate{advanced_details}"
                st.session_state.description = description
                st.experimental_rerun()
        
        # Generate button with its own styling
        generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
        generate_button = generate_col2.button("🎨 Generate Food Image", use_container_width=True)
        
        if generate_button and description:
            try:
                with st.spinner("Creating your food masterpiece..."):
                    # Enhanced prompt for better food imagery
                    enhanced_prompt = f"High-quality food photography of {description}. {image_style} style, appetizing and detailed."
                    
                    response = client.images.generate(
                        prompt=enhanced_prompt,
                        n=1,
                        size=image_size
                    )
                    
                    image_url = response.data[0].url
                    
                    # Save image URL to session state
                    st.session_state.saved_images.append({
                        "url": image_url,
                        "description": description,
                        "style": image_style
                    })
                    
                    # Display the generated image
                    st.image(image_url, caption=f"{image_style} image of: {description}", use_column_width=True)
                    
                    # Add option to download
                    st.markdown(f"[Download Image]({image_url})")
            
            except Exception as e:
                st.error(f"Error generating image: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Gallery of previously generated images
    if st.session_state.saved_images:
        st.markdown('<div class="sub-header">🖼️ Your Image Gallery</div>', unsafe_allow_html=True)
        
        # Create a gallery layout with columns
        gallery_cols = st.columns(3)
        
        for i, img_data in enumerate(st.session_state.saved_images):
            with gallery_cols[i % 3]:
                st.image(img_data["url"], caption=f"{img_data['style']}: {img_data['description'][:50]}...", use_column_width=True)
                st.markdown(f"[Open in new tab]({img_data['url']})")

# ========== Block 4: Meal Plan Generator ==========
if option == "Meal Plan Generator":
    st.markdown('<div class="sub-header">📋 Personalized Meal Plan Generator</div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="nutrient-profile">', unsafe_allow_html=True)
            st.markdown("### Your Nutrient Profile")
            deficiencies = st.multiselect(
                "Select your nutrient deficiencies:",
                ["Iron", "Vitamin D", "Vitamin B12", "Calcium", "Magnesium", "Zinc", "Omega-3", "Protein", "Fiber", "Vitamin C"]
            )
            
            dietary_restrictions = st.multiselect(
                "Any dietary restrictions?",
                ["Vegetarian", "Vegan", "Gluten-free", "Dairy-free", "Low-carb", "Keto", "None"]
            )
            
            preferences = st.text_input("Any specific food preferences or dislikes?")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="meal-plan">', unsafe_allow_html=True)
            st.markdown("### Meal Plan Preferences")
            
            duration = st.selectbox(
                "How many days would you like the meal plan for?",
                ["3 days", "5 days", "7 days"]
            )
            
            meals_per_day = st.multiselect(
                "Which meals would you like included?",
                ["Breakfast", "Lunch", "Dinner", "Snacks"],
                default=["Breakfast", "Lunch", "Dinner"]
            )
            
            cooking_time = st.selectbox(
                "Preferred cooking time per meal:",
                ["Quick (under 15 mins)", "Moderate (15-30 mins)", "Flexible"]
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        generate_plan = st.button("Generate Meal Plan", use_container_width=True)
        
        if generate_plan and deficiencies:
            try:
                with st.spinner("Creating your personalized meal plan..."):
                    # Create a detailed prompt for the meal plan
                    meal_plan_prompt = f"""Create a detailed {duration} meal plan focusing on these nutrient deficiencies: {', '.join(deficiencies)}.
                    Dietary restrictions: {', '.join(dietary_restrictions) if dietary_restrictions else 'None'}.
                    Preferences: {preferences if preferences else 'None'}.
                    Include these meals: {', '.join(meals_per_day)}.
                    Preferred cooking time: {cooking_time}.
                    For each meal, provide:
                    1. Recipe name
                    2. Ingredients with quantities
                    3. Step-by-step instructions
                    4. Nutritional benefits
                    5. Estimated preparation time
                    Format the response in a clear, organized way."""
                    
                    # Get the meal plan from GPT-4
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": st.session_state.conversation_history[0]["content"]},
                            {"role": "user", "content": meal_plan_prompt}
                        ]
                    )
                    
                    meal_plan = response.choices[0].message.content
                    
                    # Store the meal plan
                    st.session_state.meal_plans.append({
                        "plan": meal_plan,
                        "deficiencies": deficiencies,
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
                    
                    # Display the meal plan in a styled container
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown("### Your Personalized Meal Plan")
                    st.markdown(meal_plan)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add option to generate images for each meal
                    st.markdown("### Generate Images for Your Meals")
                    if st.button("Create Meal Images", use_container_width=True):
                        # Split the meal plan into individual meals
                        meals = meal_plan.split("\n\n")
                        for meal in meals:
                            if "Recipe name:" in meal:
                                recipe_name = meal.split("Recipe name:")[1].split("\n")[0].strip()
                                try:
                                    with st.spinner(f"Generating image for {recipe_name}..."):
                                        image_response = client.images.generate(
                                            prompt=f"Professional food photography of {recipe_name}, well-lit, appetizing, high quality",
                                            n=1,
                                            size="1024x1024"
                                        )
                                        st.image(image_response.data[0].url, caption=recipe_name, use_column_width=True)
                                        st.session_state.saved_images.append({
                                            "url": image_response.data[0].url,
                                            "description": recipe_name,
                                            "style": "Photorealistic"
                                        })
                                except Exception as e:
                                    st.error(f"Error generating image for {recipe_name}: {e}")
            
            except Exception as e:
                st.error(f"Error generating meal plan: {e}")
        
        # Display previous meal plans in styled containers
        if st.session_state.meal_plans:
            st.markdown("### Previous Meal Plans")
            for i, plan_data in enumerate(st.session_state.meal_plans):
                with st.expander(f"Meal Plan {i+1} - {plan_data['date']} (Focus: {', '.join(plan_data['deficiencies'])})"):
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(plan_data["plan"])
                    st.markdown('</div>', unsafe_allow_html=True)

# ========== Footer ==========
st.markdown("""
<div class="footer">
Nutrient AI - Your personal nutrition assistant powered by artificial intelligence<br>
This application is for informational purposes only and should not replace professional medical or nutritional advice.
</div>
""", unsafe_allow_html=True)