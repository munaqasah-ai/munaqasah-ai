import streamlit as st
import requests
import io
from pypdf import PdfReader
from docx import Document

st.set_page_config(
    page_title="Munaqasah AI - محلل المناقصات",
    page_icon="📋",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1a237e 0%, #0d47a1 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 { color: white; margin: 0; }
    .main-header p { color: #e3f2fd; margin: 0.5rem 0 0 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>📋 Munaqasah AI</h1>
    <p>محلل المناقصات الذكي — ارفع PDF أو Word واحصل على تقرير كامل</p>
</div>
""", unsafe_allow_html=True)

try:
    OPENROUTER_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    st.error("مفتاح OpenRouter غير معد. أضف OPENROUTER_API_KEY في الإعدادات.")
    st.stop()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openrouter/free"

MASTER_PROMPT = """
أنت محلّل مناقصات خبير في قطاع الإنشاءات والمقاولات العربية، بخبرة 20 سنة. تعمل كمستشار للمقاول، لا كطرف محايد. هدفك: حماية المقاول من الخسارة وتمكينه من قرار ربح.

قواعد صارمة:
1. لا تخمّن. إن غابت معلومة، اكتب: "غير مذكور — التقدير السوقي المعتاد: ___".
2. اذكر رقم الصفحة + اقتباس حرفي قصير (عربي أو إنجليزي كما ورد).
3. لا تكرر النصوص الطويلة. لخّص ثم استشهد.
4. رتّب المخاطر تنازليًا: قاتلة / عالية / متوسطة / منخفضة.
5. كل توصية قابلة للتنفيذ فورًا (Actionable).
6. إن وجدت تعارضًا بين وثيقتين، صنّفه "قاتل" وأبرزه في مكانه.

## قواعد الكشف التلقائي:
A. امسح بحثًا عن: عدد الوحدات، المراحل، المكونات.
B. امسح بحثًا عن: آلية التقييم (نسبة فني/مالي).
C. امسح بحثًا عن: تضاربات في المدة، الميزانية، المواعيد.
D. امسح بحثًا عن: قيود مصرفية، بنوك مستبعدة.
E. امسح بحثًا عن: شروط دفع غير متكافئة.
F. امسح بحثًا عن: مواعيد حرجة (زيارة موقع، آخر موعد).

الهيكل الإلزامي:

## 1. الملخص التنفيذي (صفحة واحدة)
- الجهة، المشروع، الموقع
- عدد الوحدات / المراحل / المكونات
- المواعيد الحرجة (زيارة إلزامية، آخر موعد) — في أول سطر
- الميزانية، المدة، الضمان
- آلية التقييم (نسبة فني/مالي إن وجدت)
- القرار: [تقدّم / لا تتقدم / تحتاج مراجعة]
- السبب في سطر واحد

## 2. الشروط المالية + التقدير السوقي
لكل بند: النص الأصلي + التقدير المعتاد + مستوى الخطورة

## 3. تحليل التدفق النقدي (Cash Flow Analysis)
- الدفعة المقدمة، المستخلصات، فترة الانتظار
- رأس المال العامل المطلوب
- تصنيف: [مريح / ضاغط / قاتل]

## 4. المخاطر التعاقدية (جدول)
| المخاطرة | الشدة | الاقتباس الحرفي | الصفحة | التوصية الفورية |

## 5. كاشف التضاربات
| التضارب | الوثيقة 1 + الصفحة | الوثيقة 2 + الصفحة | الأثر | التوصية |

## 6. المتطلبات الفنية (Checklist)

## 7. تحليل الفجوات (Gap Analysis)
كل فجوة: الحل + التكلفة + الوقت

## 8. التحليل التجاري
- النطاق السعري، هامش الربح، التكاليف الخفية
- رقم التسعير الموصى به

## 9. تحليل المنافسة

## 10. البنود التي ترفع التكلفة (Cost Killers)

## 11. استفسارات RFI جاهزة للإرسال
عربي + إنجليزي

## 12. القرار النهائي
- القرار + 3 أسباب
- خطة 7 أيام
- الخطوة التالية
"""

def extract_text_from_file(uploaded_file):
    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()

    if filename.endswith(".pdf"):
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            parts = []
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    parts.append(t)
            return "\n".join(parts)
        except Exception as e:
            st.error(f"خطأ في قراءة PDF: {e}")
            return None

    elif filename.endswith(".docx"):
        try:
            doc = Document(io.BytesIO(file_bytes))
            parts = []
            for para in doc.paragraphs:
                if para.text.strip():
                    parts.append(para.text)
            for table in doc.tables:
                for row in table.rows:
                    cells = [cell.text.strip() for cell in row.cells]
                    parts.append(" | ".join(cells))
            return "\n".join(parts)
        except Exception as e:
            st.error(f"خطأ في قراءة Word: {e}")
            return None

    elif filename.endswith(".txt") or filename.endswith(".md"):
        return file_bytes.decode("utf-8", errors="ignore")

    else:
        st.error("صيغة غير مدعومة. ارفع PDF, DOCX, TXT, MD.")
        return None


def analyze_with_openrouter(text):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://munaqasah-ai.streamlit.app",
        "X-Title": "Munaqasah AI"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": MASTER_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3,
        "max_tokens": 8000
    }
    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=180)
    if response.status_code != 200:
        raise Exception(f"خطأ {response.status_code}: {response.text[:300]}")
    data = response.json()
    return data["choices"][0]["message"]["content"]


uploaded = st.file_uploader("ارفع ملف المناقصة", type=["pdf", "docx", "txt", "md"])

if uploaded:
    with st.spinner("جاري قراءة الملف..."):
        text = extract_text_from_file(uploaded)

    if text is None:
        st.stop()

    if len(text.strip()) < 100:
        st.warning("الملف يبدو فارغًا أو ممسوحًا ضوئيًا. النسخة الحالية تدعم PDF النصي فقط.")
    else:
        st.success(f"تم استخراج {len(text):,} حرف")
        st.caption(f"حجم النص: ~{len(text)//4:,} رمز (Token)")

        if st.button("تحليل المناقصة", type="primary", use_container_width=True):
            with st.spinner("يحلل بواسطة Gemini عبر OpenRouter... قد يستغرق 60-120 ثانية"):
                try:
                    report = analyze_with_openrouter(text)
                    st.markdown("---")
                    st.markdown(report)
                    st.download_button(
                        "تحميل التقرير (Markdown)",
                        report,
                        file_name="تقرير_المناقصة.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"خطأ في التحليل: {e}")

st.markdown("---")
