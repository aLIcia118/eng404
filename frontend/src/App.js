import React, { useMemo, useState } from "react";
import "./App.css";

async function fetchJson(path) {
  const res = await fetch(path);
  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = text;
  }
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText}: ${typeof data === "string" ? data : JSON.stringify(data)}`);
  }
  return data;
}

function Card({ title, children }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16, marginBottom: 16 }}>
      <h2 style={{ marginTop: 0 }}>{title}</h2>
      {children}
    </div>
  );
}

function JsonBox({ value }) {
  return (
    <pre style={{ background: "#f7f7f7", padding: 12, borderRadius: 10, overflowX: "auto" }}>
      {JSON.stringify(value, null, 2)}
    </pre>
  );
}

export default function App() {
  // Endpoint 1: /hello
  const [hello, setHello] = useState(null);
  const [helloErr, setHelloErr] = useState(null);

  // Endpoint 2: /state/read
  const [statesResp, setStatesResp] = useState(null);
  const [statesErr, setStatesErr] = useState(null);

  // Endpoint 3: /cities (with query params)
  const [stateCode, setStateCode] = useState("NY");
  const [limit, setLimit] = useState("10");
  const [cities, setCities] = useState(null);
  const [citiesErr, setCitiesErr] = useState(null);

  const citiesPath = useMemo(() => {
    const params = new URLSearchParams();
    if (stateCode.trim()) params.set("state_code", stateCode.trim());
    if (limit.trim()) params.set("limit", limit.trim());
    return `/cities?${params.toString()}`;
  }, [stateCode, limit]);

  const loadHello = async () => {
    setHelloErr(null);
    try {
      setHello(await fetchJson("/hello"));
    } catch (e) {
      setHelloErr(e.message);
    }
  };

  const loadStates = async () => {
    setStatesErr(null);
    try {
      setStatesResp(await fetchJson("/state/read"));
    } catch (e) {
      setStatesErr(e.message);
    }
  };

  const loadCities = async () => {
    setCitiesErr(null);
    try {
      setCities(await fetchJson(citiesPath));
    } catch (e) {
      setCitiesErr(e.message);
    }
  };

  return (
    <div style={{ maxWidth: 900, margin: "24px auto", padding: "0 16px", fontFamily: "system-ui" }}>
      <h1 style={{ marginTop: 0 }}>ENG404 CRA Frontend</h1>
      <p style={{ color: "#666" }}>
        This frontend hits and displays data from 3 backend endpoints: <code>/hello</code>,{" "}
        <code>/state/read</code>, <code>/cities</code>.
      </p>

      <Card title="1) GET /hello">
        <button onClick={loadHello}>Load</button>
        {helloErr && <p style={{ color: "crimson" }}>{helloErr}</p>}
        {hello && <JsonBox value={hello} />}
      </Card>

      <Card title="2) GET /state/read">
        <button onClick={loadStates}>Load</button>
        {statesErr && <p style={{ color: "crimson" }}>{statesErr}</p>}
        {statesResp && (
          <>
            <p>
              Records: <b>{statesResp["Number of Records"]}</b>
            </p>

            {/* 只预览一部分，避免太长 */}
            <JsonBox
              value={{
                "States Preview":
                  Array.isArray(statesResp["States"])
                    ? statesResp["States"].slice(0, 10)
                    : Object.fromEntries(Object.entries(statesResp["States"] || {}).slice(0, 10)),
              }}
            />
          </>
        )}
      </Card>

      <Card title="3) GET /cities (query params)">
        <div style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
          <label>
            state_code:&nbsp;
            <input value={stateCode} onChange={(e) => setStateCode(e.target.value)} placeholder="NY" />
          </label>
          <label>
            limit:&nbsp;
            <input value={limit} onChange={(e) => setLimit(e.target.value)} placeholder="10" />
          </label>
          <button onClick={loadCities}>Load</button>
          <span style={{ color: "#666" }}>
            Path: <code>{citiesPath}</code>
          </span>
        </div>

        {citiesErr && <p style={{ color: "crimson" }}>{citiesErr}</p>}

        {Array.isArray(cities) && (
          <>
            <p>
              Results: <b>{cities.length}</b>
            </p>
            <ul>
              {cities.map((c, idx) => (
                <li key={idx}>
                  <b>{c.name}</b> ({c.state_code})
                </li>
              ))}
            </ul>
          </>
        )}

        {cities && !Array.isArray(cities) && <JsonBox value={cities} />}
      </Card>
    </div>
  );
}
