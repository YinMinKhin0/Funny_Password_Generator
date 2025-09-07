import random
import streamlit as st

# -------------------------
# Funny password generator
# -------------------------

SPECIALS = list("!@#$%&*?+-_=~")
EMOJIS = ["😂", "🤣", "🤪", "🥳", "🍕", "🦄", "🤖", "🐱", "🐶"]

def funny_word_variants(word: str) -> list[str]:
    """Return playful variants of a word."""
    if not word:
        return [""]
    variants = [
        word,
        word.upper(),
        word.capitalize(),
        word[::-1],   # reversed
        word + "lol",
        "xX" + word + "Xx",
        word + str(random.randint(1, 99)),
    ]
    return variants

def generate_passwords(theme1, theme2, theme3, count=10, max_len=20, use_emojis=False):
    passwords = []
    for _ in range(count):
        # ensure each password uses all 3 themes
        part1 = random.choice(funny_word_variants(theme1))
        part2 = random.choice(funny_word_variants(theme2))
        part3 = random.choice(funny_word_variants(theme3))

        # shuffle their order
        parts = [part1, part2, part3]
        random.shuffle(parts)
        pw = "".join(parts)

        # sprinkle numbers and specials
        pw += str(random.randint(10, 999))
        pw += random.choice(SPECIALS)

        # optional emoji
        if use_emojis and random.random() < 0.5:
            pw += random.choice(EMOJIS)

        # trim to max length
        pw = pw[:max_len]

        # only keep if reasonable
        if len(pw) >= 6:
            passwords.append(pw)

    return passwords


# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Funny Password Generator", page_icon="🔑")

st.title("🔑 Funny Password Generator")
st.caption("Enter three themes — all three will be combined into each funny password!")

col1, col2, col3 = st.columns(3)
with col1:
    theme1 = st.text_input("Theme 1", "cat")
with col2:
    theme2 = st.text_input("Theme 2", "pizza")
with col3:
    theme3 = st.text_input("Theme 3", "dragon")

st.sidebar.header("Options")
count = st.sidebar.slider("How many passwords?", 5, 50, 10)
max_len = st.sidebar.slider("Max length", 8, 32, 20)
use_emojis = st.sidebar.checkbox("Add emoji spice", value=True)

if st.button("Generate 🎲", use_container_width=True):
    if not (theme1 and theme2 and theme3):
        st.error("Please enter all three themes!")
    else:
        pwds = generate_passwords(theme1, theme2, theme3, count, max_len, use_emojis)
        st.success(f"Here are {len(pwds)} funny passwords:")
        for p in pwds:
            st.code(p)
        st.download_button(
            "Download as .txt",
            "\n".join(pwds),
            file_name="funny_passwords.txt",
            mime="text/plain",
        )
