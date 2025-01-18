import streamlit as st
import pandas as pd
import time
import convert_numbers
from collections import Counter

st.set_page_config(page_title="Quran Text Search", page_icon="☪️", layout='wide')
st.header('Quran Text Search')

st.markdown("Simple text search web app of the Holy Quran")

quran = 'quran.txt'
quran_chapters = {
    1: "الفاتحة",  # Al-Fatiha
    2: "البقرة",    # Al-Baqarah
    3: "آل عمران",   # Aal-E-Imran
    4: "النساء",    # An-Nisa
    5: "المائدة",   # Al-Ma'idah
    6: "الأنعام",    # Al-An'am
    7: "الأعراف",    # Al-A'raf
    8: "الأنفال",    # Al-Anfal
    9: "التوبة",     # At-Tawbah
    10: "يونس",      # Yunus
    11: "هود",       # Hud
    12: "يوسف",      # Yusuf
    13: "الرعد",     # Ar-Ra'd
    14: "إبراهيم",    # Ibrahim
    15: "الحجر",     # Al-Hijr
    16: "النحل",     # An-Nahl
    17: "الإسراء",   # Al-Isra
    18: "الكهف",     # Al-Kahf
    19: "مريم",      # Maryam
    20: "طه",        # Ta-Ha
    21: "الأنبياء",   # Al-Anbiya
    22: "الحج",      # Al-Hajj
    23: "المؤمنون",  # Al-Mu'minun
    24: "النور",     # An-Nur
    25: "الفرقان",   # Al-Furqan
    26: "الشعراء",   # Ash-Shu'ara
    27: "النمل",     # An-Naml
    28: "القصص",     # Al-Qasas
    29: "العنكبوت",  # Al-Ankabut
    30: "الروم",     # Ar-Rum
    31: "لقمان",     # Luqman
    32: "السجدة",    # As-Sajda
    33: "الأحزاب",   # Al-Ahzab
    34: "سبأ",       # Saba
    35: "فاطر",      # Fatir
    36: "يس",        # Ya-Sin
    37: "الصافات",   # As-Saffat
    38: "ص",         # Sad
    39: "الزمر",     # Az-Zumar
    40: "غافر",      # Ghafir
    41: "فصلت",      # Fussilat
    42: "الشورى",    # Ash-Shura
    43: "الزخرف",    # Az-Zukhruf
    44: "الدخان",    # Ad-Dukhan
    45: "الجاثية",   # Al-Jathiya
    46: "الأحقاف",   # Al-Ahqaf
    47: "محمد",      # Muhammad
    48: "الفتح",     # Al-Fath
    49: "الحجرات",   # Al-Hujurat
    50: "ق",         # Qaf
    51: "الذاريات",  # Adh-Dhariyat
    52: "الطور",     # At-Tur
    53: "النجم",     # An-Najm
    54: "القمر",     # Al-Qamar
    55: "الرحمن",    # Ar-Rahman
    56: "الواقعة",   # Al-Waqia
    57: "الحديد",    # Al-Hadid
    58: "المجادلة",  # Al-Mujadila
    59: "الحشر",     # Al-Hashr
    60: "الممتحنة",  # Al-Mumtahana
    61: "الصف",      # As-Saff
    62: "الجمعة",    # Al-Jumu'a
    63: "المنافقون", # Al-Munafiqun
    64: "التغابن",   # At-Taghabun
    65: "الطلاق",    # At-Talaq
    66: "التحريم",   # At-Tahrim
    67: "الملك",     # Al-Mulk
    68: "القلم",     # Al-Qalam
    69: "الحاقة",    # Al-Haqqa
    70: "المعارج",   # Al-Ma'arij
    71: "نوح",       # Nuh
    72: "الجن",      # Al-Jinn
    73: "المزمل",    # Al-Muzzammil
    74: "المدثر",    # Al-Muddathir
    75: "القيامة",   # Al-Qiyama
    76: "الإنسان",   # Al-Insan
    77: "المرسلات",  # Al-Mursalat
    78: "النبأ",     # An-Naba
    79: "النازعات",  # An-Naziat
    80: "عبس",       # Abasa
    81: "التكوير",   # At-Takwir
    82: "الإنفطار",  # Al-Infitar
    83: "المطففين",  # Al-Mutaffifin
    84: "الإنشقاق",  # Al-Inshiqaq
    85: "البروج",    # Al-Buruj
    86: "الطارق",    # At-Tariq
    87: "الأعلى",    # Al-A'la
    88: "الغاشية",   # Al-Ghashiya
    89: "الفجر",     # Al-Fajr
    90: "البلد",     # Al-Balad
    91: "الشمس",     # Ash-Shams
    92: "الليل",     # Al-Lail
    93: "الضحى",     # Ad-Duha
    94: "الشرح",     # Ash-Sharh
    95: "التين",     # At-Tin
    96: "العلق",     # Al-Alaq
    97: "القدر",     # Al-Qadr
    98: "البينة",    # Al-Bayyina
    99: "الزلزلة",   # Az-Zalzala
    100: "العاديات", # Al-Adiyat
    101: "القارعة",  # Al-Qari'a
    102: "التكاثر",  # At-Takathur
    103: "العصر",    # Al-Asr
    104: "الهمزة",   # Al-Humaza
    105: "الفيل",    # Al-Fil
    106: "قريش",     # Quraish
    107: "الماعون",  # Al-Ma'un
    108: "الكوثر",   # Al-Kawthar
    109: "الكافرون", # Al-Kafiroon
    110: "النصر",    # An-Nasr
    111: "المسد",    # Al-Masad
    112: "الإخلاص",  # Al-Ikhlas
    113: "الفلق",    # Al-Falaq
    114: "الناس"     # An-Nas
}

def search_in_text(text, keyword):
    lines = text.split('\n')
    results = []
    for i, line in enumerate(lines, start=1):
        if keyword.lower() in line.lower():
            results.append((i, line.strip()))
    return results

def search_in_search_results(search_results, keyword):
        results = []
        for index, (line_no, content) in enumerate(search_results):
            if keyword.lower() in content:
                results.append(content)
        return results

def display_results_page(result_no, content):
    parts = content.split("|")
    chapter_number = int(parts[0]) - 1
    # chapter_name = quran_chapters.get(chapter_number, "Error obtaining chapter name")
    chapter_name = list(quran_chapters.values())[chapter_number]
    verse_number = parts[1]
    verse_number = convert_numbers.arabic_to_hindi(verse_number)
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**Search result {result_no} found in سورة {chapter_name}:**")
    with c2:
        text = parts[2] + verse_number
        st.write(f"**:green[{parts[2]} (۞{verse_number}۞)]**")
    st.write("----------------------")

def return_chapter_names_within_search_results(search_results_within_search_results):
    chapter_names = []
    for index, content in enumerate(search_results_within_search_results):
        parts = content.split("|")
        chapter_number = int(parts[0]) - 1
        chapter_name = list(quran_chapters.values())[chapter_number]
        chapter_names.append(chapter_name)
    chapter_counts = Counter(chapter_names)
    chapter_count_summary = ". ".join(f"{chapter}: {count}" for chapter, count in chapter_counts.items()) + "."
    chapter_counts_df = (
        pd.DataFrame(chapter_counts.items(), columns=["Chapter", "Count"])
        .sort_values(by="Count", ascending=False)
        .reset_index(drop=True)
    )
    return chapter_names, chapter_count_summary, chapter_counts_df

def return_chapter_names_normal(search_results):
    chapter_names = []
    for index, (line_no, content) in enumerate(search_results):
        parts = content.split("|")
        chapter_number = int(parts[0]) - 1
        chapter_name = list(quran_chapters.values())[chapter_number]
        chapter_names.append(chapter_name)
    chapter_counts = Counter(chapter_names)
    chapter_count_summary = ". ".join(f"{chapter}: {count}" for chapter, count in chapter_counts.items()) + "."
    chapter_counts_df = (
        pd.DataFrame(chapter_counts.items(), columns=["Chapter", "Count"])
        .sort_values(by="Count", ascending=False)
        .reset_index(drop=True)
    )
    return chapter_names, chapter_count_summary, chapter_counts_df

with open(quran, 'r', encoding='utf-8') as file:
    text = file.read()

# Search functionality
st.subheader("Search here")
keyword = st.text_input("Enter a keyword or phrase to search")

if keyword:
    search_results = search_in_text(text, keyword)

    if search_results:
        no_of_occurrences = len(search_results)
        chapter_names, chapter_names_summary, chapter_counts_df = return_chapter_names_normal(search_results)
#        st.success(f"Found {no_of_occurrences} occurrence(s) of {keyword} \n\n {chapter_names_summary}")
        st.success(f"Found {no_of_occurrences} occurrence(s) of {keyword}")
        st.bar_chart(chapter_counts_df.set_index("Chapter"), color=(5,5,5))

        keyword_within_search_results = st.text_input("Enter a keyword or phrase to search within your search results")
        search_results_within_search_results = search_in_search_results(search_results, keyword_within_search_results)
        no_of_occurrences2 = len(search_results_within_search_results)

        if len(keyword_within_search_results) > 0:
            chapter_names, chapter_names_summary, chapter_counts_df = return_chapter_names_within_search_results(search_results_within_search_results)

            #st.success(f"Found {len(search_results_within_search_results)} occurrence(s) of {keyword_within_search_results} within your {no_of_occurrences} search results \n\n {chapter_names_summary}")
            st.success(f"Found {len(search_results_within_search_results)} occurrence(s) of {keyword_within_search_results} within your {no_of_occurrences} search results")
            #st.bar_chart(chapter_counts_df.set_index("Chapter"), color=(5, 5, 5))
            if no_of_occurrences2 >= 20:
                num_tabs = no_of_occurrences2 // 10
                if (no_of_occurrences2 % 10) > 0:
                    num_tabs = num_tabs + 1
                tab_labels = [f"{i + 1}" for i in range(num_tabs)]
                tabs = st.tabs(tab_labels)

                for index, content in enumerate(search_results_within_search_results):
                    result_no = index + 1
                    tab_index = (result_no - 1) // 10  # Calculate which tab it belongs to (0-based index)
                    with tabs[tab_index]:
                        display_results_page(result_no, content)

            else:
                for index, content in enumerate(search_results_within_search_results):
                    parts = content.split("|")
                    chapter_number = int(parts[0]) - 1
                    chapter_name = list(quran_chapters.values())[chapter_number]
                    verse_number = parts[1]
                    verse_number = convert_numbers.arabic_to_hindi(verse_number)

                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**Search result {index + 1} found in سورة {chapter_name}:**")
                    with c2:
                        text = parts[2] + verse_number
                        st.write(f"**:green[{parts[2]} (۞{verse_number}۞)]**")
                    st.write("----------------------")
        else:
            if no_of_occurrences >= 20:
                num_tabs = no_of_occurrences // 10
                if (no_of_occurrences % 10) > 0:
                    num_tabs = num_tabs + 1
                tab_labels = [f"{i + 1}" for i in range(num_tabs)]
                tabs = st.tabs(tab_labels)

                for index, (line_no, content) in enumerate(search_results):
                    result_no = index + 1
                    tab_index = (result_no - 1) // 10  # Calculate which tab it belongs to (0-based index)
                    with tabs[tab_index]:
                        display_results_page(result_no, content)

            else:
                for index, (line_no, content) in enumerate(search_results):
                    parts = content.split("|")
                    chapter_number = int(parts[0])-1
                    #chapter_name = quran_chapters.get(chapter_number, "Error obtaining chapter name")
                    chapter_name = list(quran_chapters.values())[chapter_number]
                    verse_number = parts[1]
                    verse_number = convert_numbers.arabic_to_hindi(verse_number)

                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**Search result {index + 1} found in سورة {chapter_name}:**")
                    with c2:
                        text = parts[2]+verse_number
                        st.write(f"**:green[{parts[2]} (۞{verse_number}۞)]**")
                    st.write("----------------------")

    else:
        st.warning(f"Found no occurrences of {keyword}. Try to use variations or similar words")


