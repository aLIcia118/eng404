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
    <div className="card">
      <h2 className="card-title">{title}</h2>
      {children}
    </div>
  );
}

function JsonBox({ value }) {
  return (
    <pre className="json">
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
    <div className="app-shell">
      <div className="badge">ENG404 Frontend Preview</div>
      <h1 className="app-title">ENG404 CRA Frontend</h1>
      <p className="app-subtitle">
        This frontend hits and displays data from 3 backend endpoints: <code>/hello</code>,{" "}
        <code>/state/read</code>, <code>/cities</code>.
      </p>

      <Card title="1) GET /hello">
        <button className="btn" onClick={loadHello}>Load</button>
        {helloErr && <p className="path" style={{ color: "crimson" }}>{helloErr}</p>}
        {hello && <JsonBox value={hello} />}
      </Card>

      <Card title="2) GET /state/read">
        <button className="btn" onClick={loadStates}>Load</button>
        {statesErr && <p className="path" style={{ color: "crimson" }}>{statesErr}</p>}
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
        <div className="controls">
          <label>
            state_code:&nbsp;
            <input className="input" value={stateCode} onChange={(e) => setStateCode(e.target.value)} placeholder="NY" />
          </label>
          <label>
            limit:&nbsp;
            <input className="input" value={limit} onChange={(e) => setLimit(e.target.value)} placeholder="10" />
          </label>
          <button className="btn" onClick={loadCities}>Load</button>
          <span className="path">
            Path: <code>{citiesPath}</code>
          </span>
        </div>

        {citiesErr && <p className="path" style={{ color: "crimson" }}>{citiesErr}</p>}

        {Array.isArray(cities) && (
          <>
            <p>
              Results: <b>{cities.length}</b>
            </p>
            <ul className="list">
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
