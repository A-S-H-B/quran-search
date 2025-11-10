import streamlit as st
import pandas as pd
import time
import convert_numbers
from collections import Counter

st.set_page_config(page_title="Quran Text Search", page_icon="☪️", layout='wide')
st.header('Quran Text Search')

st.markdown("Simple text search web app of the Holy Quran")

quran = 'quran.txt'
quran_english = 'quran_pickthall.txt'
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
quran_chapters_en = {
    1: "Al-Fatiha",
    2: "Al-Baqarah",
    3: "Aal-E-Imran",
    4: "An-Nisa",
    5: "Al-Ma'idah",
    6: "Al-An'am",
    7: "Al-A'raf",
    8: "Al-Anfal",
    9: "At-Tawbah",
    10: "Yunus",
    11: "Hud",
    12: "Yusuf",
    13: "Ar-Ra'd",
    14: "Ibrahim",
    15: "Al-Hijr",
    16: "An-Nahl",
    17: "Al-Isra",
    18: "Al-Kahf",
    19: "Maryam",
    20: "Ta-Ha",
    21: "Al-Anbiya",
    22: "Al-Hajj",
    23: "Al-Mu'minun",
    24: "An-Nur",
    25: "Al-Furqan",
    26: "Ash-Shu'ara",
    27: "An-Naml",
    28: "Al-Qasas",
    29: "Al-Ankabut",
    30: "Ar-Rum",
    31: "Luqman",
    32: "As-Sajda",
    33: "Al-Ahzab",
    34: "Saba",
    35: "Fatir",
    36: "Ya-Sin",
    37: "As-Saffat",
    38: "Sad",
    39: "Az-Zumar",
    40: "Ghafir",
    41: "Fussilat",
    42: "Ash-Shura",
    43: "Az-Zukhruf",
    44: "Ad-Dukhan",
    45: "Al-Jathiya",
    46: "Al-Ahqaf",
    47: "Muhammad",
    48: "Al-Fath",
    49: "Al-Hujurat",
    50: "Qaf",
    51: "Adh-Dhariyat",
    52: "At-Tur",
    53: "An-Najm",
    54: "Al-Qamar",
    55: "Ar-Rahman",
    56: "Al-Waqia",
    57: "Al-Hadid",
    58: "Al-Mujadila",
    59: "Al-Hashr",
    60: "Al-Mumtahana",
    61: "As-Saff",
    62: "Al-Jumu'a",
    63: "Al-Munafiqun",
    64: "At-Taghabun",
    65: "At-Talaq",
    66: "At-Tahrim",
    67: "Al-Mulk",
    68: "Al-Qalam",
    69: "Al-Haqqa",
    70: "Al-Ma'arij",
    71: "Nuh",
    72: "Al-Jinn",
    73: "Al-Muzzammil",
    74: "Al-Muddathir",
    75: "Al-Qiyama",
    76: "Al-Insan",
    77: "Al-Mursalat",
    78: "An-Naba",
    79: "An-Naziat",
    80: "Abasa",
    81: "At-Takwir",
    82: "Al-Infitar",
    83: "Al-Mutaffifin",
    84: "Al-Inshiqaq",
    85: "Al-Buruj",
    86: "At-Tariq",
    87: "Al-A'la",
    88: "Al-Ghashiya",
    89: "Al-Fajr",
    90: "Al-Balad",
    91: "Ash-Shams",
    92: "Al-Lail",
    93: "Ad-Duha",
    94: "Ash-Sharh",
    95: "At-Tin",
    96: "Al-Alaq",
    97: "Al-Qadr",
    98: "Al-Bayyina",
    99: "Az-Zalzala",
    100: "Al-Adiyat",
    101: "Al-Qari'a",
    102: "At-Takathur",
    103: "Al-Asr",
    104: "Al-Humaza",
    105: "Al-Fil",
    106: "Quraish",
    107: "Al-Ma'un",
    108: "Al-Kawthar",
    109: "Al-Kafiroon",
    110: "An-Nasr",
    111: "Al-Masad",
    112: "Al-Ikhlas",
    113: "Al-Falaq",
    114: "An-Nas"
}
quran_chapters_meanings = {
    1: "The Opening",
    2: "The Cow",
    3: "The Family of Imran",
    4: "The Women",
    5: "The Table Spread",
    6: "The Cattle",
    7: "The Heights",
    8: "The Spoils of War",
    9: "The Repentance",
    10: "Jonah",
    11: "Hud",
    12: "Joseph",
    13: "The Thunder",
    14: "Abraham",
    15: "The Rocky Tract",
    16: "The Bee",
    17: "The Night Journey",
    18: "The Cave",
    19: "Mary",
    20: "Ta-Ha",
    21: "The Prophets",
    22: "The Pilgrimage",
    23: "The Believers",
    24: "The Light",
    25: "The Criterion",
    26: "The Poets",
    27: "The Ant",
    28: "The Stories",
    29: "The Spider",
    30: "The Romans",
    31: "Luqman",
    32: "The Prostration",
    33: "The Confederates",
    34: "Sheba",
    35: "The Originator",
    36: "Ya-Sin",
    37: "Those Who Set the Ranks",
    38: "Sad",
    39: "The Groups",
    40: "The Forgiver",
    41: "Explained in Detail",
    42: "The Consultation",
    43: "The Gold Adornments",
    44: "The Smoke",
    45: "The Kneeling",
    46: "The Wind-Curved Sandhills",
    47: "Muhammad",
    48: "The Victory",
    49: "The Rooms",
    50: "Qaf",
    51: "The Winnowing Winds",
    52: "The Mount",
    53: "The Star",
    54: "The Moon",
    55: "The Most Merciful",
    56: "The Inevitable",
    57: "The Iron",
    58: "The Pleading Woman",
    59: "The Exile",
    60: "The Woman to be Examined",
    61: "The Ranks",
    62: "The Congregation",
    63: "The Hypocrites",
    64: "Mutual Disillusion",
    65: "The Divorce",
    66: "The Prohibition",
    67: "The Sovereignty",
    68: "The Pen",
    69: "The Inevitable Reality",
    70: "The Ascending Stairways",
    71: "Noah",
    72: "The Jinn",
    73: "The Enshrouded One",
    74: "The Cloaked One",
    75: "The Resurrection",
    76: "The Human",
    77: "Those Sent Forth",
    78: "The Tidings",
    79: "Those Who Drag Forth",
    80: "He Frowned",
    81: "The Overthrowing",
    82: "The Cleaving",
    83: "The Defrauding",
    84: "The Splitting Open",
    85: "The Constellations",
    86: "The Nightcomer",
    87: "The Most High",
    88: "The Overwhelming",
    89: "The Dawn",
    90: "The City",
    91: "The Sun",
    92: "The Night",
    93: "The Morning Hours",
    94: "The Relief",
    95: "The Fig",
    96: "The Clot",
    97: "The Power",
    98: "The Clear Proof",
    99: "The Earthquake",
    100: "The Courser",
    101: "The Striking Calamity",
    102: "The Rivalry in World Increase",
    103: "The Declining Day",
    104: "The Slanderer",
    105: "The Elephant",
    106: "Quraish",
    107: "The Small Kindnesses",
    108: "The Abundance",
    109: "The Disbelievers",
    110: "The Divine Support",
    111: "The Palm Fiber",
    112: "The Sincerity",
    113: "The Daybreak",
    114: "The Mankind"
}

def load_english_translations():
    english_dict = {}
    try:
        with open(quran_english, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    chapter = parts[0]
                    verse = parts[1]
                    translation = '|'.join(parts[2:])  # Join the rest as translation text
                    key = f"{chapter}|{verse}"
                    english_dict[key] = translation
        return english_dict
    except FileNotFoundError:
        st.error("English translation file not found. Please make sure 'quran_english.txt' is in the same directory.")
        return {}
    
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
    chapter_name_en = list(quran_chapters_en.values())[chapter_number]
    verse_number_arabic = parts[1]
    verse_number = convert_numbers.arabic_to_hindi(verse_number_arabic)

    english_text = ""
    if english_dict:
        english_text = get_english_translation(parts[0], parts[1], english_dict)
    
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**Search result {result_no} found in Chapter {chapter_number}: {chapter_name_en} || سورة {chapter_name}:**")
    with c2:
        text = parts[2] + verse_number
        st.write(f"**:green[{parts[2]} (۞{verse_number}۞)]**")
        if english_text:
            st.write(f"English Translation: :green[{english_text} (۞{verse_number_arabic}۞)]")
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

def get_english_translation(chapter, verse, english_dict):
    """Get English translation for a specific chapter and verse"""
    key = f"{chapter}|{verse}"
    return english_dict.get(key, "Translation not available")

with open(quran, 'r', encoding='utf-8') as file:
    text = file.read()

english_dict = load_english_translations()

# Search functionality
st.subheader("Search here")
keyword = st.text_input("Enter a keyword or phrase to search   |   اطبع عبارة لإجراء البحث ")

if keyword:
    search_results = search_in_text(text, keyword)

    if search_results:
        no_of_occurrences = len(search_results)
        chapter_names, chapter_names_summary, chapter_counts_df = return_chapter_names_normal(search_results)
#        st.success(f"Found {no_of_occurrences} occurrence(s) of {keyword} \n\n {chapter_names_summary}")
        st.success(f"Found {no_of_occurrences} occurrence(s) of {keyword}")
        st.bar_chart(chapter_counts_df.set_index("Chapter"), color=(5,5,5))

        keyword_within_search_results = st.text_input("Enter a keyword or phrase to search within your search results   |   اطبع عبارة لإجراء بحث ضمن نتائج البحث الحالية ")
        search_results_within_search_results = search_in_search_results(search_results, keyword_within_search_results)
        no_of_occurrences2 = len(search_results_within_search_results)

        if len(keyword_within_search_results) > 0:
            chapter_names, chapter_names_summary, chapter_counts_df = return_chapter_names_within_search_results(search_results_within_search_results)

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
                    verse_number_arabic = parts[1]
                    verse_number = convert_numbers.arabic_to_hindi(verse_number_arabic)

                    english_text = ""
                    if english_dict:
                        english_text = get_english_translation(parts[0], parts[1], english_dict)
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**Search result {index + 1} found in سورة {chapter_name}:**")
                    with c2:
                        text = parts[2] + verse_number
                        st.write(f"**:green[{parts[2]} (۞{verse_number}۞)]**")
                        if english_text:
                            st.write(f"English Translation: :green[{english_text} (۞{verse_number_arabic}۞)]")
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
                    verse_number_arabic = parts[1]
                    verse_number = convert_numbers.arabic_to_hindi(verse_number_arabic)

                    english_text = get_english_translation(parts[0], parts[1], english_dict)

                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**Search result {index + 1} found in سورة {chapter_name}:**")
                    with c2:
                        text = parts[2]+verse_number
                        st.write(f"**:green[{parts[2]} (۞{verse_number}۞)]**")
                        if english_text:
                            st.write(f"English Translation: :green[{english_text} (۞{verse_number_arabic}۞)]")
                    st.write("----------------------")

    else:
        st.warning(f"Found no occurrences of {keyword}. Try to use variations or similar words")


