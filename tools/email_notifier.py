import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config


def send_report(sender_email: str, sender_password: str, receiver_email: str,
                new_discoveries: list) -> bool:
    if not new_discoveries:
        print("   📭 无新发现，不发送邮件")
        return False

    today = datetime.now().strftime("%Y-%m-%d")

    rows = ""
    for d in new_discoveries:
        rows += f"""
        <tr>
            <td style="padding:8px; border-bottom:1px solid #ddd;">{d.get('species', '未知')}</td>
            <td style="padding:8px; border-bottom:1px solid #ddd; color:#c0392b; font-weight:bold;">{d.get('category', '?')}</td>
            <td style="padding:8px; border-bottom:1px solid #ddd;">{d.get('location', '未知')}</td>
            <td style="padding:8px; border-bottom:1px solid #ddd;">{d.get('observed_on', '?')}</td>
        </tr>"""

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>🌍 InvasiveGuard 濒危物种监测日报</h2>
        <p><strong>日期：</strong>{today}</p>
        <p><strong>监测范围：</strong>IUCN红色名录 EN/CR/EW 等级物种</p>
        <p><strong>新发现观察记录：{len(new_discoveries)} 条</strong></p>
        
        <table style="border-collapse:collapse; width:100%; margin-top:15px;">
            <tr style="background:#2c3e50; color:white;">
                <th style="padding:10px; text-align:left;">物种</th>
                <th style="padding:10px; text-align:left;">濒危等级</th>
                <th style="padding:10px; text-align:left;">发现地点</th>
                <th style="padding:10px; text-align:left;">观察日期</th>
            </tr>
            {rows}
        </table>
        
        <p style="margin-top:20px; color:#7f8c8d; font-size:12px;">
            本邮件由 InvasiveGuard 自动监测系统发送<br>
            数据来源：IUCN Red List + iNaturalist
        </p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🌍 InvasiveGuard 濒危物种监测日报 - {today}"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        server = smtplib.SMTP(config.EMAIL_SMTP_SERVER, config.EMAIL_SMTP_PORT)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("   ✅ 邮件发送成功")
        return True
    except smtplib.SMTPAuthenticationError:
        print("   ❌ 邮箱认证失败，请确认使用Gmail应用专用密码（非Gmail登录密码）")
        return False
    except Exception as e:
        print(f"   ❌ 邮件发送失败: {e}")
        return False
