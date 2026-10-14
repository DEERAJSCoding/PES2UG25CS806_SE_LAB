
"""Support Ticket Tracker with safer input and file handling."""

import json
import logging
import os

TICKETS = {}
VALID_STATUSES = {"open", "in_progress", "closed"}


def create_ticket(
    title,
    description,
    reporter,
    priority="medium",
    category="general",
    *,
    audit_log=None,
):
    """Create a ticket and optionally record the action in an audit log."""
    if not isinstance(title, str) or not title.strip():
        return None

    if audit_log is None:
        audit_log = []

    ticket_id = str(len(TICKETS) + 1)
    ticket = {
        "id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "open",
        "reporter": reporter,
        "assignee": None,
    }

    TICKETS[ticket_id] = ticket
    audit_log.append(f"Created ticket {ticket_id} for {reporter}")
    return ticket


def assign_ticket(ticket_id, agent, notify=False):
    """Assign a ticket to an agent."""
    ticket = TICKETS.get(str(ticket_id))
    if ticket is None:
        return False

    ticket["assignee"] = agent
    if notify:
        logging.info("Ticket %s assigned to %s", ticket_id, agent)
    return True


def update_status(ticket_id, status):
    """Update a ticket's status if the ticket and status are valid."""
    ticket = TICKETS.get(str(ticket_id))
    if ticket is None or status not in VALID_STATUSES:
        return None

    ticket["status"] = status
    return ticket


def search_tickets(status=None, priority=None):
    """Return tickets matching the supplied status and priority filters."""
    results = []
    for ticket in TICKETS.values():
        if status is not None and ticket["status"] != status:
            continue
        if priority and ticket["priority"] != priority:
            continue
        results.append(ticket)
    return results


def save_tickets(path="tickets.json"):
    """Save all tickets to a JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(TICKETS, file, indent=2)


def load_tickets(path="tickets.json"):
    """Load tickets from a JSON file."""
    with open(path, "r", encoding="utf-8") as file:
        loaded_tickets = json.load(file)

    if not isinstance(loaded_tickets, dict):
        raise ValueError("Ticket data must be a JSON object.")

    TICKETS.clear()
    TICKETS.update(loaded_tickets)


def print_ticket_report():
    """Print a summary of all tickets."""
    print("Support Tickets")
    if not TICKETS:
        print("No tickets yet")
        return

    for ticket_id, ticket in TICKETS.items():
        print(ticket_id, ticket["title"], ticket["status"])


def close_ticket(ticket_id):
    """Close a ticket, returning whether the operation succeeded."""
    ticket = TICKETS.get(str(ticket_id))
    if ticket is None:
        return False

    ticket["status"] = "closed"
    return True


def is_open(ticket_id):
    """Check whether a ticket is open or in progress."""
    ticket = TICKETS.get(str(ticket_id))
    return ticket is not None and ticket["status"] in {
        "open",
        "in_progress",
    }


def main():
    """Run a demonstration of the support ticket tracker."""
    logging.basicConfig(level=logging.INFO)

    create_ticket(
        "Cannot sign in",
        "Password reset link fails",
        "alex@example.com",
    )
    create_ticket(
        "Billing question",
        "Charged twice",
        "lee@example.com",
        "high",
    )

    assign_ticket("1", "agent-01")
    update_status("1", "in_progress")
    print_ticket_report()

    logging.info("Tickets created: %d", len(TICKETS))
    print("Ticket 1 open?", is_open("1"))

    ticket_id = input("Ticket id to close (Enter to skip): ").strip()
    if ticket_id and not close_ticket(ticket_id):
        print("Ticket not found.")

    save_tickets()

    if os.environ.get("RUN_UNSAFE_DEMO") == "1":
        print("unsafe demo")


if __name__ == "__main__":
    main()
