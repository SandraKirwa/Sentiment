import streamlit as st
import pickle
import time
import os
import re


# Load the model
model = pickle.load(open('analysis.pkl', 'rb'))

st.title('Sentiment Analysis')

review = st.text_input('Enter your review')

submit = st.button('Predict')
def is_english_text(text):
    pattern = r'[^\x00-\x7F]+'
    return not re.search(pattern, text)
def is_digit_free_text(text):
    pattern = r'[0-9]'
    return not re.search(pattern, text)


if submit:
   if submit:
    if not review:
        st.error('Please enter some text to analyze.') 
    else:
        # remove leading and trailing spaces
        review = review.strip()

        if not review:
            st.error('Please enter some text to analyze.')
        else:
            if not is_english_text(review):
                st.error('Please enter text in English only.')
            else:
                if not  is_digit_free_text(review):
                    st.error("Input should not contain digits or numbers.")
        
                else:
                    start = time.time()
                    prediction = model.predict([review])[0]
                    end = time.time()
                    st.write('Prediction time taken:', round(end - start, 2), 'seconds')
                    st.write(prediction[0])   
                    if (prediction[0] == '0'):
                            disp = "Negative"
                            st.write(disp)              
                    else:
                            disp = "Positive"
                            st.write(disp) 
        
    #prediction = model.predict([review])[0]
   
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')      
# Define a function to store feedback in a file
def store_feedback(feedback_message):
    with open('feedback.txt', 'a') as f:
        f.write(feedback_message + '\n')

# Check if the feedback file exists, and create it if not
if not os.path.exists('feedback.txt'):
    with open('feedback.txt', 'w') as f:
        f.write('')
        

# Define a function to display the feedback form
def display_feedback_form():
    st.subheader('Provide Feedback')
    st.markdown('We appreciate your feedback on the sentiment analysis system.')

    with st.form('feedback_form'):
        feedback_text = st.text_area('Please enter your feedback:')
        st.markdown('<style>.form-class {width = 300px}</style>', unsafe_allow_html=True)
        submit_button = st.form_submit_button('Submit')

    if submit_button:
        # Process and store feedback
        feedback_message = feedback_text.strip()
        if feedback_message:
            # Store feedback in a database or file
            store_feedback(feedback_message)
            st.success('Thank you for your feedback!')
        else:
            st.warning('Please enter some feedback before submitting.')

# Display the feedback form
display_feedback_form()

