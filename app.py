import streamlit as st
import google.generativeai as genai
import pdfplumber
import io

# ============ إعدادات الصفحة ============
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
    <p>محلل المناقصات الذكي — ارفع PDF واحصل على تقرير كامل في 90 ثانية</p>
</div>
""", unsafe_allow_html=True)

# ============ إعداد Gemini ============
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("⚠️ مفتاح API غير معد. أضف GEMINI_API_KEY في الإعدادات.")
    st.stop()

MODEL_NAME = "gemini-2.5-pro"

# ============ الـ Prompt الرئيسي v3.0 ============
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
- 🔢 عدد الوحدات / المراحل / المكونات
- 📅 المواعيد الحرجة (زيارة إلزامية، آخر موعد) — في أول سطر
- 💰 الميزانية، المدة، الضمان
- ⚖️ آلية التقييم (نسبة فني/مالي إن وجدت)
- 🎯 القرار: [تقدّم / لا تتقدم / تحتاج مراجعة]
- 💡 السبب في سطر واحد

## 2. الشروط المالية + التقدير السوقي
لكل بند: النص الأصلي + التقدير المعتاد + مستوى الخطورة

## 3. تحليل التدفق النقدي (Cash Flow Analysis)
- الدفعة المقدمة، المستخلصات، فترة الانتظار
- رأس المال العامل المطلوب
- 🚨 تصنيف: [مريح / ضاغط / قاتل]

## 4. المخاطر التعاقدية (جدول)
| المخاطرة | الشدة | الاقتباس الحرفي | الصفحة | التوصية الفورية |

## 5. كاشف التضاربات
| التضارب | الوثيقة 1 + الصفحة | الوثيقة 2 + الصفحة | الأثر | التوصية |

## 6. المتطلبات الفنية (Checklist)

## 7. تحليل الفجوات (Gap Analysis)
كل فجوة → الحل + التكلفة + الوقت

## 8. التحليل التجاري
- النطاق السعري، هامش الربح، التكاليف الخفية
- 🔢 رقم التسعير الموصى به

## 9. تحليل المنافسة

## 10. البنود التي ترفع التكلفة (Cost Killers)

## 11. استفسارات RFI جاهزة للإرسال
عربي + إنجليزي

## 12. القرار النهائي
- القرار + 3 أسباب
- خطة 7 أيام
- الخطوة التالية
"""

# ============ رفع الملف ============
uploaded = st.file_uploader("📎 ارفع ملف المناقصة (PDF)", type=["pdf"])

if uploaded:
    with st.spinner("جاري قراءة الملف..."):
        try:
            with pdfplumber.open(io.BytesIO(uploaded.read())) as pdf:
                pages = len(pdf.pages)
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        except Exception as e:
            st.error(f"خطأ في قراءة الملف: {e}")
            st.stop()

    if len(text.strip()) < 100:
        st.warning("⚠️ الملف يبدو صورة ممسوحة (Scanned). هذه النسخة تدعم PDF نصي فقط.")
    else:
        st.success(f"✅ تم استخراج {len(text):,} حرف من {pages} صفحة")
        st.caption(f"حجم النص: ~{len(text)//4:,} رمز (Token)")

        if st.button("🚀 تحليل المناقصة", type="primary", use_container_width=True):
            with st.spinner("يحلل بواسطة Gemini... قد يستغرق 60-90 ثانية"):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    response = model.generate_content([MASTER_PROMPT, text])
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button(
                        "📥 تحميل التقرير (Markdown)",
                        response.text,
                        file_name="تقرير_المناقصة.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"خطأ في التحليل: {e}")

# ============ تذييل ============
st.markdown("---")
st.caption("Munaqasah AI v1.0 — محلل مناقصات ذكي للقطاع الإنشائي العربي")
