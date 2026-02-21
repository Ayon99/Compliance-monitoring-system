import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    dbname="compliance_db",
    user="postgres",
    password="2006",
    host="localhost",
    port="5432"
)

conn.autocommit = True


def fetch_violations():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rule_name, user_id, details, detected_at
        FROM violations
        ORDER BY detected_at DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def generate_html_report(violations):
    rows_html = ""
    for v in violations:
        rows_html += f"""
        <tr>
            <td>{v[0]}</td>
            <td>{v[1]}</td>
            <td>{v[2]}</td>
            <td>{v[3]}</td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>Compliance Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; }}
            th {{ background-color: #f4f4f4; }}
        </style>
    </head>
    <body>
        <h2>Compliance Violations Report</h2>
        <p>Generated at: {datetime.utcnow()}</p>
        <table>
            <tr>
                <th>Rule</th>
                <th>User</th>
                <th>Details</th>
                <th>Detected At</th>
            </tr>
            {rows_html}
        </table>
    </body>
    </html>
    """


def run():
    violations = fetch_violations()
    html = generate_html_report(violations)

    with open("compliance_report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Report generated: compliance_report.html")


if __name__ == "__main__":
    run()
