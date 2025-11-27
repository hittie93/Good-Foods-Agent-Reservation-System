"""SQLite-backed persistence for GoodFoods reservations.

This module is intentionally small and framework-free.
"""

import os
import sqlite3
from typing import Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "reservations.db")


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the reservations table if it does not exist."""
    conn = _get_conn()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reservations (
                id TEXT PRIMARY KEY,
                restaurant_id TEXT NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                party_size INTEGER NOT NULL,
                datetime TEXT NOT NULL,
                special_requests TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                cancelled_at TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def list_reservations_by_phone(phone: str) -> list[dict]:
    """Return all reservations (active or cancelled) for a given phone number."""
    init_db()
    conn = _get_conn()
    try:
        cur = conn.execute(
            "SELECT * FROM reservations WHERE phone = ? ORDER BY datetime",
            (phone,),
        )
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def save_reservation(rec: Dict[str, Any]) -> None:
    """Insert or replace a reservation row based on its id."""
    init_db()
    conn = _get_conn()
    try:
        conn.execute(
            """
            INSERT OR REPLACE INTO reservations (
                id, restaurant_id, name, phone, party_size, datetime,
                special_requests, status, created_at, cancelled_at
            ) VALUES (:id, :restaurant_id, :name, :phone, :party_size, :datetime,
                     :special_requests, :status, :created_at, :cancelled_at)
            """,
            rec,
        )
        conn.commit()
    finally:
        conn.close()


def mark_cancelled(res_id: str, cancelled_at: str) -> None:
    """Mark an existing reservation as cancelled in the database."""
    init_db()
    conn = _get_conn()
    try:
        conn.execute(
            """
            UPDATE reservations
            SET status = 'cancelled', cancelled_at = :cancelled_at
            WHERE id = :id
            """,
            {"id": res_id, "cancelled_at": cancelled_at},
        )
        conn.commit()
    finally:
        conn.close()
