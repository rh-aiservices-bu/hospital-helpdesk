"""
Oak City General Hospital — IT Helpdesk Ticketing MCP Server

Exposes four tools to an LLM via the Model Context Protocol (SSE transport):
  - create_ticket
  - get_ticket
  - list_tickets
  - update_ticket
"""

import os
import uuid
from datetime import datetime
from typing import Optional

from fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Pre-seeded data
# ---------------------------------------------------------------------------

TICKETS: dict[str, dict] = {
    "TKT-001": {
        "id": "TKT-001",
        "title": "Nurse locked out of workstation — Ward 4A",
        "category": "access",
        "description": (
            "Nurse Sarah Mitchell on Ward 4A is unable to log in to her workstation. "
            "She entered her password incorrectly three times and her account is now locked. "
            "She needs access urgently to update patient records."
        ),
        "priority": "high",
        "status": "open",
        "requester": "Sarah Mitchell",
        "created_at": "2025-01-15 08:30",
        "comments": [],
    },
    "TKT-002": {
        "id": "TKT-002",
        "title": "Infusion pump showing error code 525 — ICU Bay 3",
        "category": "equipment",
        "description": (
            "The infusion pump in ICU Bay 3 is displaying error code 525 and has stopped "
            "functioning. Patient care is at risk. A replacement unit is needed immediately. "
            "The faulty unit also needs to be collected for inspection by Biomedical Engineering."
        ),
        "priority": "critical",
        "status": "open",
        "requester": "Dr. James Thompson",
        "created_at": "2025-01-15 09:15",
        "comments": [],
    },
    "TKT-003": {
        "id": "TKT-003",
        "title": "Printer unresponsive — Radiology Department (3rd Floor)",
        "category": "equipment",
        "description": (
            "The main laser printer in the Radiology department is not responding to print jobs. "
            "Radiology reports cannot be printed, causing delays in patient discharge. "
            "The printer shows a solid amber light."
        ),
        "priority": "medium",
        "status": "in_progress",
        "requester": "Maria Gonzalez",
        "created_at": "2025-01-14 14:00",
        "comments": [
            "2025-01-14 15:00 — Technician dispatched. Investigating paper jam in rear tray.",
        ],
    },
    "TKT-004": {
        "id": "TKT-004",
        "title": "EMR system extremely slow — Ward 2B",
        "category": "software",
        "description": (
            "All workstations on Ward 2B are experiencing severe slowness in the Electronic Medical "
            "Records (EMR) system. Loading a patient record takes over two minutes. "
            "Staff have already tried restarting their workstations with no improvement."
        ),
        "priority": "high",
        "status": "open",
        "requester": "Dr. Priya Patel",
        "created_at": "2025-01-15 07:45",
        "comments": [],
    },
    "TKT-005": {
        "id": "TKT-005",
        "title": "Badge access denied to pharmacy",
        "category": "access",
        "description": (
            "Dr. Linda Chen's staff badge stopped granting access to the pharmacy on Monday. "
            "Her access was working the previous week. No changes to her role have been made."
        ),
        "priority": "high",
        "status": "resolved",
        "requester": "Dr. Linda Chen",
        "created_at": "2025-01-13 11:00",
        "comments": [
            "2025-01-13 12:00 — Access permissions reviewed. Badge expired due to annual renewal cycle.",
            "2025-01-13 13:30 — New badge issued and pharmacy access restored. User notified.",
        ],
    },
}

# ---------------------------------------------------------------------------
# MCP server
# ---------------------------------------------------------------------------

mcp = FastMCP("hospital-ticketing")

VALID_CATEGORIES = {"access", "equipment", "network", "software", "facilities"}
VALID_PRIORITIES = {"low", "medium", "high", "critical"}
VALID_STATUSES = {"open", "in_progress", "resolved", "closed"}


@mcp.tool()
def create_ticket(
    title: str,
    category: str,
    description: str,
    requester_name: str,
    priority: str = "medium",
) -> dict:
    """
    Open a new IT support ticket.

    Args:
        title: Short summary of the issue (max 100 characters).
        category: One of: access, equipment, network, software, facilities.
        description: Full description of the problem.
        requester_name: Full name of the person raising the ticket.
        priority: One of: low, medium, high, critical. Defaults to medium.

    Returns:
        The newly created ticket including its assigned ID.
    """
    if category not in VALID_CATEGORIES:
        return {"error": f"Invalid category '{category}'. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}."}
    if priority not in VALID_PRIORITIES:
        return {"error": f"Invalid priority '{priority}'. Must be one of: {', '.join(sorted(VALID_PRIORITIES))}."}

    ticket_id = f"TKT-{uuid.uuid4().hex.upper()}"
    while ticket_id in TICKETS:
        ticket_id = f"TKT-{uuid.uuid4().hex.upper()}"

    ticket = {
        "id": ticket_id,
        "title": title[:100],
        "category": category,
        "description": description,
        "priority": priority,
        "status": "open",
        "requester": requester_name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "comments": [],
    }
    TICKETS[ticket_id] = ticket
    return ticket


@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """
    Retrieve a single ticket by its ID (e.g. TKT-001).

    Args:
        ticket_id: The ticket identifier.

    Returns:
        Full ticket details, or an error if not found.
    """
    ticket = TICKETS.get(ticket_id.upper())
    if not ticket:
        return {"error": f"Ticket '{ticket_id}' not found."}
    return ticket


@mcp.tool()
def list_tickets(
    status: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None,
) -> list[dict]:
    """
    List tickets, with optional filters.

    Args:
        status: Filter by status: open, in_progress, resolved, closed. Leave empty for all.
        category: Filter by category: access, equipment, network, software, facilities. Leave empty for all.
        priority: Filter by priority: low, medium, high, critical. Leave empty for all.

    Returns:
        A list of matching tickets (summary view, without full description).
    """
    results = []
    for ticket in TICKETS.values():
        if status and ticket["status"] != status:
            continue
        if category and ticket["category"] != category:
            continue
        if priority and ticket["priority"] != priority:
            continue
        results.append({
            "id": ticket["id"],
            "title": ticket["title"],
            "category": ticket["category"],
            "priority": ticket["priority"],
            "status": ticket["status"],
            "requester": ticket["requester"],
            "created_at": ticket["created_at"],
        })
    return results


@mcp.tool()
def update_ticket(
    ticket_id: str,
    status: Optional[str] = None,
    comment: Optional[str] = None,
) -> dict:
    """
    Update a ticket's status and/or add a comment to it.

    Args:
        ticket_id: The ticket identifier (e.g. TKT-001).
        status: New status: open, in_progress, resolved, closed. Leave empty to keep current.
        comment: A note to append to the ticket's comment history. Leave empty to add no comment.

    Returns:
        The updated ticket, or an error if not found.
    """
    ticket = TICKETS.get(ticket_id.upper())
    if not ticket:
        return {"error": f"Ticket '{ticket_id}' not found."}

    if status:
        if status not in VALID_STATUSES:
            return {"error": f"Invalid status '{status}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}."}
        ticket["status"] = status

    if comment:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        ticket["comments"].append(f"{timestamp} — {comment}")

    return ticket


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    mcp.run(transport="streamable-http", host=host, port=port)
