# report_generator.py - PDF Report Generator

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io

def generate_analysis_report(result, resume_text, job_description, user_name):
    """
    Generate a professional PDF report for skill analysis
    """
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a2e'),
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=10
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=8
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6
    )
    
    # Build content
    story = []
    
    # ============================================
    # 1. TITLE SECTION
    # ============================================
    story.append(Paragraph("🚀 SkillBridge", title_style))
    story.append(Paragraph("Professional Resume Analysis Report", subtitle_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Date and user
    story.append(Paragraph(f"📅 Report Generated: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    story.append(Paragraph(f"👤 Prepared for: {user_name}", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Divider line
    story.append(Paragraph("_" * 80, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # 2. EXECUTIVE SUMMARY
    # ============================================
    story.append(Paragraph("📊 Executive Summary", heading_style))
    ats_score = result.get("ats_score", 0)
    job_title = result.get("job_title", "Not Detected")
    
    if ats_score >= 70:
        status = "✅ Strong Match"
    elif ats_score >= 50:
        status = "⚠️ Moderate Match"
    else:
        status = "❌ Needs Improvement"
    
    summary_text = f"""
    Your resume was analyzed against the <b>{job_title}</b> position. 
    Your ATS (Applicant Tracking System) compatibility score is <b>{ats_score}%</b>, 
    which is considered a <b>{status}</b>.
    """
    story.append(Paragraph(summary_text, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # 3. ATS SCORE
    # ============================================
    story.append(Paragraph("🎯 ATS Compatibility Score", heading_style))
    
    score_data = [
        ["Score", f"{ats_score}%"],
        ["Status", status]
    ]
    
    score_table = Table(score_data, colWidths=[2*inch, 2*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f7fa')),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ]))
    
    story.append(score_table)
    story.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # 4. SKILLS ANALYSIS
    # ============================================
    story.append(Paragraph("🛠️ Skills Analysis", heading_style))
    
    skills_have = result.get("skills_have", [])
    skills_need = result.get("skills_need", [])
    skills_missing = result.get("skills_missing", [])
    
    # Skills table
    skill_data = [
        ["✅ Skills You Have", "📌 Skills You Need", "🚨 Missing Skills"]
    ]
    
    max_rows = max(len(skills_have), len(skills_need), len(skills_missing))
    for i in range(max_rows):
        have = skills_have[i] if i < len(skills_have) else ""
        need = skills_need[i] if i < len(skills_need) else ""
        missing = skills_missing[i] if i < len(skills_missing) else ""
        skill_data.append([have, need, missing])
    
    skill_table = Table(skill_data, colWidths=[2*inch, 2*inch, 2*inch])
    skill_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#e8f5e9')),
        ('BACKGROUND', (1, 1), (1, -1), colors.HexColor('#fff3e0')),
        ('BACKGROUND', (2, 1), (2, -1), colors.HexColor('#ffebee')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(skill_table)
    story.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # 5. LEARNING ROADMAP
    # ============================================
    story.append(Paragraph("📚 Personalized Learning Roadmap", heading_style))
    
    roadmap = result.get("learning_roadmap", [])
    if roadmap:
        for i, step in enumerate(roadmap, 1):
            story.append(Paragraph(f"{i}. {step}", normal_style))
    else:
        story.append(Paragraph("No learning roadmap generated.", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # 6. RESUME OPTIMIZATION TIPS
    # ============================================
    story.append(Paragraph("💡 Resume Optimization Tips", heading_style))
    
    tips = result.get("resume_tips", [])
    if tips:
        for i, tip in enumerate(tips, 1):
            story.append(Paragraph(f"💡 {tip}", normal_style))
    else:
        story.append(Paragraph("No tips generated.", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # 7. FOOTER
    # ============================================
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("_" * 80, normal_style))
    story.append(Paragraph(
        "🚀 SkillBridge - Your AI Career Coach",
        ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#999999'),
            alignment=TA_CENTER
        )
    ))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data