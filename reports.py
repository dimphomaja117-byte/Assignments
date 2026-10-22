# reports.py
# This file generates reports for admins and system operators.

from database import get_connection


def campus_summary(campus_id):
    # Returns a summary for one campus:
    # total bookings, most used resource, average duration
    conn = get_connection()
    cursor = conn.cursor()

    # Total number of bookings
    cursor.execute(
        "SELECT COUNT(*) AS total FROM bookings WHERE campus_id = ?",
        (campus_id,)
    )
    total = cursor.fetchone()["total"]

    # Most used resource
    cursor.execute("""
        SELECT r.name AS resource_name, COUNT(*) AS uses
        FROM bookings b
        JOIN resources r ON b.resource_id = r.id
        WHERE b.campus_id = ?
        GROUP BY b.resource_id
        ORDER BY uses DESC
        LIMIT 1
    """, (campus_id,))
    top = cursor.fetchone()
    most_used = top["resource_name"] if top else "N/A"
    most_used_count = top["uses"] if top else 0

    # Average booking duration
    cursor.execute(
        "SELECT AVG(duration) AS avg_dur FROM bookings WHERE campus_id = ?",
        (campus_id,)
    )
    avg_row = cursor.fetchone()
    avg_duration = round(avg_row["avg_dur"], 2) if avg_row["avg_dur"] else 0

    conn.close()

    return {
        "total_bookings": total,
        "most_used_resource": most_used,
        "most_used_count": most_used_count,
        "average_duration": avg_duration,
    }


def all_campuses_comparison():
    # Returns a list of stats for every campus (for the system operator)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM campuses ORDER BY name")
    campuses = cursor.fetchall()

    results = []
    for campus in campuses:
        cid = campus["id"]

        # Total bookings for this campus
        cursor.execute(
            "SELECT COUNT(*) AS total FROM bookings WHERE campus_id = ?",
            (cid,)
        )
        total = cursor.fetchone()["total"]

        # Average duration
        cursor.execute(
            "SELECT AVG(duration) AS avg_dur FROM bookings WHERE campus_id = ?",
            (cid,)
        )
        avg = cursor.fetchone()["avg_dur"]
        avg = round(avg, 2) if avg else 0

        # Total number of resources
        cursor.execute(
            "SELECT COUNT(*) AS res FROM resources WHERE campus_id = ?",
            (cid,)
        )
        resources = cursor.fetchone()["res"]

        # Most used resource
        cursor.execute("""
            SELECT r.name AS rname, COUNT(*) AS uses
            FROM bookings b
            JOIN resources r ON b.resource_id = r.id
            WHERE b.campus_id = ?
            GROUP BY b.resource_id
            ORDER BY uses DESC
            LIMIT 1
        """, (cid,))
        top = cursor.fetchone()

        results.append({
            "campus_name": campus["name"],
            "total_bookings": total,
            "average_duration": avg,
            "total_resources": resources,
            "most_used_resource": top["rname"] if top else "N/A",
        })

    conn.close()
    return results