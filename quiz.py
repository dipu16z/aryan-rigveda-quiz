import streamlit as st
import json
import time

def load_questions():
    """Loads the questions from a JSON file."""
    try:
        with open("questions.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def load_leaderboard():
    """Loads the leaderboard from a JSON file."""
    try:
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_leaderboard(leaderboard):
    """Saves the leaderboard to a JSON file."""
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file, indent=4)

def conduct_quiz():
    """Runs the interactive quiz using Streamlit with a countdown timer and improved UI."""
    st.set_page_config(page_title="UPSC Quiz", layout="wide")
    
    st.markdown("""
        <style>
            .timer {
                position: absolute;
                top: 10px;
                right: 10px;
                font-size: 20px;
                font-weight: bold;
                color: red;
            }
            .question-box {
                padding: 15px;
                border-radius: 10px;
                background-color: #f9f9f9;
                margin-bottom: 10px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📜 UPSC Quiz 🏛️")
    st.write("### Test your knowledge! 🏆")
    
    player_name = st.text_input("👤 Enter your name and press Enter:")
    
    if player_name:
        questions = load_questions()
        total_time = len(questions) * 15  # 15 seconds per question
        start_time = time.time()
        end_time = start_time + total_time
        responses = {}
        
        timer_placeholder = st.empty()
        
        st.write("### 📖 Answer the following questions:")
        
        for index, q in enumerate(questions, start=1):
            with st.container():
                st.markdown(f"<div class='question-box'><b>{index}. {q['question']}</b></div>", unsafe_allow_html=True)
                responses[f"q{index}"] = st.radio(
                    "",
                    [f"{chr(65 + i)}. {option}" for i, option in enumerate(q['options'])],
                    index=None,
                    key=f"q{index}"
                )
        
        submit_clicked = st.button("✅ Submit Quiz")
        
        while time.time() < end_time:
            remaining_time = int(end_time - time.time())
            minutes, seconds = divmod(remaining_time, 60)
            timer_placeholder.markdown(f"<div class='timer'>⏳ Time Remaining: {minutes}:{seconds} mins</div>", unsafe_allow_html=True)
            time.sleep(1)
            if submit_clicked:
                break
        
        if time.time() >= end_time:
            st.warning("⏳ Time's Up! Auto-submitting your answers.")
            time.sleep(2)
        
        score = 0
        total_questions = len(questions)
        st.write("### 📊 Quiz Results")
        
        for index, q in enumerate(questions, start=1):
            answer = responses[f"q{index}"]
            correct_option = f"{q['answer']}. {q['options'][ord(q['answer']) - 65]}"
            
            if answer:
                selected_option = answer[0]
                if selected_option == q['answer']:
                    score += 2
                    st.success(f"✅ {index}. {q['question']} (Correct!)")
                else:
                    score -= 0.66
                    st.error(f"❌ {index}. {q['question']} (Wrong!)")
                    st.write(f"✔️ Correct Answer: {correct_option}")
            else:
                st.warning(f"⚠️ {index}. {q['question']} (Unanswered)")
                st.write(f"✔️ Correct Answer: {correct_option}")
        
        st.write(f"### 🎯 {player_name}, your final score is: **{score}/{total_questions * 2}**")
        
        leaderboard = load_leaderboard()
        leaderboard[player_name] = score
        save_leaderboard(leaderboard)
        
        st.write("## 🏆 Leaderboard:")
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
        for rank, (name, scr) in enumerate(sorted_leaderboard, start=1):
            st.write(f"{rank}. {name} - {scr} points")

if __name__ == "__main__":
    conduct_quiz()
