"""R1 — Out-of-band notification on configuration change within 15 min.

Protocol:
  1. Record the provider API's current forwarder list and the owner-of-record
     out-of-band notification endpoint (SMS / alt-mailbox / webhook).
  2. Add a canary forwarder via the provider's forwarder-create API.
  3. Within the SLA window (15 minutes), poll the out-of-band endpoint for the
     notification. Pass if present within the window and the event correctly
     identifies the added forwarder; fail otherwise.
  4. Clean up: delete the canary forwarder.
"""
from __future__ import annotations

import time
import uuid


def run(target: str, credentials: dict, verbose: bool = False) -> tuple[bool, str]:
    SLA_SECONDS = 15 * 60
    canary_source = f"canary-r1-{uuid.uuid4().hex[:8]}@{credentials.get('domain','example.test')}"
    canary_dest   = credentials.get("canary_destination", "canary-dest@example.test")

    # 1. Snapshot the out-of-band inbox for the owner-of-record.
    # 2. Create the canary forwarder.
    # 3. Poll the OOB inbox at 30s intervals up to the SLA.
    # 4. On receipt (or SLA expiry) delete the canary.
    # 5. Return (ok, detail).

    # The runner is a staging-interaction harness. Each provider implements its
    # own test shim that fills in the three provider-specific hooks:
    #   - create_forwarder(target, credentials, source, dest) -> forwarder_id
    #   - delete_forwarder(target, credentials, forwarder_id) -> None
    #   - poll_oob_inbox(credentials, matching) -> message | None
    #
    # In the open template below they are stubs so a provider can run the
    # harness end-to-end with their own adapters plugged in.

    try:
        from .adapters import create_forwarder, delete_forwarder, poll_oob_inbox
    except ImportError:
        return False, "No adapters module. See conformance/tests/adapters.py.template."

    forwarder_id = create_forwarder(target, credentials, canary_source, canary_dest)
    try:
        deadline = time.time() + SLA_SECONDS
        while time.time() < deadline:
            msg = poll_oob_inbox(credentials, matching=canary_source)
            if msg:
                return True, f"OOB notification received at {msg.get('received_at','?')}"
            time.sleep(30)
        return False, "No OOB notification within 15-minute SLA"
    finally:
        delete_forwarder(target, credentials, forwarder_id)
