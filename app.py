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
MODEL_NAME = "google/gemini-2.0-flash-exp:free"

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
st.caption("Munaqasah AI v2.2 — محلل مناقصات ذكي للقطاع الإنشائي العربي")  return;
      }

      analyzeBtn.disabled = true;
      showStatus("جارٍ تحليل الملف، يرجى الانتظار...");

      try {
        let report;

        if (demoMode.checked) {
          await wait(900);
          report = createDemoReport(selectedFile.name);
          currentReport = report;
          displayReport(report, true);
        } else {
          report = await analyzeWithSecureBackend(selectedFile);
          currentReport = report;
          displayReport(report, false);
        }

        showStatus("اكتمل إنشاء التقرير.");
      } catch (error) {
        showError(error.message || "تعذر إكمال التحليل.");
        showStatus("فشل التحليل.");
      } finally {
        analyzeBtn.disabled = false;
      }
    });

    async function analyzeWithSecureBackend(file) {
      /*
        يجب أن يكون هذا المسار خلفيًا وآمنًا.
        لا تضع GEMINI_API_KEY في هذا الملف أو في المتصفح.

        مثال متوقع لنقطة الاتصال:
        POST /api/analyze
        Content-Type: multipart/form-data
      */

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error(
          "التحليل الحقيقي يحتاج إلى نقطة اتصال خلفية آمنة ومهيأة."
        );
      }

      const data = await response.json();

      if (!data.report) {
        throw new Error("لم تصل نتيجة تقرير صالحة من الخدمة الخلفية.");
      }

      return data.report;
    }

    function createDemoReport(filename) {
      return `
<span class="badge demo-badge">وضع العرض التجريبي — ليست نتيجة تحليل حقيقية</span>

<h2>1. الملخص التنفيذي</h2>
<p><strong>الملف:</strong> ${escapeHtml(filename)}</p>
<p><strong>الجهة:</strong> غير مذكور — التقدير السوقي المعتاد: يلزم مراجعة وثائق المناقصة.</p>
<p><strong>المشروع:</strong> غير مذكور.</p>
<p><strong>الموقع:</strong> غير مذكور.</p>
<p><strong>عدد الوحدات أو المراحل:</strong> غير مذكور.</p>
<p><strong>المواعيد الحرجة:</strong> غير مذكور.</p>
<p><strong>الميزانية والمدة والضمان:</strong> غير مذكور.</p>
<p><strong>القرار:</strong> تحتاج مراجعة.</p>
<p><strong>السبب:</strong> التقرير الحالي تجريبي ولا يعتمد على تحليل فعلي للوثيقة.</p>

<h2>2. الشروط المالية والتقدير السوقي</h2>
<table>
  <tr>
    <th>البند</th>
    <th>النص الأصلي</th>
    <th>الخطورة</th>
    <th>التوصية</th>
  </tr>
  <tr>
    <td>شروط الدفع</td>
    <td>غير مذكور</td>
    <td><span class="badge danger-badge">عالية</span></td>
    <td>طلب جدول الدفعات وفترة اعتماد المستخلصات.</td>
  </tr>
</table>

<h2>3. تحليل التدفق النقدي</h2>
<p>لا توجد بيانات كافية لتحديد الدفعة المقدمة أو فترة الانتظار.</p>
<p><strong>التصنيف:</strong> ضاغط حتى يتم التحقق من شروط الدفع.</p>

<h2>4. المخاطر التعاقدية</h2>
<table>
  <tr>
    <th>المخاطرة</th>
    <th>الشدة</th>
    <th>الاقتباس</th>
    <th>الصفحة</th>
    <th>التوصية</th>
  </tr>
  <tr>
    <td>غياب شروط واضحة</td>
    <td>عالية</td>
    <td>غير مذكور</td>
    <td>غير مذكور</td>
    <td>إرسال طلب توضيح رسمي.</td>
  </tr>
</table>

<h2>5. كاشف التضاربات</h2>
<p>لم يتم اكتشاف تضاربات في وضع العرض التجريبي.</p>

<h2>6. المتطلبات الفنية</h2>
<ul>
  <li>مراجعة نطاق الأعمال.</li>
  <li>التحقق من المواصفات والمخططات.</li>
  <li>تأكيد متطلبات الخبرة والكوادر.</li>
</ul>

<h2>7. تحليل الفجوات</h2>
<p>يلزم توفير الوثيقة وتحليل محتواها لتحديد الفجوات والتكلفة والوقت.</p>

<h2>8. التحليل التجاري</h2>
<p>لا يمكن تحديد النطاق السعري أو رقم التسعير الموصى به دون بيانات الكميات والتكاليف.</p>

<h2>9. تحليل المنافسة</h2>
<p>غير مذكور — التقدير السوقي المعتاد: يلزم تحليل السوق والمنافسين.</p>

<h2>10. البنود التي ترفع التكلفة</h2>
<ul>
  <li>تأخر الدفعات.</li>
  <li>تغير نطاق الأعمال.</li>
  <li>غموض المواصفات.</li>
</ul>

<h2>11. استفسارات RFI جاهزة للإرسال</h2>
<p><strong>العربية:</strong> يرجى تزويدنا بجدول الدفعات، مدة اعتماد المستخلصات، وآلية معالجة أوامر التغيير.</p>
<p><strong>English:</strong> Please provide the payment schedule, certification period, and change-order procedure.</p>

<h2>12. القرار النهائي</h2>
<ol>
  <li>لا يمكن اتخاذ قرار نهائي دون تحليل الملف الفعلي.</li>
  <li>يجب التحقق من الشروط المالية والمواعيد الحرجة.</li>
  <li>يجب طلب التوضيحات قبل التسعير.</li>
</ol>

<p><strong>خطة 7 أيام:</strong></p>
<ul>
  <li>اليوم 1: مراجعة الوثائق.</li>
  <li>اليومان 2 و3: استخراج الكميات والمتطلبات.</li>
  <li>اليومان 4 و5: مراجعة المخاطر والتسعير.</li>
  <li>اليومان 6 و7: تجهيز الاستفسارات والقرار النهائي.</li>
</ul>
      `;
    }

    function displayReport(report, isDemo) {
      reportSection.style.display = "block";

      reportContent.innerHTML = `
        ${isDemo ? "" : '<span class="badge safe-badge">تحليل حقيقي</span>'}
        ${report}
      `;

      reportSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    }

    document.getElementById("copyBtn").addEventListener("click", async () => {
      const text = reportContent.innerText;

      await navigator.clipboard.writeText(text);
      showStatus("تم نسخ التقرير.");
    });

    document.getElementById("downloadBtn").addEventListener("click", () => {
      const text = reportContent.innerText;
      const blob = new Blob([text], {
        type: "text/markdown;charset=utf-8"
      });

      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = "تقرير_المناقصة.md";
      link.click();

      URL.revokeObjectURL(url);
    });

    resetBtn.addEventListener("click", () => {
      if (!confirm("هل تريد حذف الملف والتقرير الحالي؟")) {
        return;
      }

      selectedFile = null;
      extractedText = "";
      currentReport = "";

      fileInput.value = "";
      fileInfo.style.display = "none";
      summary.style.display = "none";
      reportSection.style.display = "none";
      statusBox.style.display = "none";
      errorBox.style.display = "none";
      analyzeBtn.disabled = true;
    });

    function wait(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }

    function escapeHtml(value) {
      return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }
  </script>
</body>
</html>
