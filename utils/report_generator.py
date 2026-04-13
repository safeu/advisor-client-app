"""
===========================================================
Report Generator
===========================================================
Script purpose:
    Generates a PDF report for a client's policy summary.
"""

from fpdf import FPDF
import io

def generate_client_report(client_name, policy, fund_info, riders, payments):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, f"Policy Summary - {client_name}", ln=True, align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, f"Total Payments Made: P {sum(p[4] for p in payments if p[6] == 'Paid' and p[4]):,.2f}", ln=True, align="C")
    pdf.ln(3)


    col_width = 95
    left_x = 10
    right_x = 105
    start_y = pdf.get_y()


    pdf.set_xy(left_x, start_y)

    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(col_width, 6, "Plan Details", ln=True)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(left_x, pdf.get_y(), left_x + col_width, pdf.get_y())
    pdf.ln(1)

    def left_row(label, value):
        pdf.set_x(left_x)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(40, 5, label, border=0)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(col_width - 40, 5, str(value) if value else "-", ln=True)

    left_row("Plan Name:", policy[2])
    left_row("Policy Number:", policy[3])
    left_row("Issue Date:", policy[4])
    left_row("Face Amount:", f"P {policy[5]:,.2f}" if policy[5] else None)
    left_row("Sum Assured:", f"P {policy[6]:,.2f}" if policy[6] else None)
    left_row("Policy Duration:", policy[7])
    left_row("Years to Pay:", policy[8])
    left_row("Remaining Years:", policy[9])
    pdf.ln(3)

    
    pdf.set_x(left_x)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(col_width, 6, "Status & Billing", ln=True)
    pdf.line(left_x, pdf.get_y(), left_x + col_width, pdf.get_y())
    pdf.ln(1)

    left_row("Status:", policy[10])
    left_row("Premium Due:", policy[11])
    left_row("Mode of Payment:", policy[12])
    left_row("Premium Amount:", f"P {policy[13]:,.2f}" if policy[13] else None)
    left_row("Total Annual Premium:", f"P {policy[14]:,.2f}" if policy[14] else None)
    pdf.ln(3)

    
    pdf.set_x(left_x)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(col_width, 6, "Fund Allocation", ln=True)
    pdf.line(left_x, pdf.get_y(), left_x + col_width, pdf.get_y())
    pdf.ln(1)

    if fund_info:
        left_row("Fund Value:", f"P {fund_info[2]:,.2f}" if fund_info[2] else None)
        left_row("Fund Name:", fund_info[3])
        left_row("Allocation:", f"{fund_info[4]}%" if fund_info[4] else None)
        left_row("Cost of Insurance:", f"P {fund_info[5]:,.2f}" if fund_info[5] else None)
        left_row("As of Date:", fund_info[6])
    pdf.ln(3)

    
    pdf.set_x(left_x)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(col_width, 6, "Supplemental Benefits", ln=True)
    pdf.line(left_x, pdf.get_y(), left_x + col_width, pdf.get_y())
    pdf.ln(1)

    if riders:
        pdf.set_x(left_x)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(60, 5, "Rider Name", border=0)
        pdf.cell(35, 5, "Amount", ln=True)
        pdf.set_font("Helvetica", "", 8)
        for r in riders:
            pdf.set_x(left_x)
            pdf.cell(60, 5, str(r[2]) if r[2] else "-", border=0)
            pdf.cell(35, 5, f"P {r[3]:,.2f}" if r[3] else "-", ln=True)
    else:
        pdf.set_x(left_x)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(col_width, 5, "No riders.", ln=True)

    
    pdf.set_xy(right_x, start_y)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(col_width, 6, "Transaction History", ln=True)
    pdf.set_xy(right_x, pdf.get_y())
    pdf.line(right_x, pdf.get_y(), right_x + col_width, pdf.get_y())
    pdf.ln(1)

    if payments:
        years = sorted(set(p[2] for p in payments))
        for year in years:
            year_payments = [p for p in payments if p[2] == year]
            year_total = sum(p[4] for p in year_payments if p[4])

            pdf.set_x(right_x)
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(col_width, 5, f"Year {year}", ln=True)

            pdf.set_x(right_x)
            pdf.set_font("Helvetica", "B", 7)
            pdf.cell(30, 4, "Due Date", border=1)
            pdf.cell(25, 4, "Amount", border=1)
            pdf.cell(30, 4, "Date Paid", border=1)
            pdf.cell(15, 4, "Status", border=1, ln=True)

            
            pdf.set_font("Helvetica", "", 7)
            for p in year_payments:
                pdf.set_x(right_x)
                pdf.cell(30, 4, str(p[3]) if p[3] else "-", border=1)
                pdf.cell(25, 4, f"P {p[4]:,.2f}" if p[4] else "-", border=1)
                pdf.cell(30, 4, str(p[5]) if p[5] else "-", border=1)
                pdf.cell(15, 4, str(p[6]) if p[6] else "-", border=1, ln=True)

            pdf.set_x(right_x)
            pdf.set_font("Helvetica", "B", 7)
            pdf.cell(85, 4, f"Year {year} Total:", border=0)
            pdf.cell(15, 4, f"P {year_total:,.2f}", border=0, ln=True)
            pdf.ln(2)
    else:
        pdf.set_x(right_x)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(col_width, 5, "No payments recorded.", ln=True)


    return bytes(pdf.output())