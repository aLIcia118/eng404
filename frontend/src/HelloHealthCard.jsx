import React, { useState } from "react";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

async function fetchJson(path) {
  const url = `${API_URL}${path}`;
  const res = await fetch(url);
  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = text;
  }
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}: ${text}`);
  return data;
}

function HealthBadge({ ok }) {
  return (
    <span
      style={{
        padding: "6px 10px",
        borderRadius: 999,
        fontWeight: 600,
        fontSize: 12,
        border: "1px solid rgba(0,0,0,0.08)",
        background: ok ? "rgba(34,197,94,0.12)" : "rgba(239,68,68,0.12)",
      }}
    >
      {ok ? "✅ Online" : "❌ Offline"}
    </span>
  );
}

export default function HelloHealthCard() {
  const [loading, setLoading] = useState(false);
  const [ok, setOk] = useState(null); // null = not checked yet
  const [latencyMs, setLatencyMs] = useState(null);
  const [checkedAt, setCheckedAt] = useState(null);
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  async function runCheck() {
    setLoading(true);
    setError("");
    setData(null);
    setLatencyMs(null);

    const t0 = performance.now();
    try {
      const resp = await fetchJson("/hello");
      const t1 = performance.now();
      setLatencyMs(Math.round(t1 - t0));
      setCheckedAt(new Date());
      setOk(true);
      setData(resp);
    } catch (e) {
      const t1 = performance.now();
      setLatencyMs(Math.round(t1 - t0));
      setCheckedAt(new Date());
      setOk(false);
      setError(String(e.message || e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12 }}>
        <h2 className="card-title" style={{ margin: 0 }}>Server Health</h2>
        {ok !== null && <HealthBadge ok={ok} />}
      </div>

      <div style={{ marginTop: 10, display: "grid", gap: 8 }}>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
          <button className="btn" onClick={runCheck} disabled={loading}>
            {loading ? "Checking..." : "Run health check"}
          </button>

          <span style={{ opacity: 0.75, fontSize: 13 }}>
            API: <code>{API_URL}</code>
          </span>

          {latencyMs !== null && (
            <span style={{ opacity: 0.75, fontSize: 13 }}>
              Latency: <b>{latencyMs}ms</b>
            </span>
          )}

          {checkedAt && (
            <span style={{ opacity: 0.75, fontSize: 13 }}>
              Last checked: <b>{checkedAt.toLocaleString()}</b>
            </span>
          )}
        </div>

        {error && (
          <div
            style={{
              padding: 12,
              borderRadius: 10,
              background: "rgba(239,68,68,0.10)",
              border: "1px solid rgba(239,68,68,0.25)",
              color: "rgba(127,29,29,1)",
              fontSize: 14,
            }}
          >
            <b>Couldn’t reach the backend.</b>
            <div style={{ marginTop: 6 }}>
              {error}
            </div>
            <div style={{ marginTop: 8, opacity: 0.85 }}>
              Tip: make sure your backend is running and CORS allows <code>localhost:3000</code>.
            </div>
          </div>
        )}

        {data && (
          <details style={{ marginTop: 4 }}>
            <summary style={{ cursor: "pointer", opacity: 0.8 }}>Show raw JSON</summary>
            <pre className="json" style={{ marginTop: 8 }}>
              {JSON.stringify(data, null, 2)}
            </pre>
          </details>
        )}
      </div>
    </div>
  );
}