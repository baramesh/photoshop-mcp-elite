"""Photoshop AppleScript / ExtendScript Bridge.

Communicates with Adobe Photoshop via macOS AppleScript (`osascript`) and temporary JSX script files.
Includes embedded JSON polyfill for reliable ES3 ExtendScript serialization.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from typing import Any

JSON2_POLYFILL = """
if (typeof JSON === "undefined") {
    JSON = {
        stringify: function(val) {
            if (val === null || val === undefined) return "null";
            if (typeof val === "boolean" || typeof val === "number") return "" + val;
            if (typeof val === "string") {
                return "\\"" + val.replace(/\\\\/g, "\\\\\\\\")
                                  .replace(/\\"/g, "\\\\\\"")
                                  .replace(/\\n/g, "\\\\n")
                                  .replace(/\\r/g, "\\\\r")
                                  .replace(/\\t/g, "\\\\t") + "\\"";
            }
            if (val instanceof Array) {
                var items = [];
                for (var i = 0; i < val.length; i++) items.push(JSON.stringify(val[i]));
                return "[" + items.join(",") + "]";
            }
            if (typeof val === "object") {
                var props = [];
                for (var k in val) {
                    if (val.hasOwnProperty(k)) {
                        props.push("\\"" + k + "\\":" + JSON.stringify(val[k]));
                    }
                }
                return "{" + props.join(",") + "}";
            }
            return "null";
        },
        parse: function(s) {
            return eval('(' + s + ')');
        }
    };
}
"""


class PhotoshopBridge:
    def __init__(self, app_id: str = "com.adobe.Photoshop", timeout_seconds: int = 60):
        self.app_id = app_id
        self.timeout_seconds = timeout_seconds

    def execute_jsx(self, script: str, with_json_polyfill: bool = True) -> Any:
        """Executes a JSX script inside Photoshop and returns the result."""
        full_script = (JSON2_POLYFILL + "\n" + script) if with_json_polyfill else script

        with tempfile.NamedTemporaryFile(suffix=".jsx", mode="w", encoding="utf-8", delete=False) as f:
            f.write(full_script)
            jsx_path = f.name

        try:
            # We target Photoshop by bundle id or fall back to application name
            ascript = f'''
            try
                tell application id "{self.app_id}" to do javascript (file "{jsx_path}")
            on error errMsg number errNum
                error errMsg number errNum
            end try
            '''
            proc = subprocess.run(
                ["/usr/bin/osascript", "-e", ascript],  # nosec B603
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )

            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()

            if proc.returncode != 0:
                # Fallback to application "Adobe Photoshop 2026" if bundle id resolution fails
                ascript_fallback = f'''
                try
                    tell application "Adobe Photoshop 2026" to do javascript (file "{jsx_path}")
                on error errMsg number errNum
                    error errMsg number errNum
                end try
                '''
                proc2 = subprocess.run(
                    ["/usr/bin/osascript", "-e", ascript_fallback],  # nosec B603
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds,
                    check=False,
                )
                if proc2.returncode != 0:
                    err_msg = proc2.stderr.strip() or stderr
                    raise RuntimeError(f"Photoshop execution failed: {err_msg}")
                stdout = proc2.stdout.strip()

            if not stdout:
                return None

            # Attempt JSON parse if it looks like JSON
            if (stdout.startswith("{") and stdout.endswith("}")) or (stdout.startswith("[") and stdout.endswith("]")):
                try:
                    return json.loads(stdout)
                except ValueError:
                    pass

            return stdout

        finally:
            if os.path.exists(jsx_path):
                try:
                    os.remove(jsx_path)
                except OSError:
                    pass


# Default singleton bridge instance
bridge = PhotoshopBridge()
