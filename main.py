import streamlit as st
import pandas as pd
import convert_numbers
from collections import Counter

st.set_page_config(page_title="Quran Text Search", page_icon="☪️", layout='wide')

col_title, col_lang = st.columns([6, 1])
with col_lang:
    lang = st.selectbox(
        "Language / اللغة",
        ["English", "العربية"],
        index=0,
        label_visibility="collapsed"
    )
with col_title:
    st.header(
        "Quran Text Search | البحث في نص القرآن الكريم"
    )
st.session_state["lang"] = lang

ui_strings = {
    "English": {
        "header": "Quran Text Search",
        "description": "Simple text search web app of the Holy Quran",
        "search_here": "Search here",
        "keyword_input": "Enter a keyword or phrase to search",
        "show_english": "Show English translations",
        "keyword_within": "Enter a keyword or phrase to search within your search results",
        "found_occurrences": "Found {} occurrence(s) of {}",
        "found_within": "Found {} occurrence(s) of {} within your {} search results",
        "not_found": "Found no occurrences of {}. Try to use variations or similar words",
        "chapter_prefix": "Search result {} found in Chapter {}: {} || سورة {}:",
        "pickthall": "Pickthall",
        "yusufali": "Yusuf Ali",
        "sahih": "Sahih International",
    },
    "العربية": {
        "header": "البحث في نص القرآن الكريم",
        "description": "تطبيق ويب بسيط للبحث في نص القرآن الكريم",
        "search_here": "ابحث هنا",
        "keyword_input": "أدخل كلمة أو عبارة للبحث",
        "show_english": "إظهار الترجمات الإنجليزية",
        "keyword_within": "أدخل كلمة أو عبارة للبحث ضمن نتائج البحث الحالية",
        "found_occurrences": "تم العثور على {} تكرار لـ {}",
        "found_within": "تم العثور على {} تكرار لـ {} ضمن {} نتيجة بحث",
        "not_found": "لم يتم العثور على نتائج لـ {}. جرّب كلمات مختلفة أو مشابهة",
        "chapter_prefix": "نتيجة البحث {} موجودة في السورة {}:",
        "pickthall": "بيكثال",
        "yusufali": "يوسف علي",
        "sahih": "صحيح الدولية",
    }
}
ui = ui_strings[lang]

# Apply RTL direction for Arabic interface
if lang == "العربية":
    st.markdown("""
        <style>
        .stApp {
            direction: rtl;
            text-align: right;
        }
        /* Ensure columns don't reverse order */
        .stHorizontalBlock {
            direction: ltr;
        }
        </style>
    """, unsafe_allow_html=True)

st.markdown(ui["description"])

quran = 'quran.txt'
quran_english = 'quran_pickthall.txt'
quran_english2 = 'quran_yusufali.txt'
quran_english3 = 'quran_sahih.txt'

quran_chapters = {1: "الفاتحة", 2: "البقرة", 3: "آل عمران", 4: "النساء", 5: "المائدة",
                  6: "الأنعام", 7: "الأعراف", 8: "الأنفال", 9: "التوبة", 10: "يونس",
                  11: "هود", 12: "يوسف", 13: "الرعد", 14: "إبراهيم", 15: "الحجر",
                  16: "النحل", 17: "الإسراء", 18: "الكهف", 19: "مريم", 20: "طه",
                  21: "الأنبياء", 22: "الحج", 23: "المؤمنون", 24: "النور", 25: "الفرقان",
                  26: "الشعراء", 27: "النمل", 28: "القصص", 29: "العنكبوت", 30: "الروم",
                  31: "لقمان", 32: "السجدة", 33: "الأحزاب", 34: "سبأ", 35: "فاطر",
                  36: "يس", 37: "الصافات", 38: "ص", 39: "الزمر", 40: "غافر",
                  41: "فصلت", 42: "الشورى", 43: "الزخرف", 44: "الدخان", 45: "الجاثية",
                  46: "الأحقاف", 47: "محمد", 48: "الفتح", 49: "الحجرات", 50: "ق",
                  51: "الذاريات", 52: "الطور", 53: "النجم", 54: "القمر", 55: "الرحمن",
                  56: "الواقعة", 57: "الحديد", 58: "المجادلة", 59: "الحشر", 60: "الممتحنة",
                  61: "الصف", 62: "الجمعة", 63: "المنافقون", 64: "التغابن", 65: "الطلاق",
                  66: "التحريم", 67: "الملك", 68: "القلم", 69: "الحاقة", 70: "المعارج",
                  71: "نوح", 72: "الجن", 73: "المزمل", 74: "المدثر", 75: "القيامة",
                  76: "الإنسان", 77: "المرسلات", 78: "النبأ", 79: "النازعات", 80: "عبس",
                  81: "التكوير", 82: "الإنفطار", 83: "المطففين", 84: "الإنشقاق", 85: "البروج",
                  86: "الطارق", 87: "الأعلى", 88: "الغاشية", 89: "الفجر", 90: "البلد",
                  91: "الشمس", 92: "الليل", 93: "الضحى", 94: "الشرح", 95: "التين",
                  96: "العلق", 97: "القدر", 98: "البينة", 99: "الزلزلة", 100: "العاديات",
                  101: "القارعة", 102: "التكاثر", 103: "العصر", 104: "الهمزة", 105: "الفيل",
                  106: "قريش", 107: "الماعون", 108: "الكوثر", 109: "الكافرون", 110: "النصر",
                  111: "المسد", 112: "الإخلاص", 113: "الفلق", 114: "الناس"}

quran_chapters_en = {1: "Al-Fatiha", 2: "Al-Baqarah", 3: "Aal-E-Imran", 4: "An-Nisa", 5: "Al-Ma'idah",
                     6: "Al-An'am", 7: "Al-A'raf", 8: "Al-Anfal", 9: "At-Tawbah", 10: "Yunus",
                     11: "Hud", 12: "Yusuf", 13: "Ar-Ra'd", 14: "Ibrahim", 15: "Al-Hijr",
                     16: "An-Nahl", 17: "Al-Isra", 18: "Al-Kahf", 19: "Maryam", 20: "Ta-Ha",
                     21: "Al-Anbiya", 22: "Al-Hajj", 23: "Al-Mu'minun", 24: "An-Nur", 25: "Al-Furqan",
                     26: "Ash-Shu'ara", 27: "An-Naml", 28: "Al-Qasas", 29: "Al-Ankabut", 30: "Ar-Rum",
                     31: "Luqman", 32: "As-Sajda", 33: "Al-Ahzab", 34: "Saba", 35: "Fatir",
                     36: "Ya-Sin", 37: "As-Saffat", 38: "Sad", 39: "Az-Zumar", 40: "Ghafir",
                     41: "Fussilat", 42: "Ash-Shura", 43: "Az-Zukhruf", 44: "Ad-Dukhan", 45: "Al-Jathiya",
                     46: "Al-Ahqaf", 47: "Muhammad", 48: "Al-Fath", 49: "Al-Hujurat", 50: "Qaf",
                     51: "Adh-Dhariyat", 52: "At-Tur", 53: "An-Najm", 54: "Al-Qamar", 55: "Ar-Rahman",
                     56: "Al-Waqia", 57: "Al-Hadid", 58: "Al-Mujadila", 59: "Al-Hashr", 60: "Al-Mumtahana",
                     61: "As-Saff", 62: "Al-Jumu'a", 63: "Al-Munafiqun", 64: "At-Taghabun", 65: "At-Talaq",
                     66: "At-Tahrim", 67: "Al-Mulk", 68: "Al-Qalam", 69: "Al-Haqqa", 70: "Al-Ma'arij",
                     71: "Nuh", 72: "Al-Jinn", 73: "Al-Muzzammil", 74: "Al-Muddathir", 75: "Al-Qiyama",
                     76: "Al-Insan", 77: "Al-Mursalat", 78: "An-Naba", 79: "An-Naziat", 80: "Abasa",
                     81: "At-Takwir", 82: "Al-Infitar", 83: "Al-Mutaffifin", 84: "Al-Inshiqaq", 85: "Al-Buruj",
                     86: "At-Tariq", 87: "Al-A'la", 88: "Al-Ghashiya", 89: "Al-Fajr", 90: "Al-Balad",
                     91: "Ash-Shams", 92: "Al-Lail", 93: "Ad-Duha", 94: "Ash-Sharh", 95: "At-Tin",
                     96: "Al-Alaq", 97: "Al-Qadr", 98: "Al-Bayyina", 99: "Az-Zalzala", 100: "Al-Adiyat",
                     101: "Al-Qari'a", 102: "At-Takathur", 103: "Al-Asr", 104: "Al-Humaza", 105: "Al-Fil",
                     106: "Quraish", 107: "Al-Ma'un", 108: "Al-Kawthar", 109: "Al-Kafiroon", 110: "An-Nasr",
                     111: "Al-Masad", 112: "Al-Ikhlas", 113: "Al-Falaq", 114: "An-Nas"}

quran_chapters_meanings = {1: "The Opening", 2: "The Cow", 3: "The Family of Imran", 4: "The Women", 5: "The Table Spread",
                           6: "The Cattle", 7: "The Heights", 8: "The Spoils of War", 9: "The Repentance", 10: "Jonah",
                           11: "Hud", 12: "Joseph", 13: "The Thunder", 14: "Abraham", 15: "The Rocky Tract",
                           16: "The Bee", 17: "The Night Journey", 18: "The Cave", 19: "Mary", 20: "Ta-Ha",
                           21: "The Prophets", 22: "The Pilgrimage", 23: "The Believers", 24: "The Light", 25: "The Criterion",
                           26: "The Poets", 27: "The Ant", 28: "The Stories", 29: "The Spider", 30: "The Romans",
                           31: "Luqman", 32: "The Prostration", 33: "The Confederates", 34: "Sheba", 35: "The Originator",
                           36: "Ya-Sin", 37: "Those Who Set the Ranks", 38: "Sad", 39: "The Groups", 40: "The Forgiver",
                           41: "Explained in Detail", 42: "The Consultation", 43: "The Gold Adornments", 44: "The Smoke", 45: "The Kneeling",
                           46: "The Wind-Curved Sandhills", 47: "Muhammad", 48: "The Victory", 49: "The Rooms", 50: "Qaf",
                           51: "The Winnowing Winds", 52: "The Mount", 53: "The Star", 54: "The Moon", 55: "The Most Merciful",
                           56: "The Inevitable", 57: "The Iron", 58: "The Pleading Woman", 59: "The Exile", 60: "The Woman to be Examined",
                           61: "The Ranks", 62: "The Congregation", 63: "The Hypocrites", 64: "Mutual Disillusion", 65: "The Divorce",
                           66: "The Prohibition", 67: "The Sovereignty", 68: "The Pen", 69: "The Inevitable Reality", 70: "The Ascending Stairways",
                           71: "Noah", 72: "The Jinn", 73: "The Enshrouded One", 74: "The Cloaked One", 75: "The Resurrection",
                           76: "The Human", 77: "Those Sent Forth", 78: "The Tidings", 79: "Those Who Drag Forth", 80: "He Frowned",
                           81: "The Overthrowing", 82: "The Cleaving", 83: "The Defrauding", 84: "The Splitting Open", 85: "The Constellations",
                           86: "The Nightcomer", 87: "The Most High", 88: "The Overwhelming", 89: "The Dawn", 90: "The City",
                           91: "The Sun", 92: "The Night", 93: "The Morning Hours", 94: "The Relief", 95: "The Fig",
                           96: "The Clot", 97: "The Power", 98: "The Clear Proof", 99: "The Earthquake", 100: "The Courser",
                           101: "The Striking Calamity", 102: "The Rivalry in World Increase", 103: "The Declining Day", 104: "The Slanderer",
                           105: "The Elephant", 106: "Quraish", 107: "The Small Kindnesses", 108: "The Abundance", 109: "The Disbelievers",
                           110: "The Divine Support", 111: "The Palm Fiber", 112: "The Sincerity", 113: "The Daybreak", 114: "The Mankind"}

def load_english_translations(file_path):
    english_dict = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    chapter = parts[0]
                    verse = parts[1]
                    translation = '|'.join(parts[2:])
                    key = f"{chapter}|{verse}"
                    english_dict[key] = translation
        return english_dict
    except FileNotFoundError:
        st.error(f"Translation file not found: {file_path}.")
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
    for line_no, content in search_results:
        if keyword.lower() in content:
            results.append(content)
    return results

def get_english_translation(chapter, verse, english_dict):
    key = f"{chapter}|{verse}"
    return english_dict.get(key, "Translation not available")

def display_results_page(result_no, content):
    parts = content.split("|")
    chapter_number = int(parts[0]) - 1
    chapter_name = list(quran_chapters.values())[chapter_number]
    chapter_name_en = list(quran_chapters_en.values())[chapter_number]
    verse_number_arabic = parts[1]
    verse_number = convert_numbers.arabic_to_hindi(verse_number_arabic)

    trans_pickthall = get_english_translation(parts[0], parts[1], english_dict) if english_dict else ""
    trans_yusufali = get_english_translation(parts[0], parts[1], english_dict2) if english_dict2 else ""
    trans_sahih = get_english_translation(parts[0], parts[1], english_dict3) if english_dict3 else ""

    c1, c2 = st.columns(2)
    with c1:
        if lang == "English":
            st.write(f"**{ui['chapter_prefix'].format(result_no, chapter_number, chapter_name_en, chapter_name)}:**")
        else:
            st.write(f"**{ui['chapter_prefix'].format(result_no, chapter_name)}:**")
    with c2:
        text = parts[2] + verse_number
        st.write(f"**:green[{parts[2]} (۞{verse_number}۞)]**")
        if st.session_state.show_english:
            if trans_pickthall:
                st.write(f"{ui['pickthall']}: :green[{trans_pickthall} (۞{verse_number_arabic}۞)]")
            if trans_yusufali:
                st.write(f"{ui['yusufali']}: :green[{trans_yusufali} (۞{verse_number_arabic}۞)]")
            if trans_sahih:
                st.write(f"{ui['sahih']}: :green[{trans_sahih} (۞{verse_number_arabic}۞)]")
    st.write("----------------------")

def return_chapter_names_normal(search_results):
    chapter_names = []
    for line_no, content in search_results:
        parts = content.split("|")
        chapter_number = int(parts[0]) - 1
        chapter_names.append(list(quran_chapters.values())[chapter_number])
    chapter_counts = Counter(chapter_names)
    chapter_counts_df = pd.DataFrame(chapter_counts.items(), columns=["Chapter", "Count"]).sort_values(by="Count", ascending=False)
    return chapter_names, chapter_counts_df

def return_chapter_names_within_search_results(search_results_list):
    chapter_names = []
    for content in search_results_list:
        parts = content.split("|")
        chapter_number = int(parts[0]) - 1
        chapter_names.append(list(quran_chapters.values())[chapter_number])
    chapter_counts = Counter(chapter_names)
    chapter_counts_df = pd.DataFrame(chapter_counts.items(), columns=["Chapter", "Count"]).sort_values(by="Count", ascending=False)
    return chapter_names, chapter_counts_df

with open(quran, 'r', encoding='utf-8') as file:
    text = file.read()

english_dict = load_english_translations(quran_english)
english_dict2 = load_english_translations(quran_english2)
english_dict3 = load_english_translations(quran_english3)

# Toggle for English translations (default: hide)
if 'show_english' not in st.session_state:
    st.session_state.show_english = False

st.subheader(ui["search_here"])

col_input, col_check = st.columns([9, 1])
with col_input:
    keyword = st.text_input(ui["keyword_input"], key="main_search", label_visibility="visible")
with col_check:
    st.write("")
    show_english = st.checkbox(ui["show_english"], value=st.session_state.show_english, key="show_eng")
st.session_state.show_english = show_english

if keyword:
    search_results = search_in_text(text, keyword)

    if search_results:
        no_of_occurrences = len(search_results)
        chapter_names, chapter_counts_df = return_chapter_names_normal(search_results)
        st.success(ui["found_occurrences"].format(no_of_occurrences, keyword))
        st.bar_chart(chapter_counts_df.set_index("Chapter"), color=(5,5,5))

        keyword_within = st.text_input(ui["keyword_within"], key="within_search")
        search_results_within = search_in_search_results(search_results, keyword_within)
        no_of_occurrences2 = len(search_results_within)

        if len(keyword_within) > 0:
            chapter_names, chapter_counts_df = return_chapter_names_within_search_results(search_results_within)
            st.success(ui["found_within"].format(no_of_occurrences2, keyword_within, no_of_occurrences))

            if no_of_occurrences2 >= 20:
                num_tabs = no_of_occurrences2 // 10 + (1 if no_of_occurrences2 % 10 else 0)
                tabs = st.tabs([f"{i+1}" for i in range(num_tabs)])
                for idx, content in enumerate(search_results_within):
                    tab_index = idx // 10
                    with tabs[tab_index]:
                        display_results_page(idx+1, content)
            else:
                for idx, content in enumerate(search_results_within):
                    parts = content.split("|")
                    chapter_number = int(parts[0]) - 1
                    chapter_name = list(quran_chapters.values())[chapter_number]
                    verse_number_arabic = parts[1]
                    verse_number = convert_numbers.arabic_to_hindi(verse_number_arabic)

                    trans_pickthall = get_english_translation(parts[0], parts[1], english_dict) if english_dict else ""
                    trans_yusufali = get_english_translation(parts[0], parts[1], english_dict2) if english_dict2 else ""
                    trans_sahih = get_english_translation(parts[0], parts[1], english_dict3) if english_dict3 else ""

                    c1, c2 = st.columns(2)
                    with c1:
                        if lang == "English":
                            st.write(f"**{ui['chapter_prefix'].format(idx+1, chapter_number, list(quran_chapters_en.values())[chapter_number], chapter_name)}:**")
                        else:
                            st.write(f"**{ui['chapter_prefix'].format(idx+1, chapter_name)}:**")
                    with c2:
                        st.write(f"**:green[{parts[2]} (۞{verse_number}۞)]**")
                        if st.session_state.show_english:
                            if trans_pickthall:
                                st.write(f"{ui['pickthall']}: :green[{trans_pickthall} (۞{verse_number_arabic}۞)]")
                            if trans_yusufali:
                                st.write(f"{ui['yusufali']}: :green[{trans_yusufali} (۞{verse_number_arabic}۞)]")
                            if trans_sahih:
                                st.write(f"{ui['sahih']}: :green[{trans_sahih} (۞{verse_number_arabic}۞)]")
                    st.write("----------------------")
        else:
            if no_of_occurrences >= 20:
                num_tabs = no_of_occurrences // 10 + (1 if no_of_occurrences % 10 else 0)
                tabs = st.tabs([f"{i+1}" for i in range(num_tabs)])
                for idx, (line_no, content) in enumerate(search_results):
                    tab_index = idx // 10
                    with tabs[tab_index]:
                        display_results_page(idx+1, content)
            else:
                for idx, (line_no, content) in enumerate(search_results):
                    parts = content.split("|")
                    chapter_number = int(parts[0]) - 1
                    chapter_name = list(quran_chapters.values())[chapter_number]
                    verse_number_arabic = parts[1]
                    verse_number = convert_numbers.arabic_to_hindi(verse_number_arabic)

                    trans_pickthall = get_english_translation(parts[0], parts[1], english_dict) if english_dict else ""
                    trans_yusufali = get_english_translation(parts[0], parts[1], english_dict2) if english_dict2 else ""
                    trans_sahih = get_english_translation(parts[0], parts[1], english_dict3) if english_dict3 else ""

                    c1, c2 = st.columns(2)
                    with c1:
                        if lang == "English":
                            st.write(f"**{ui['chapter_prefix'].format(idx+1, chapter_number, list(quran_chapters_en.values())[chapter_number], chapter_name)}:**")
                        else:
                            st.write(f"**{ui['chapter_prefix'].format(idx+1, chapter_name)}:**")
                    with c2:
                        st.write(f"**:green[{parts[2]} (۞{verse_number}۞)]**")
                        if st.session_state.show_english:
                            if trans_pickthall:
                                st.write(f"{ui['pickthall']}: :green[{trans_pickthall} (۞{verse_number_arabic}۞)]")
                            if trans_yusufali:
                                st.write(f"{ui['yusufali']}: :green[{trans_yusufali} (۞{verse_number_arabic}۞)]")
                            if trans_sahih:
                                st.write(f"{ui['sahih']}: :green[{trans_sahih} (۞{verse_number_arabic}۞)]")
                    st.write("----------------------")
    else:
        st.warning(ui["not_found"].format(keyword))