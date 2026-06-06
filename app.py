from flask import Flask, request, jsonify, send_file
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os
import uuid
import base64
from io import BytesIO

app = Flask(__name__)

# ── Brand Colors ──────────────────────────────────────────────────────────────
PURPLE    = colors.HexColor("#32215C")
BLUE      = colors.HexColor("#0092D4")
BLUE_LT   = colors.HexColor("#E6F4FC")
PURPLE_LT = colors.HexColor("#F0EDF8")
WHITE     = colors.white
DARK      = colors.HexColor("#1A1A2E")
MID       = colors.HexColor("#4A4A6A")
LIGHT_BG  = colors.HexColor("#F8F8FC")
GREEN     = colors.HexColor("#27AE60")
GOLD      = colors.HexColor("#F5A623")
BORDER    = colors.HexColor("#D0C8E8")

W, H = A4
CW = W - 36*mm

def S(name, **kw):
    base = dict(fontName="Helvetica", fontSize=10, leading=14, textColor=MID, spaceAfter=0, spaceBefore=0)
    base.update(kw)
    return ParagraphStyle(name, **base)

def generate_pdf(data):
    filename = f"/tmp/iti_report_{uuid.uuid4().hex}.pdf"
    
    # Extract data
    full_name     = data.get("full_name", "Participant")
    organisation  = data.get("organisation", "")
    role_level    = data.get("role_level", "")
    submission_date = data.get("submission_date", "")
    
    iti_score     = data.get("iti_score", "0")
    iti_band      = data.get("iti_band", "")
    avs           = data.get("avs", "0")
    avs_band      = data.get("avs_band", "")
    rss           = data.get("rss", "0")
    rrs           = data.get("rrs", "0")
    rrs_band      = data.get("rrs_band", "")
    igd           = data.get("igd", "0")
    igd_band      = data.get("igd_band", "")
    
    sa_avg        = data.get("sa_avg", "0")
    vv_avg        = data.get("vv_avg", "0")
    co_avg        = data.get("co_avg", "0")
    fa_avg        = data.get("fa_avg", "0")
    ab_avg        = data.get("ab_avg", "0")
    dp_avg        = data.get("dp_avg", "0")
    al_avg        = data.get("al_avg", "0")
    ri_avg        = data.get("ri_avg", "0")
    
    ai_narrative  = data.get("ai_narrative", "")

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=16*mm, bottomMargin=16*mm,
    )

    sScore  = S("sc", fontName="Helvetica-Bold", fontSize=28, textColor=PURPLE, leading=32, alignment=TA_CENTER)
    sSmall  = S("sm", fontSize=7.5, textColor=colors.HexColor("#8888AA"), leading=11, alignment=TA_CENTER)
    sTH     = S("th", fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE, leading=12, alignment=TA_CENTER)
    sTDb    = S("tb", fontName="Helvetica-Bold", fontSize=9, leading=13, textColor=DARK)
    sNarr   = S("nr", fontSize=9.5, leading=15, textColor=MID)
    sH1     = S("h1", fontName="Helvetica-Bold", fontSize=13, textColor=PURPLE, leading=18, spaceBefore=4)
    sFooter = S("ft", fontSize=7.5, textColor=colors.HexColor("#9090B0"), leading=11, alignment=TA_CENTER)

    story = []

    # ── HEADER ────────────────────────────────────────────────────────────────
    logo_path = os.path.join(os.path.dirname(__file__), "logo.jpg")
    logo = Image(logo_path, width=60*mm, height=14*mm)

    header_data = [[
        logo,
        Paragraph("IDENTITY TRAJECTORY INTELLIGENCE™<br/>Assessment Report",
            S("hr", fontName="Helvetica-Bold", fontSize=14, textColor=WHITE, leading=20, alignment=TA_RIGHT))
    ]]
    header_table = Table(header_data, colWidths=[65*mm, CW-65*mm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), PURPLE),
        ("TOPPADDING",   (0,0),(-1,-1), 14),
        ("BOTTOMPADDING",(0,0),(-1,-1), 14),
        ("LEFTPADDING",  (0,0),(-1,-1), 14),
        ("RIGHTPADDING", (0,0),(-1,-1), 14),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))

    # Info bar
    info_bar = Table([[
        Paragraph(f"{full_name}  |  {role_level}  |  {organisation}  |  {submission_date}",
            S("ib", fontSize=9, textColor=WHITE, leading=13, alignment=TA_CENTER))
    ]], colWidths=[CW])
    info_bar.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), BLUE),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
    ]))
    story.append(info_bar)
    story.append(Spacer(1, 10))

    # ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────
    story.append(Paragraph("Executive Summary", sH1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PURPLE, spaceAfter=8))

    score_data = [
        [Paragraph("IDENTITY TRAJECTORY INDEX™", S("si", fontName="Helvetica-Bold", fontSize=8, textColor=BLUE, leading=11, alignment=TA_CENTER)),
         Paragraph("CLASSIFICATION", S("si", fontName="Helvetica-Bold", fontSize=8, textColor=BLUE, leading=11, alignment=TA_CENTER))],
        [Paragraph(str(iti_score), sScore),
         Paragraph(str(iti_band), S("cl", fontName="Helvetica-Bold", fontSize=20, textColor=PURPLE, leading=24, alignment=TA_CENTER))],
        [Paragraph("out of 100", sSmall),
         Paragraph("Your advancement trajectory classification", S("cd", fontSize=8.5, textColor=MID, leading=12, alignment=TA_CENTER))],
    ]
    score_table = Table(score_data, colWidths=[CW/2-5, CW/2-5])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(0,-1), PURPLE_LT),
        ("BACKGROUND", (1,0),(1,-1), BLUE_LT),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("GRID",          (0,0),(-1,-1), 0.5, BORDER),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 8))

    summary_box = Table([[Paragraph(
        "Your ITI assessment reveals where you are on your identity and advancement journey. "
        "Review your scores, growth edges, and personalised narrative below.",
        sNarr)]], colWidths=[CW])
    summary_box.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), LIGHT_BG),
        ("TOPPADDING",   (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
        ("RIGHTPADDING", (0,0),(-1,-1), 12),
        ("LINEABOVE",    (0,0),(-1,0),  2, BLUE),
    ]))
    story.append(summary_box)
    story.append(Spacer(1, 10))

    # Core Highlights
    hw = CW/4 - 3
    highlights = [
        [Paragraph("8",  S("hv", fontName="Helvetica-Bold", fontSize=22, textColor=PURPLE, leading=26, alignment=TA_CENTER)),
         Paragraph(str(iti_score), S("hv", fontName="Helvetica-Bold", fontSize=22, textColor=PURPLE, leading=26, alignment=TA_CENTER)),
         Paragraph(str(avs), S("hv", fontName="Helvetica-Bold", fontSize=22, textColor=GREEN, leading=26, alignment=TA_CENTER)),
         Paragraph(str(rss), S("hv", fontName="Helvetica-Bold", fontSize=22, textColor=BLUE, leading=26, alignment=TA_CENTER))],
        [Paragraph("Dimensions\nAssessed", sSmall),
         Paragraph("Overall\nITI Score", sSmall),
         Paragraph("Advancement\nVelocity", sSmall),
         Paragraph("Retention\nStability", sSmall)],
    ]
    hl_table = Table(highlights, colWidths=[hw,hw,hw,hw])
    hl_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), WHITE),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("GRID",          (0,0),(-1,-1), 0.5, BORDER),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(Paragraph("Core Highlights", S("ch", fontName="Helvetica-Bold", fontSize=10, textColor=DARK, leading=14)))
    story.append(Spacer(1, 4))
    story.append(hl_table)
    story.append(Spacer(1, 12))

    # ── DIMENSIONS ────────────────────────────────────────────────────────────
    story.append(Paragraph("Core ITI Dimensions", sH1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PURPLE, spaceAfter=8))

    dims = [
        ("Self-Authority", sa_avg),
        ("Visibility & Voice", vv_avg),
        ("Capability Ownership", co_avg),
        ("Future Self Alignment", fa_avg),
        ("Advancement Behavior", ab_avg),
        ("Decision Patterns", dp_avg),
        ("Advancement Likelihood", al_avg),
        ("Retention Intent", ri_avg),
    ]

    dim_rows = [[Paragraph("Dimension", sTH), Paragraph("Score", sTH), Paragraph("Signal", sTH)]]
    for name, score in dims:
        try:
            score_val = float(score)
        except:
            score_val = 0
        if score_val >= 70: signal, col = "Strong", GREEN
        elif score_val >= 50: signal, col = "Developing", BLUE
        else: signal, col = "Growth Edge", GOLD
        dim_rows.append([
            Paragraph(name, sTDb),
            Paragraph(f"{score} / 100", S("ds", fontName="Helvetica-Bold", fontSize=9, textColor=col, leading=13, alignment=TA_CENTER)),
            Paragraph(signal, S("sg", fontSize=8.5, textColor=col, leading=13, alignment=TA_CENTER)),
        ])

    dw = [CW*0.55, CW*0.22, CW*0.23]
    dim_table = Table(dim_rows, colWidths=dw, repeatRows=1)
    dim_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  PURPLE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, PURPLE_LT]),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("GRID",          (0,0),(-1,-1), 0.4, BORDER),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(dim_table)
    story.append(Spacer(1, 12))

    # ── TRAJECTORY INDICES ────────────────────────────────────────────────────
    story.append(Paragraph("Trajectory Indices", sH1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PURPLE, spaceAfter=8))

    indices = [
        ("Identity Trajectory Index™", f"{iti_score} / 100", iti_band, PURPLE),
        ("Advancement Velocity Score™", f"{avs} / 100", avs_band, GREEN),
        ("Retention Stability Score™", f"{rss} / 100", "Stable", BLUE),
        ("Retention Risk Score™", f"{rrs} / 100", rrs_band, GREEN),
        ("Identity Gap Differential™", str(igd), igd_band, GOLD),
    ]

    idx_rows = [[Paragraph("Index", sTH), Paragraph("Score", sTH), Paragraph("Classification", sTH)]]
    for name, score, band, col in indices:
        idx_rows.append([
            Paragraph(name, sTDb),
            Paragraph(score, S("is", fontName="Helvetica-Bold", fontSize=9, textColor=col, leading=13, alignment=TA_CENTER)),
            Paragraph(band,  S("ib", fontSize=8.5, textColor=col, leading=13, alignment=TA_CENTER)),
        ])

    idx_table = Table(idx_rows, colWidths=dw, repeatRows=1)
    idx_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  BLUE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, BLUE_LT]),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("GRID",          (0,0),(-1,-1), 0.4, BORDER),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(idx_table)
    story.append(Spacer(1, 12))

    # ── AI NARRATIVE ──────────────────────────────────────────────────────────
    story.append(Paragraph("Your Personalised ITI Report", sH1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PURPLE, spaceAfter=8))

    narr_box = Table([
        [Paragraph("AI-Generated Narrative Report", S("nt", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, leading=14))],
        [Paragraph(str(ai_narrative), sNarr)],
    ], colWidths=[CW])
    narr_box.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(0,0), PURPLE),
        ("BACKGROUND",  (0,1),(0,1), WHITE),
        ("TOPPADDING",    (0,0),(-1,-1), 9),
        ("BOTTOMPADDING", (0,0),(-1,-1), 9),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("LINEBEFORE",    (0,0),(0,-1),  2, BLUE),
        ("LINEBELOW",     (0,-1),(-1,-1), 0.5, BORDER),
    ]))
    story.append(KeepTogether(narr_box))
    story.append(Spacer(1, 12))

    # ── FOOTER ────────────────────────────────────────────────────────────────
    footer = Table([[
        Paragraph(f"CONFIDENTIAL  |  Identity Trajectory Intelligence™  |  Powered by IAMWHOISAYIAM™  |  {submission_date}", sFooter)
    ]], colWidths=[CW])
    footer.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), PURPLE),
        ("TOPPADDING",   (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LEFTPADDING",  (0,0),(-1,-1), 14),
        ("RIGHTPADDING", (0,0),(-1,-1), 14),
    ]))
    story.append(footer)

    doc.build(story)
    return filename


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        pdf_path = generate_pdf(data)

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
        os.remove(pdf_path)

        return jsonify({
            "success": True,
            "pdf_base64": pdf_base64,
            "filename": f"ITI_Report_{data.get('full_name', 'Participant').replace(' ', '_')}.pdf"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "ITI PDF Generator"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
