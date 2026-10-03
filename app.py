<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Munaqasah AI</title>

  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: #f4f7fb;
      color: #172033;
      font-family: Tahoma, Arial, sans-serif;
    }

    .app {
      max-width: 1100px;
      margin: auto;
      padding: 24px;
    }

    .hero {
      padding: 34px 24px;
      color: white;
      text-align: center;
      border-radius: 18px;
      background: linear-gradient(135deg, #17237e, #0d61ad);
      box-shadow: 0 12px 30px #17237e35;
    }

    .hero h1 {
      margin: 0 0 10px;
      font-size: 34px;
    }

    .hero p {
      margin: 0;
      color: #e4f2ff;
      font-size: 17px;
    }

    .card {
      margin-top: 20px;
      padding: 22px;
      border: 1px solid #dce4ef;
      border-radius: 16px;
      background: white;
      box-shadow: 0 5px 18px #26364d12;
    }

    .card h2 {
      margin-top: 0;
      color: #17237e;
    }

    .upload-area {
      display: block;
      padding: 35px 20px;
      border: 2px dashed #4387c6;
      border-radius: 14px;
      background: #f5faff;
      text-align: center;
      cursor: pointer;
    }

    .upload-area:hover,
    .upload-area:focus-within {
      background: #eaf4ff;
      border-color: #17237e;
    }

    .upload-area input {
      display: none;
    }

    .upload-icon {
      font-size: 42px;
      display: block;
      margin-bottom: 12px;
    }

    .hint {
      color: #617087;
      font-size: 14px;
      margin-top: 8px;
    }

    .file-info,
    .summary {
      display: none;
      margin-top: 18px;
      padding: 16px;
      border-radius: 12px;
      background: #f7f9fc;
    }

    .summary-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
    }

    .summary-item {
      padding: 14px;
      border: 1px solid #dce4ef;
      border-radius: 10px;
      background: white;
    }

    .summary-item strong {
      display: block;
      margin-top: 5px;
      color: #17237e;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }

    button {
      border: 0;
      border-radius: 9px;
      padding: 12px 18px;
      color: white;
      background: #17237e;
      cursor: pointer;
      font-weight: bold;
      font-size: 14px;
    }

    button:hover {
      filter: brightness(1.12);
    }

    button.secondary {
      color: #17237e;
      background: #e8eef8;
    }

    button.danger {
      background: #b42318;
    }

    button:disabled {
      opacity: .55;
      cursor: not-allowed;
    }

    .status {
      display: none;
      margin-top: 18px;
      padding: 14px;
      border-radius: 10px;
      color: #17416e;
      background: #e6f3ff;
    }

    .error {
      display: none;
      margin-top: 14px;
      padding: 13px;
      border-radius: 10px;
      color: #8b1e1e;
      background: #fff0f0;
    }

    .mode {
      display: flex;
      align-items: center;
      gap: 10px;
      margin: 15px 0;
      color: #344054;
    }

    .report {
      display: none;
      margin-top: 20px;
      padding: 24px;
      border-radius: 14px;
      background: white;
      line-height: 1.9;
    }

    .report h2 {
      padding-bottom: 8px;
      border-bottom: 2px solid #dce8f5;
      color: #17237e;
    }

    .report h3 {
      color: #0d61ad;
    }

    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: bold;
    }

    .demo-badge {
      color: #7a4d00;
      background: #fff1bf;
    }

    .danger-badge {
      color: #8b1e1e;
      background: #ffd9d9;
    }

    .safe-badge {
      color: #126b3a;
      background: #d9f8e5;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0 24px;
    }

    th,
    td {
      padding: 10px;
      border: 1px solid #dce4ef;
      text-align: right;
      vertical-align: top;
    }

    th {
      color: white;
      background: #17237e;
    }

    footer {
      padding: 25px 0 10px;
      color: #718096;
      text-align: center;
      font-size: 13px;
    }

    @media (max-width: 700px) {
      .app {
        padding: 12px;
      }

      .hero h1 {
        font-size: 26px;
      }

      .summary-grid {
        grid-template-columns: repeat(2, 1fr);
      }

      .actions button {
        width: 100%;
      }
    }
  </style>
</head>

<body>
  <main class="app">
    <section class="hero">
      <h1>📋 Munaqasah AI</h1>
      <p>محلل المناقصات الذكي — ارفع PDF أو Word واحصل على تقرير كامل</p>
    </section>

    <section class="card">
      <h2>رفع ملف المناقصة</h2>

      <label class="upload-area" for="fileInput">
        <span class="upload-icon">📎</span>
        <strong>اضغط لاختيار ملف المناقصة</strong>
        <div class="hint">الصيغ المدعومة: PDF، DOCX، TXT، MD</div>
        <input
          id="fileInput"
          type="file"
          accept=".pdf,.docx,.txt,.md"
        />
      </label>

      <div id="errorBox" class="error"></div>

      <div id="fileInfo" class="file-info">
        <strong id="fileName"></strong>
        <div id="fileDetails" class="hint"></div>
      </div>

      <div class="mode">
        <input id="demoMode" type="checkbox" checked />
        <label for="demoMode">
          استخدام وضع العرض التجريبي عند عدم توفر اتصال خلفي آمن
        </label>
      </div>

      <div class="actions">
        <button id="analyzeBtn" disabled>
          🚀 تحليل المناقصة
        </button>

        <button id="resetBtn" class="danger">
          إعادة ضبط
        </button>
      </div>

      <div id="statusBox" class="status"></div>
    </section>

    <section id="summary" class="card summary">
      <h2>ملخص الملف</h2>

      <div class="summary-grid">
        <div class="summary-item">
          اسم الملف
          <strong id="summaryName">-</strong>
        </div>

        <div class="summary-item">
          النوع
          <strong id="summaryType">-</strong>
        </div>

        <div class="summary-item">
          حالة الاستخراج
          <strong id="summaryStatus">-</strong>
        </div>

        <div class="summary-item">
          عدد الأحرف
          <strong id="summaryLength">-</strong>
        </div>
      </div>
    </section>

    <section id="reportSection" class="card report">
      <div class="actions">
        <button id="copyBtn" class="secondary">
          نسخ التقرير
        </button>

        <button id="downloadBtn" class="secondary">
          تنزيل Markdown
        </button>
      </div>

      <article id="reportContent"></article>
    </section>

    <footer>
      Munaqasah AI — محلل مناقصات للقطاع الإنشائي العربي
    </footer>
  </main>

  <script>
    const fileInput = document.getElementById("fileInput");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const resetBtn = document.getElementById("resetBtn");
    const demoMode = document.getElementById("demoMode");

    const errorBox = document.getElementById("errorBox");
    const statusBox = document.getElementById("statusBox");
    const fileInfo = document.getElementById("fileInfo");
    const summary = document.getElementById("summary");
    const reportSection = document.getElementById("reportSection");
    const reportContent = document.getElementById("reportContent");

    let selectedFile = null;
    let extractedText = "";
    let currentReport = "";

    const allowedExtensions = ["pdf", "docx", "txt", "md"];

    function showError(message) {
      errorBox.textContent = message;
      errorBox.style.display = "block";
    }

    function clearError() {
      errorBox.textContent = "";
      errorBox.style.display = "none";
    }

    function showStatus(message) {
      statusBox.textContent = message;
      statusBox.style.display = "block";
    }

    function getExtension(filename) {
      return filename.split(".").pop().toLowerCase();
    }

    function formatBytes(bytes) {
      if (bytes < 1024) return `${bytes} بايت`;
      if (bytes < 1024 * 1024) {
        return `${(bytes / 1024).toFixed(1)} كيلوبايت`;
      }
      return `${(bytes / (1024 * 1024)).toFixed(1)} ميجابايت`;
    }

    fileInput.addEventListener("change", async () => {
      clearError();
      selectedFile = fileInput.files[0];

      if (!selectedFile) {
        analyzeBtn.disabled = true;
        return;
      }

      const extension = getExtension(selectedFile.name);

      if (!allowedExtensions.includes(extension)) {
        selectedFile = null;
        fileInput.value = "";
        analyzeBtn.disabled = true;
        showError("صيغة الملف غير مدعومة. ارفع PDF أو DOCX أو TXT أو MD.");
        return;
      }

      fileInfo.style.display = "block";
      analyzeBtn.disabled = false;

      document.getElementById("fileName").textContent =
        selectedFile.name;

      document.getElementById("fileDetails").textContent =
        `${formatBytes(selectedFile.size)} — ${extension.toUpperCase()}`;

      document.getElementById("summaryName").textContent =
        selectedFile.name;

      document.getElementById("summaryType").textContent =
        extension.toUpperCase();

      if (extension === "txt" || extension === "md") {
        extractedText = await selectedFile.text();
        updateSummary("تم استخراج النص");
      } else if (extension === "pdf") {
        updateSummary("يحتاج إلى استخراج أو OCR");
      } else {
        updateSummary("جاهز للمعالجة الخلفية");
      }

      summary.style.display = "block";
    });

    function updateSummary(status) {
      document.getElementById("summaryStatus").textContent = status;
      document.getElementById("summaryLength").textContent =
        extractedText ? extractedText.length.toLocaleString("ar") : "-";
    }

    analyzeBtn.addEventListener("click", async () => {
      clearError();

      if (!selectedFile) {
        showError("اختر ملفًا أولًا قبل بدء التحليل.");
        return;
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
