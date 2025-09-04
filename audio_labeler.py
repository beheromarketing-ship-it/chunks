import streamlit as st
import pandas as pd
import os
from pathlib import Path
import datetime

# Параметри
AUDIO_DIR = "recordings/chunks"  # Папка з chunk_*.wav
LABELS_CSV = "labels.csv"

# Завантаження списку chunk-файлів
chunk_files = sorted(Path(AUDIO_DIR).glob("chunk_*.wav"))

# Завантаження або створення таблиці з мітками
if os.path.exists(LABELS_CSV):
    df = pd.read_csv(LABELS_CSV)
else:
    df = pd.DataFrame({"filename": [f.name for f in chunk_files], "label": ["" for _ in chunk_files]})

# Ітерація по всіх файлах без мітки
for i, row in df[df['label'] == ""].iterrows():
    st.header(f"{row['filename']}")
    st.audio(str(Path(AUDIO_DIR) / row['filename']), format='audio/wav')

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔊 Loud", key=f"loud_{i}"):
            df.at[i, 'label'] = 'loud'
            df.to_csv(LABELS_CSV, index=False)
            st.experimental_rerun()
    with col2:
        if st.button("🤫 Calm", key=f"calm_{i}"):
            df.at[i, 'label'] = 'calm'
            df.to_csv(LABELS_CSV, index=False)
            st.experimental_rerun()

    break  # показуємо лише один файл за раз

# Показ завершення
if (df['label'] != "").all():
    st.success("✅ Усі фрагменти розмічені!")
    st.dataframe(df)
