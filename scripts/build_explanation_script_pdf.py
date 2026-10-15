"""
Generate FLORAai Project Explanation Script PDF for Faculty & Teacher Defense.
Generates a comprehensive, professional, beautifully styled multi-page PDF document.
"""
import sys
from pathlib import Path
from fpdf import FPDF

# Define Project Palette
COLOR_FOREST = (19, 58, 34)       # #133a22 - Deep Botanical Green
COLOR_EMERALD = (22, 101, 52)     # #166534 - Vibrant Green
COLOR_MINT_BG = (240, 253, 244)   # #f0fdf4 - Soft Mint Background
COLOR_MINT_BORDER = (187, 247, 208)# #bbf7d0 - Mint Border
COLOR_DARK_TEXT = (30, 41, 59)    # #1e293b - Slate Dark
COLOR_BODY_TEXT = (51, 65, 85)    # #334155 - Slate Body
COLOR_MUTED = (100, 116, 139)     # #64748b - Slate Muted
COLOR_CARD_BG = (248, 250, 252)   # #f8fafc - Card Background
COLOR_CARD_BORDER = (226, 232, 240)# #e2e8f0 - Card Border
COLOR_GOLD = (180, 83, 9)         # #b45309 - Warm Gold / Amber Accent

FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_ITALIC = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
LOGO_PATH = "/Users/amrutachari/Desktop/floraAI/frontend/public/logo.png"
OUTPUT_PDF = "/Users/amrutachari/Desktop/floraAI/script_for_explanation/FLORAai_Project_Explanation_Script.pdf"


class ExplanationPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(18, 18, 18)
        self.set_auto_page_break(auto=True, margin=18)
        self.add_font("ArialCustom", "", FONT_REG)
        self.add_font("ArialCustom", "B", FONT_BOLD)
        self.add_font("ArialCustom", "I", FONT_ITALIC)
        self.current_chapter = ""

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("ArialCustom", "B", 8)
        self.set_text_color(*COLOR_FOREST)
        self.cell(100, 6, "FLORAai  Project Explanation Script & Viva Defense Guide", align="L")
        self.set_font("ArialCustom", "I", 8)
        self.set_text_color(*COLOR_MUTED)
        self.cell(0, 6, self.current_chapter, align="R")
        self.ln(7)
        self.set_draw_color(*COLOR_CARD_BORDER)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(*COLOR_CARD_BORDER)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)
        self.set_font("ArialCustom", "", 8)
        self.set_text_color(*COLOR_MUTED)
        self.cell(90, 6, "Author: Amrut Achari  |  FLORAai Project Presentation Package", align="L")
        self.cell(0, 6, f"Page {self.page_no()} of {{nb}}", align="R")

    def chapter_title(self, number, title):
        self.current_chapter = f"Section {number}: {title}"
        self.ln(3)
        self.set_font("ArialCustom", "B", 15)
        self.set_text_color(*COLOR_FOREST)
        self.cell(0, 8, f"{number}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*COLOR_EMERALD)
        self.set_line_width(0.8)
        y = self.get_y() + 1
        self.line(self.l_margin, y, self.l_margin + 45, y)
        self.set_draw_color(*COLOR_MINT_BORDER)
        self.set_line_width(0.4)
        self.line(self.l_margin + 45, y, self.w - self.r_margin, y)
        self.ln(5)

    def section_subtitle(self, title):
        self.ln(2)
        self.set_font("ArialCustom", "B", 11.5)
        self.set_text_color(*COLOR_EMERALD)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def paragraph(self, text, style="", size=9.8, text_color=COLOR_BODY_TEXT):
        self.set_font("ArialCustom", style, size)
        self.set_text_color(*text_color)
        self.multi_cell(0, 5.2, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bullet_point(self, title, desc):
        self.set_font("ArialCustom", "B", 9.5)
        self.set_text_color(*COLOR_DARK_TEXT)
        prefix = "   "
        self.cell(6, 5, prefix)
        title_width = self.get_string_width(f"{title}: ")
        self.cell(title_width, 5, f"{title}: ")
        self.set_font("ArialCustom", "", 9.5)
        self.set_text_color(*COLOR_BODY_TEXT)
        avail_width = self.w - self.r_margin - self.get_x()
        self.multi_cell(avail_width, 5, desc, new_x="LMARGIN", new_y="NEXT")
        self.ln(1.5)

    def callout_box(self, title, body_lines, accent_color=COLOR_EMERALD, bg_color=COLOR_MINT_BG):
        self.ln(2)
        w = self.w - self.l_margin - self.r_margin
        content_w = w - 12

        # Measure title and body lines accurately
        self.set_font("ArialCustom", "B", 10)
        title_lines = self.multi_cell(content_w, 5, title, dry_run=True, output="LINES")
        title_h = len(title_lines) * 5.2

        self.set_font("ArialCustom", "", 9)
        total_text_h = 0
        for line in body_lines:
            lines = self.multi_cell(content_w, 4.5, line, dry_run=True, output="LINES")
            total_text_h += len(lines) * 4.6 + 1.5

        box_h = 7 + title_h + total_text_h

        start_y = self.get_y()
        # Ensure no page split inside small box
        if start_y + box_h > self.h - self.b_margin:
            self.add_page()
            start_y = self.get_y()

        self.set_fill_color(*bg_color)
        self.set_draw_color(*COLOR_MINT_BORDER)
        self.rect(self.l_margin, start_y, w, box_h, style="FD")

        # Left thick border
        self.set_fill_color(*accent_color)
        self.rect(self.l_margin, start_y, 2.5, box_h, style="F")

        # Title
        self.set_xy(self.l_margin + 6, start_y + 3)
        self.set_font("ArialCustom", "B", 10)
        self.set_text_color(*accent_color)
        self.multi_cell(content_w, 5, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

        # Body
        self.set_font("ArialCustom", "", 9)
        self.set_text_color(*COLOR_DARK_TEXT)
        for line in body_lines:
            self.set_x(self.l_margin + 6)
            self.multi_cell(content_w, 4.5, line, new_x="LMARGIN", new_y="NEXT")
            self.ln(1)
        self.set_y(start_y + box_h + 3)

    def draw_table(self, headers, rows, col_widths, align_cols=None):
        if align_cols is None:
            align_cols = ["L"] * len(headers)
        self.ln(2)
        # Header Row
        self.set_font("ArialCustom", "B", 9)
        self.set_fill_color(*COLOR_FOREST)
        self.set_text_color(255, 255, 255)
        self.set_draw_color(*COLOR_CARD_BORDER)
        self.set_line_width(0.3)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 7, header, border=1, fill=True, align=align_cols[i])
        self.ln(7)

        # Body Rows
        self.set_font("ArialCustom", "", 8.5)
        self.set_text_color(*COLOR_DARK_TEXT)
        for r_idx, row in enumerate(rows):
            fill = (r_idx % 2 == 1)
            self.set_fill_color(*(248, 250, 252) if fill else (255, 255, 255))
            # Find max height for this row
            max_lines = 1
            for i, cell_val in enumerate(row):
                lines = self.multi_cell(col_widths[i], 4.5, str(cell_val), border=0, dry_run=True, output="LINES")
                if len(lines) > max_lines:
                    max_lines = len(lines)
            row_h = max(6.5, max_lines * 4.6)

            # Page break check
            if self.get_y() + row_h > self.h - self.b_margin:
                self.add_page()
                # Redraw header on new page
                self.set_font("ArialCustom", "B", 9)
                self.set_fill_color(*COLOR_FOREST)
                self.set_text_color(255, 255, 255)
                for i, header in enumerate(headers):
                    self.cell(col_widths[i], 7, header, border=1, fill=True, align=align_cols[i])
                self.ln(7)
                self.set_font("ArialCustom", "", 8.5)
                self.set_text_color(*COLOR_DARK_TEXT)

            start_y = self.get_y()
            start_x = self.get_x()
            for i, cell_val in enumerate(row):
                self.set_xy(start_x, start_y)
                self.rect(start_x, start_y, col_widths[i], row_h, style="FD" if fill else "D")
                self.set_xy(start_x + 1.5, start_y + 1.2)
                self.multi_cell(col_widths[i] - 3, 4.2, str(cell_val), border=0, align=align_cols[i])
                start_x += col_widths[i]
            self.set_y(start_y + row_h)
        self.ln(3)


def build_explanation_pdf():
    pdf = ExplanationPDF()
    pdf.alias_nb_pages()

    # =========================================================================
    # PAGE 1: TITLE & COVER PAGE
    # =========================================================================
    pdf.add_page()
    pdf.ln(10)

    # Top Brand Bar
    w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_fill_color(*COLOR_FOREST)
    pdf.rect(pdf.l_margin, pdf.get_y(), w, 55, style="F")

    # Logo + Title inside Top Bar
    logo_file = Path(LOGO_PATH)
    if logo_file.exists():
        pdf.image(str(logo_file), x=pdf.l_margin + 6, y=pdf.get_y() + 7, w=40)

    pdf.set_xy(pdf.l_margin + 52, pdf.get_y() + 8)
    pdf.set_font("ArialCustom", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 9, "FLORAai", new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(pdf.l_margin + 52)
    pdf.set_font("ArialCustom", "", 12)
    pdf.set_text_color(187, 247, 208)
    pdf.cell(0, 6, "Botanical Herbarium & Plant Health AI System", new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(pdf.l_margin + 52)
    pdf.set_font("ArialCustom", "I", 9.5)
    pdf.set_text_color(226, 232, 240)
    pdf.cell(0, 6, "Specialized for Flora and Agricultural Crops of the Indian Subcontinent", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(pdf.l_margin + 65)
    pdf.ln(4)

    # Document Subtitle / Metadata Card
    pdf.set_font("ArialCustom", "B", 16)
    pdf.set_text_color(*COLOR_FOREST)
    pdf.multi_cell(0, 7.5, "Project Presentation Script & Viva Defense Package", align="L")
    pdf.ln(1)

    pdf.set_font("ArialCustom", "", 10.5)
    pdf.set_text_color(*COLOR_MUTED)
    pdf.multi_cell(0, 5.5, "A complete, step-by-step explanatory guide designed to present the full technical architecture, machine learning model roadmap, and live demonstration workflow to faculty evaluators.")
    pdf.ln(4)

    # Metadata Grid Box
    meta_box_y = pdf.get_y()
    pdf.set_fill_color(*COLOR_CARD_BG)
    pdf.set_draw_color(*COLOR_CARD_BORDER)
    pdf.rect(pdf.l_margin, meta_box_y, w, 34, style="FD")

    col1_x = pdf.l_margin + 5
    col2_x = pdf.l_margin + 93

    # Row 1
    pdf.set_xy(col1_x, meta_box_y + 3.5)
    pdf.set_font("ArialCustom", "B", 9)
    pdf.set_text_color(*COLOR_FOREST)
    pdf.cell(32, 5, "Student / Author:")
    pdf.set_font("ArialCustom", "", 9)
    pdf.set_text_color(*COLOR_DARK_TEXT)
    pdf.cell(52, 5, "Amrut Achari")

    pdf.set_xy(col2_x, meta_box_y + 3.5)
    pdf.set_font("ArialCustom", "B", 9)
    pdf.set_text_color(*COLOR_FOREST)
    pdf.cell(26, 5, "Project Type:")
    pdf.set_font("ArialCustom", "", 9)
    pdf.set_text_color(*COLOR_DARK_TEXT)
    pdf.cell(50, 5, "Full-Stack AI Web Application")

    # Row 2
    pdf.set_xy(col1_x, meta_box_y + 10.5)
    pdf.set_font("ArialCustom", "B", 9)
    pdf.set_text_color(*COLOR_FOREST)
    pdf.cell(32, 5, "Tech Stack:")
    pdf.set_font("ArialCustom", "", 9)
    pdf.set_text_color(*COLOR_DARK_TEXT)
    pdf.cell(52, 5, "FastAPI + React + MongoDB")

    pdf.set_xy(col2_x, meta_box_y + 10.5)
    pdf.set_font("ArialCustom", "B", 9)
    pdf.set_text_color(*COLOR_FOREST)
    pdf.cell(26, 5, "AI Engine:")
    pdf.set_font("ArialCustom", "", 9)
    pdf.set_text_color(*COLOR_DARK_TEXT)
    pdf.cell(50, 5, "Google Gemini Vision Multimodal")

    # Row 3
    pdf.set_xy(col1_x, meta_box_y + 17.5)
    pdf.set_font("ArialCustom", "B", 9)
    pdf.set_text_color(*COLOR_FOREST)
    pdf.cell(32, 5, "Botanical Catalog:")
    pdf.set_font("ArialCustom", "", 9)
    pdf.set_text_color(*COLOR_DARK_TEXT)
    pdf.cell(52, 5, "63 Species (12 Palms Herbarium)")

    pdf.set_xy(col2_x, meta_box_y + 17.5)
    pdf.set_font("ArialCustom", "B", 9)
    pdf.set_text_color(*COLOR_FOREST)
    pdf.cell(26, 5, "Security & Auth:")
    pdf.set_font("ArialCustom", "", 9)
    pdf.set_text_color(*COLOR_DARK_TEXT)
    pdf.cell(50, 5, "JWT HttpOnly Cookies + Bcrypt")

    # Row 4
    pdf.set_xy(col1_x, meta_box_y + 24.5)
    pdf.set_font("ArialCustom", "B", 9)
    pdf.set_text_color(*COLOR_FOREST)
    pdf.cell(32, 5, "Deployment:")
    pdf.set_font("ArialCustom", "", 9)
    pdf.set_text_color(*COLOR_DARK_TEXT)
    pdf.cell(52, 5, "Docker & Compose Ready")

    pdf.set_xy(col2_x, meta_box_y + 24.5)
    pdf.set_font("ArialCustom", "B", 9)
    pdf.set_text_color(*COLOR_FOREST)
    pdf.cell(26, 5, "Repository:")
    pdf.set_font("ArialCustom", "", 9)
    pdf.set_text_color(*COLOR_DARK_TEXT)
    pdf.cell(50, 5, "AMRUTACHARI/Amrutproject")

    pdf.set_y(meta_box_y + 37)

    # 1-Minute Pitch Box
    pdf.callout_box(
        "The 60-Second Elevator Pitch (Memorize this for your opening):",
        [
            "\"Good morning, Sir/Ma'am. My project is FLORAai, an intelligent, full-stack plant health diagnostic system tailored specifically for agricultural crops, spices, medicinal herbs, and palms of the Indian subcontinent.",
            "While existing gardening apps are trained on Western house plants and spit out dense Latin disease jargon that regular farmers cannot decipher, FLORAai accurately diagnoses 63 native species from a single photo, explains the root cause in simple plain English, and provides 100% realistic organic Ayurvedic remedies like neem oil, wood ash, and sour buttermilk spray.\"",
        ],
        accent_color=COLOR_FOREST,
        bg_color=COLOR_MINT_BG,
    )

    pdf.section_subtitle("Table of Contents for Presentation:")
    pdf.bullet_point("Section 1", "Executive Summary, Real-World Problem, and Solution Architecture")
    pdf.bullet_point("Section 2", "End-to-End System Workflow: From Camera Click to Organic Diagnosis")
    pdf.bullet_point("Section 3", "Technology Stack, Programming Languages & Framework Justifications")
    pdf.bullet_point("Section 4", "The AI Vision Model Roadmap, Botanical Knowledge & Plain-English Layer")
    pdf.bullet_point("Section 5", "Word-for-Word Teacher Presentation Script (5 to 10 Minute Guide)")
    pdf.bullet_point("Section 6", "Live Demonstration Walkthrough: What to Click & What to Say")
    pdf.bullet_point("Section 7", "Viva Voce / Examination Q&A Preparation: 10 Tough Questions & Winning Answers")
    pdf.bullet_point("Section 8", "Security, Containerized Deployment (Docker) & Future Enhancements")

    # =========================================================================
    # PAGE 2: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("1", "Executive Summary & Problem Statement")

    pdf.section_subtitle("1.1 The Real-World Agricultural & Botanical Problem")
    pdf.paragraph(
        "In the Indian subcontinent, agriculture and home gardening form the backbone of both rural livelihoods and urban wellbeing. "
        "However, millions of smallholder farmers, terrace gardeners, and plant enthusiasts face three persistent bottlenecks when their plants fall sick:"
    )
    pdf.bullet_point(
        "Geographic & Taxonomy Bias in Existing Tools",
        "Most global computer vision plant diagnosis models are trained on European and North American temperate flora (roses, hydrangeas, oak, apples). They consistently fail or misclassify critical tropical staples and cash crops such as Coconut, Areca Palm, Betel Leaf (Paan), Curry Leaf (Kadi Patta), and Turmeric.",
    )
    pdf.bullet_point(
        "The 'Latin Jargon' Barrier",
        "Standard botanical diagnosis applications output clinical pathology terminology like 'foliar chlorosis', 'interveinal necrosis', 'apical meristem blight', or 'fungal sporulation'. These words confuse farmers, students, and home gardeners rather than helping them take quick corrective action.",
    )
    pdf.bullet_point(
        "Inaccessible Chemical Recommendations",
        "Many existing tools immediately recommend expensive, patented synthetic fungicides and chemical pesticides that damage soil microbiomes and are unavailable in local Indian markets.",
    )

    pdf.section_subtitle("1.2 The FLORAai Solution Architecture")
    pdf.paragraph(
        "FLORAai is designed from the ground up to solve these three specific dilemmas through a three-pronged innovation:"
    )
    pdf.bullet_point(
        "Domain-Specialized Subcontinent Dataset (63 Species)",
        "Spanning 8 core categories: Staple Grains (Rice, Wheat), Cash Crops (Sugarcane, Cotton), Plantation Crops (Tea, Coffee), Fruit Trees (Mango, Guava, Jackfruit, Papaya), Kitchen Spices (Curry Leaf, Cardamom, Turmeric, Black Pepper, Clove, Cinnamon), Sacred Flowers (Hibiscus, Lotus, Jasmine), Ayurvedic Herbs (Tulsi, Neem, Giloy, Ashwagandha), and a dedicated 12-species Palm Herbarium.",
    )
    pdf.bullet_point(
        "Multimodal AI Vision with Plain-English Translation",
        "Leverages Google Gemini Vision with strict custom prompt engineering that forbids academic Latin jargon and strictly mandates everyday terms (e.g., 'leaves turning yellow', 'cottony white sap bugs', 'damp weather mold').",
    )
    pdf.bullet_point(
        "100% Accessible Organic & Ayurvedic Remedies",
        "Provides realistic, non-toxic remedies widely accessible across Indian households and rural villages (cold-pressed neem oil spray, wood ash silica dusting, sour buttermilk probiotic wash, Trichoderma bio-fungicide, and jeevamrut organic drenches).",
    )

    pdf.callout_box(
        "Key Differentiator to Emphasize to Your Teacher:",
        [
            "\"Sir/Ma'am, unlike commercial apps that push expensive chemical fertilizers, FLORAai's diagnostic protocol prioritizes sustainable organic farming and traditional Indian bio-remedies, making plant healthcare eco-friendly, cost-effective, and safe for home gardens.\"",
        ],
        accent_color=COLOR_GOLD,
        bg_color=(254, 252, 232),
    )

    # =========================================================================
    # PAGE 3: END-TO-END SYSTEM WORKFLOW
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("2", "End-to-End System Workflow")

    pdf.paragraph(
        "When explaining how the website works to your teacher, describe the end-to-end journey in 6 distinct sequential stages. "
        "This demonstrates that you understand the entire client-server data lifecycle."
    )

    pdf.section_subtitle("Stage 1: User Interaction & Image Acquisition (Frontend)")
    pdf.paragraph(
        "The user navigates to the 'Plant Care Studio' (/dashboard). They have two options: either click 'Upload Photo' to select a picture from their device, or click 'Take Photo' to invoke the device camera. "
        "The frontend uses the modern HTML5 MediaDevices API (navigator.mediaDevices.getUserMedia) configured with facingMode: 'environment' to directly activate the back camera on smartphones and tablets."
    )

    pdf.section_subtitle("Stage 2: Client-Side Frame Capture & Base64 Serialization")
    pdf.paragraph(
        "When the user snaps a photo, a hidden HTML5 <canvas> element dynamically grabs the video frame at full native resolution and renders it as an optimized JPEG Base64 data string (canvas.toDataURL('image/jpeg', 0.9)). "
        "This eliminates the need for multipart file uploads and ensures fast, resilient asynchronous transmission."
    )

    pdf.section_subtitle("Stage 3: Secure API Dispatch to FastAPI Asynchronous Backend")
    pdf.paragraph(
        "The React client sends a POST request to http://localhost:8001/api/scans with a JSON payload containing { image_base64, plant_name }. "
        "The request passes through an authentication middleware: FastAPI validates the user's JSON Web Token (JWT) stored in a secure, HttpOnly, SameSite cookie, ensuring only authenticated users can trigger diagnostics."
    )

    pdf.section_subtitle("Stage 4: AI Multimodal Processing & Visual Reasoning")
    pdf.paragraph(
        "Inside backend/plant_ai.py, the analyze_plant() engine formats the Base64 image and feeds it to Google Gemini Vision along with a specialized system prompt. "
        "The AI analyzes leaf venation, color distortion, lesions, insect webbing, and stem structures. It enforces a strict visual distinction rule (for example, separating Lipstick Palm's vibrant scarlet crownshafts from Areca Palm's green canes)."
    )

    pdf.section_subtitle("Stage 5: Taxonomy Normalization & Knowledge Cross-Referencing")
    pdf.paragraph(
        "The Vision model's response is parsed as a standardized JSON object. The backend cross-references the detected plant against EXPANDED_BOTANICAL_KNOWLEDGE and _PLANT_ALIASES. "
        "If the user uploaded a photo of a sick plant, the backend verifies symptoms against ground-truth remedies. If external network is offline, a deterministic offline reference engine seamlessly serves verified reference profiles."
    )

    pdf.section_subtitle("Stage 6: MongoDB Persistence & Dynamic Frontend Visualization")
    pdf.paragraph(
        "The complete diagnostic report (health score, confidence, symptoms, causes, organic remedies, precautions, timestamp) is written as an immutable document into MongoDB's 'scans' collection. "
        "The frontend receives the JSON response in real-time, displays an animated health gauge (0-100 score), a status badge (Healthy / Leaf Spot / Pest Infestation / Blight), step-by-step remedy cards, and a verified photo of the species."
    )

    pdf.callout_box(
        "How to summarize the workflow in 15 seconds to your teacher:",
        [
            "\"User snaps a photo -> Frontend encodes it to Base64 -> FastAPI validates JWT auth -> Gemini Vision AI diagnoses leaf pathology -> Backend normalizes data against 63 Indian species catalog -> Record saves to MongoDB -> Interactive health card renders with organic remedies.\"",
        ],
        accent_color=COLOR_EMERALD,
        bg_color=COLOR_MINT_BG,
    )

    # =========================================================================
    # PAGE 4: TECHNOLOGY STACK & PROGRAMMING LANGUAGES
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("3", "Technology Stack & Programming Languages")

    pdf.paragraph(
        "Your teacher will certainly ask: 'What languages and libraries did you use, and why did you choose them?' "
        "Use this comprehensive matrix to justify every architectural decision:"
    )

    tech_headers = ["Layer", "Technology", "Language", "Why Selected (Technical Justification)"]
    tech_widths = [28, 38, 28, 80]
    tech_rows = [
        [
            "Frontend UI",
            "React 18 (CRACO)",
            "JavaScript (ES6+)",
            "Component-based architecture, reactive state management (useState, useEffect), blazing fast Virtual DOM updates.",
        ],
        [
            "Styling & Design",
            "Vanilla CSS +\nTailwind Tokens",
            "CSS3",
            "Zero bloated runtime. Custom HSL color design tokens, rich glassmorphism, responsive across mobile, tablet, and desktop.",
        ],
        [
            "UI Components",
            "Radix UI Primitives",
            "JSX",
            "Unstyled, fully accessible (WAI-ARIA compliant) modal dialogs, dropdowns, alerts, and navigation menus.",
        ],
        [
            "Backend Server",
            "FastAPI",
            "Python 3.9 / 3.10",
            "High performance asynchronous execution (async/await), automatic OpenAPI documentation, and native Pydantic schema validation.",
        ],
        [
            "ASGI Server",
            "Uvicorn",
            "Python",
            "Lightweight, lightning-fast lightning ASGI server powering asynchronous request handling with zero thread-blocking.",
        ],
        [
            "Database",
            "MongoDB 7.0",
            "NoSQL BSON",
            "Schema flexibility for unstructured botanical diagnostics (arrays of remedies, precautions, symptoms) and high write throughput.",
        ],
        [
            "Database Driver",
            "Motor",
            "Python (Async)",
            "Non-blocking asynchronous driver allowing FastAPI to interact with MongoDB without stalling the event loop.",
        ],
        [
            "Authentication",
            "PyJWT + Bcrypt",
            "Python",
            "Stateless, tamper-proof JSON Web Tokens. Salted password hashing (12 rounds) prevents rainbow table attacks. Stored in HttpOnly cookies.",
        ],
        [
            "AI / Vision",
            "Google Gemini Vision",
            "REST / Python",
            "State-of-the-art multimodal vision model capable of zero-shot visual pathology analysis and structured JSON adherence.",
        ],
        [
            "DevOps / Deploy",
            "Docker & Compose",
            "YAML / Dockerfile",
            "Containerizes Frontend (Nginx), Backend (Python), and MongoDB into isolated, reproducible production microservices.",
        ],
    ]
    pdf.draw_table(tech_headers, tech_rows, tech_widths)

    pdf.section_subtitle("3.1 Security Architecture Highlights")
    pdf.bullet_point(
        "HttpOnly & SameSite Cookie Protection",
        "Tokens are stored in cookies inaccessible to JavaScript (document.cookie), completely neutralizing Cross-Site Scripting (XSS) token theft.",
    )
    pdf.bullet_point(
        "Brute-Force Rate Limiting",
        "Backend tracks IP and email login attempts. Five consecutive failures trigger an automatic 15-minute security lockout.",
    )
    pdf.bullet_point(
        "Strict Input Sanitization",
        "Pydantic models validate all incoming payloads; unauthorized or malformed data is rejected before reaching business logic.",
    )

    # =========================================================================
    # PAGE 5: AI & MACHINE LEARNING ROADMAP
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("4", "AI & Machine Learning Roadmap")

    pdf.paragraph(
        "When explaining the AI/Machine Learning aspect of FLORAai, teachers love to hear about the engineering methodology, "
        "the curation of training/ground-truth knowledge, and how hallucinations were prevented."
    )

    pdf.section_subtitle("Phase 1: Domain Scoping & Taxonomy Definition")
    pdf.paragraph(
        "We surveyed the primary agricultural, horticultural, and kitchen plants grown across the agro-climatic zones of India, Pakistan, Bangladesh, and Sri Lanka. "
        "We curated a standardized 63-species botanical master catalog organized into 8 distinct botanical categories:"
    )

    cat_headers = ["Category", "Species Count", "Key Representative Plants"]
    cat_widths = [45, 28, 101]
    cat_rows = [
        ["Palms & Architectural", "12 species", "Coconut, Areca, Palmyra, Lipstick, Date, Wild Date, Fish-tail, Golden Cane, Royal, Foxtail, Bottle, Bismarck"],
        ["Staple Field Crops", "6 species", "Rice/Paddy (Dhan), Wheat (Gehun), Sugarcane, Cotton, Pearl Millet, Finger Millet"],
        ["Plantation & Cash Crops", "6 species", "Tea Bush (Chai), Coffee (Kaapi), Mustard, Chickpea, Pigeon Pea, Sesame"],
        ["Kitchen Vegetables", "10 species", "Tomato, Brinjal, Green Chilli, Okra (Bhindi), Bitter Gourd, Bottle Gourd, Coriander, Fenugreek, Moringa, Spinach"],
        ["Fruit Orchards", "9 species", "Mango (Alphonso/Kesar), Guava, Papaya, Lemon, Pomegranate, Jackfruit, Amla, Jamun, Sapota"],
        ["Sacred & Courtyard Flowers", "6 species", "Hibiscus (Gudhal), Jasmine (Mogra), Indian Rose, Marigold, Plumeria (Champa), Lotus"],
        ["Kitchen Spices", "7 species", "Curry Leaf (Kadi Patta), Cardamom (Elaichi), Turmeric (Haldi), Black Pepper, Cinnamon, Clove, Ginger"],
        ["Ayurvedic Medicinal Flora", "7 species", "Tulsi (Holy Basil), Neem Tree, Aloe Vera, Giloy (Guduchi), Ashwagandha, Betel Leaf (Paan), Brahmi"],
    ]
    pdf.draw_table(cat_headers, cat_rows, cat_widths)

    pdf.section_subtitle("Phase 2: Visual Discrimination & System Prompt Engineering")
    pdf.paragraph(
        "A common failure of generic AI vision models is misidentifying species with similar leaf structures (such as Lipstick Palm vs. Areca Palm, or Mango vs. Guava leaves). "
        "We engineered precise negative prompt constraints and visual discrimination markers:"
    )
    pdf.bullet_point(
        "Visual Disambiguation Rule",
        "If clustering palm stems display vivid scarlet, crimson, or orange-red crownshafts (Cyrtostachys renda), the model is strictly instructed to classify it as Lipstick Palm, NOT Areca Palm.",
    )
    pdf.bullet_point(
        "Ground Truth Anchoring",
        "If visual features match a catalog plant, the model must adopt standardized botanical taxonomy (common name, regional Hindi/Indian name, and scientific Latin binomial).",
    )

    pdf.section_subtitle("Phase 3: The Plain-English & Organic Remedy Layer")
    pdf.paragraph(
        "We enforced five strict language transformation rules in the LLM instruction set: (1) Ban dense academic jargon like chlorosis, necrosis, and etiology; (2) Describe physical signs plainly ('leaves turning yellow', 'cottony white bugs'); "
        "(3) Explain root causes intuitively ('too much dampness rotting the roots'); (4) Recommend realistic organic Indian remedies (neem oil spray, diluted sour buttermilk spray, wood ash silica, Trichoderma bio-fungicide); "
        "and (5) Provide actionable future care precautions."
    )

    pdf.section_subtitle("Phase 4: High-Availability Offline Reference Engine")
    pdf.paragraph(
        "To guarantee 100% uptime during exams or network disruptions, we implemented a deterministic fallback engine (_fallback_result). "
        "If the LLM API is unreachable, the system automatically retrieves ground-truth botanical records and flags the result gracefully with is_mock: true, ensuring the website never crashes."
    )

    # =========================================================================
    # PAGE 6: WORD-FOR-WORD PRESENTATION SCRIPT
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("5", "Word-for-Word Teacher Presentation Script")

    pdf.paragraph(
        "Use this word-for-word script during your project demonstration. Read it with confidence, pacing your voice smoothly:"
    )

    pdf.callout_box(
        "1. Introduction & Project Motivation (0:00 - 1:30):",
        [
            "\"Good morning/afternoon, Sir/Ma'am. Today I am proud to present FLORAai, an AI-powered Botanical Health and Plant Intelligence platform engineered specifically for the flora of the Indian subcontinent.",
            "As we know, early detection of plant disease is vital for Indian agriculture and terrace gardening. However, when a plant gets sick, farmers and gardeners face two big obstacles: existing diagnostic apps are trained on Western flora and fail on native crops, and they output confusing Latin jargon like 'foliar necrosis' with expensive chemical recommendations.",
            "I developed FLORAai to solve this: a user can take a photo of any crop, fruit tree, spice, or palm. The AI identifies the species, assesses health from 0 to 100, explains the problem in everyday simple English, and prescribes 100% organic, accessible home remedies like neem oil, wood ash, and buttermilk spray.\"",
        ],
        accent_color=COLOR_FOREST,
        bg_color=COLOR_MINT_BG,
    )

    pdf.callout_box(
        "2. Technical Architecture Overview (1:30 - 3:00):",
        [
            "\"Behind the scenes, FLORAai is built on a clean modern decoupled architecture:",
            "- On the Frontend, I used React 18 with CRACO and Tailwind CSS tokens, ensuring a responsive, glassmorphic UI that adapts perfectly across mobile phones, tablets, and desktops.",
            "- On the Backend, I chose FastAPI in Python 3.10. FastAPI provides high-speed asynchronous endpoint handling, automatic Pydantic data validation, and non-blocking I/O.",
            "- For Database storage, I utilized MongoDB with Motor, an async driver. MongoDB's document model allows us to store complex, rich diagnostic reports containing dynamic arrays of symptoms and remedies.",
            "- For Security, I implemented full JWT authentication with bcrypt password hashing and HttpOnly, SameSite cookies, which completely prevents token theft via Cross-Site Scripting (XSS).\"",
        ],
        accent_color=COLOR_EMERALD,
        bg_color=COLOR_MINT_BG,
    )

    pdf.callout_box(
        "3. Machine Learning & Domain Intelligence (3:00 - 4:30):",
        [
            "\"The intelligence core uses Google Gemini Vision multimodal reasoning combined with our curated 63-species Indian botanical master database.",
            "A key engineering milestone was our visual discrimination system. For instance, in our 12-species Palm Herbarium, distinguishing an ornamental Lipstick Palm from an Areca Palm requires fine-grained prompt constraints targeting the scarlet crownshaft.",
            "Furthermore, our multi-tier alias resolution algorithm normalizes regional names—so whether a user types 'Khajoor', 'Pind Khajoor', or 'Date Palm', the system maps it accurately to Phoenix dactylifera with full diagnostic ground truth.\"",
        ],
        accent_color=COLOR_GOLD,
        bg_color=(254, 252, 232),
    )

    pdf.callout_box(
        "4. Conclusion & Handover for Live Demo (4:30 - 5:00):",
        [
            "\"Finally, the entire stack is containerized using Docker and Docker Compose, making it production-ready for cloud deployment on any Linux server.",
            "I would now like to give you a live demonstration of FLORAai in action.\"",
        ],
        accent_color=COLOR_FOREST,
        bg_color=COLOR_MINT_BG,
    )

    # =========================================================================
    # PAGE 7: LIVE DEMO WALKTHROUGH GUIDE
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("6", "Live Demonstration Walkthrough Guide")

    pdf.paragraph(
        "Follow these exact screen actions during your live demo. Each step includes the physical action to take and the exact sentence to speak:"
    )

    pdf.section_subtitle("Step 1: The Landing Page & Species Showcase")
    pdf.bullet_point(
        "What to do",
        "Open http://localhost:3000 in your browser. Scroll smoothly through the homepage hero section down to the 'Signature Indian Flora Showcase'.",
    )
    pdf.bullet_point(
        "What to say",
        "\"Here is our responsive homepage. You can see our curated showcase highlighting signature Indian plants like Curry Leaf, Tulsi, Neem, and Coconut. Each card reveals verified photographs, botanical family, and cultural role.\"",
    )

    pdf.section_subtitle("Step 2: Authentication & Security")
    pdf.bullet_point(
        "What to do",
        "Click 'Sign In' or 'Sign Up'. Log in with the pre-seeded admin account (amrutachari11112086@gmail.com).",
    )
    pdf.bullet_point(
        "What to say",
        "\"Our authentication system uses 12-round salted bcrypt hashing and issues dual JWT access and refresh tokens stored securely in HttpOnly cookies, protecting user privacy and preventing session hijacking.\"",
    )

    pdf.section_subtitle("Step 3: The Plant Care Studio (Camera & Upload)")
    pdf.bullet_point(
        "What to do",
        "Navigate to 'Plant Care Studio' (/dashboard). Click the 'Palms & Big Plants' dropdown to show the 12 palm species. Then either take a camera photo or upload a sample plant image.",
    )
    pdf.bullet_point(
        "What to say",
        "\"This is our Plant Care Studio. Notice how our dropdown covers all major agricultural crops and our newly expanded 12-species palm herbarium—including Date Palm (Khajoor), Wild Date Palm, Fish-tail Palm, and Bismarck Palm. Users can also select 'Auto-detect' to let the AI classify the species purely from the image.\"",
    )

    pdf.section_subtitle("Step 4: Real-Time Diagnostic Analysis")
    pdf.bullet_point(
        "What to do",
        "Click the green 'Analyze Plant Health' button. The animated analysis radar activates.",
    )
    pdf.bullet_point(
        "What to say",
        "\"The frontend converts the image frame to Base64 and dispatches it asynchronously to FastAPI. The vision model analyzes leaf venation, fungal spots, and chlorosis patterns against our Indian pathogen database.\"",
    )

    pdf.section_subtitle("Step 5: The Diagnostic Report Card")
    pdf.bullet_point(
        "What to do",
        "Show the generated diagnostic card: point out the Health Score (e.g. 95%), Status Badge, Problem Cause, Organic Remedies, and Precautions.",
    )
    pdf.bullet_point(
        "What to say",
        "\"Here is the generated diagnosis. Notice that instead of confusing Latin terms, the cause is explained in simple everyday English. Look at the prescribed remedies: 100% natural and accessible—such as cold-pressed neem oil spray and sour buttermilk foliar wash.\"",
    )

    pdf.section_subtitle("Step 6: Private Scan History & Data Export")
    pdf.bullet_point(
        "What to do",
        "Click 'My Scan History' in the navigation bar. Show the search bar, status filters, and the 'Export History (JSON)' button.",
    )
    pdf.bullet_point(
        "What to say",
        "\"Every scan is archived in the user's private MongoDB collection. Users can filter by health status, search past diagnoses, and export their full history for record-keeping or agricultural audits.\"",
    )

    # =========================================================================
    # PAGE 8: VIVA VOCE & TEACHER Q&A
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("7", "Examiner & Teacher Viva Q&A (Top 10 Questions)")

    pdf.paragraph(
        "Teachers and external examiners love to ask deep architectural and conceptual questions. Here are the top 10 questions with winning answers:"
    )

    qa_list = [
        (
            "Q1: Why did you choose MongoDB over a relational database like MySQL or PostgreSQL?",
            "Ans: Botanical health reports are semi-structured and dynamic. Each diagnostic result contains varying numbers of observed symptoms, multi-step organic remedies, and seasonal precautions. In SQL, this would require 4 or 5 normalized tables with foreign keys and expensive JOIN operations. In MongoDB, the entire diagnostic report is stored as a single, natural BSON document, which delivers faster read/write speeds and effortless schema evolution.",
        ),
        (
            "Q2: How does the AI Vision model differentiate between very similar species like Areca Palm and Lipstick Palm?",
            "Ans: We engineered explicit visual discrimination heuristics into the multimodal prompt. For Lipstick Palm (Cyrtostachys renda), we instructed the model to look specifically for intense scarlet or orange-red crownshafts and upper stem sheaths, strictly barring it from misidentifying it as green-stemmed Areca Palm. We also built an alias resolution dictionary that maps regional Hindi/Bengali names to standardized botanical ground truth.",
        ),
        (
            "Q3: Why did you use FastAPI instead of traditional Flask or Django?",
            "Ans: FastAPI is built on top of Starlette and asyncio, making it one of the fastest Python web frameworks in existence—comparable in speed to NodeJS and Go. It handles thousands of concurrent requests without blocking. Furthermore, its native integration with Pydantic ensures strict runtime type-checking and automated OpenAPI documentation.",
        ),
        (
            "Q4: How do you protect user authentication tokens from theft?",
            "Ans: We do not store tokens in localStorage where vulnerable third-party JavaScript scripts could access them via Cross-Site Scripting (XSS). Instead, our dual JWT architecture (15-min access token and 7-day refresh token) is stored exclusively in HttpOnly, SameSite cookies with path restrictions, making them completely invisible to malicious client scripts.",
        ),
        (
            "Q5: What happens if the external AI service rate-limits or the internet fails during evaluation?",
            "Ans: We implemented a fault-tolerant fallback engine (_fallback_result). If the LLM network request times out, the backend gracefully queries our internal 63-species knowledge base, returns a high-confidence verified profile with is_mock: true, and keeps the user interface responsive without ever throwing an unhandled 500 server crash.",
        ),
        (
            "Q6: Why did you convert photos to Base64 instead of uploading files to Amazon S3?",
            "Ans: Direct Base64 encoding allows instant client-side canvas serialization and asynchronous JSON transport without requiring cloud bucket storage fees, external S3 API credentials, or temporary server disk cleanup crons. This keeps the application 100% self-contained and deployable on any local or offline server.",
        ),
        (
            "Q7: How do you handle password storage securely?",
            "Ans: Passwords are never stored in plaintext. We use the industry-standard bcrypt algorithm with a cost factor (salt rounds) of 12. Bcrypt incorporates a cryptographic random salt that completely neutralizes rainbow table attacks and slows down brute-force hardware crackers.",
        ),
        (
            "Q8: What is CRACO and why did you use it in the React frontend?",
            "Ans: CRACO stands for Create React App Configuration Override. It allowed us to customize Webpack loaders, PostCSS plugins, and Tailwind utility compilation without having to run 'npm run eject', which would clutter the repository with thousands of lines of fragile build configuration scripts.",
        ),
        (
            "Q9: How is the application prepared for cloud deployment?",
            "Ans: The project contains production multi-stage Dockerfiles for both frontend (using Nginx alpine to serve static assets) and backend (Python 3.10 slim), orchestrated via a single docker-compose.yml file that launches MongoDB, FastAPI, and React in isolated network containers with persistent data volumes.",
        ),
        (
            "Q10: What future enhancements are planned for FLORAai?",
            "Ans: Future iterations will include: (1) Voice-assisted regional audio output in Hindi, Marathi, and Tamil for rural farmers; (2) An on-device quantized TensorFlow Lite model for 100% offline edge inference on low-cost smartphones; and (3) IoT soil-sensor telemetry integration.",
        ),
    ]

    for q, a in qa_list:
        pdf.callout_box(q, [a], accent_color=COLOR_FOREST, bg_color=COLOR_CARD_BG)

    # =========================================================================
    # PAGE 9: DOCKER DEPLOYMENT & CONCLUSION
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("8", "Docker Deployment, Git Repository & Conclusion")

    pdf.section_subtitle("8.1 Production Containerization with Docker Compose")
    pdf.paragraph(
        "Demonstrate to your teacher that your project is not just a toy prototype, but a production-ready application packaged with industry-standard containerization:"
    )

    pdf.bullet_point(
        "Backend Container (Dockerfile)",
        "Built on python:3.10-slim. Installs required dependencies (FastAPI, Motor, PyJWT, Uvicorn), copies the server code, exposes port 8001, and runs via Uvicorn ASGI.",
    )
    pdf.bullet_point(
        "Frontend Container (Dockerfile)",
        "Multi-stage Dockerfile: Stage 1 compiles the React bundle with Node 18; Stage 2 copies the optimized production build to an ultra-lightweight Nginx Alpine web server on port 3000.",
    )
    pdf.bullet_point(
        "Database Container (MongoDB 7.0)",
        "Spins up official MongoDB 7.0 with a persistent named Docker volume (flora_mongo_data) so user accounts and diagnostic scans survive container restarts.",
    )
    pdf.bullet_point(
        "Single-Command Deployment",
        "Any evaluator can clone the repository, execute 'docker compose up -d --build', and have the entire system live in under 2 minutes.",
    )

    pdf.section_subtitle("8.2 Safe Version Control & Git Repository")
    pdf.paragraph(
        "The complete project is published and tracked on GitHub at:"
    )
    pdf.bullet_point("Repository URL", "https://github.com/AMRUTACHARI/Amrutproject")
    pdf.bullet_point("Default Branch", "main (fully synchronized and active)")
    pdf.bullet_point("Secrets Management", ".env files are strictly excluded via .gitignore; .env.example templates provide safe reference configurations.")

    pdf.section_subtitle("8.3 Closing Statement for Your Defense")
    pdf.callout_box(
        "Your Final Project Defense Closing Line:",
        [
            "\"In summary, FLORAai successfully bridges the gap between modern artificial intelligence and real-world agricultural healthcare.",
            "By pairing Google Gemini Vision multimodal reasoning with an exhaustive 63-species Indian botanical catalog, plain-English symptom translation, and accessible organic remedies, FLORAai empowers Indian farmers and home gardeners to heal their plants safely, affordably, and sustainably.",
            "Thank you, Sir/Ma'am. I am now open to any further questions or technical code inspection.\"",
        ],
        accent_color=COLOR_EMERALD,
        bg_color=COLOR_MINT_BG,
    )

    # Save PDF
    out_path = Path(OUTPUT_PDF)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out_path))
    print(f"Successfully generated PDF: {out_path} ({out_path.stat().st_size} bytes, {pdf.page_no()} pages)")


if __name__ == "__main__":
    build_explanation_pdf()
