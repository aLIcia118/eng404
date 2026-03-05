import React, { useMemo, useState, useEffect, useCallback } from "react";
import "./App.css";
import "leaflet/dist/leaflet.css";
import GeoMap from "./GeoMap";
import HelloHealthCard from "./HelloHealthCard"; 

const API_URL =
  process.env.REACT_APP_API_URL ||
  process.env.REACT_APP_API_BASE_URL ||
  "http://localhost:8000";

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

  const [loadingHello, setLoadingHello] = useState(false);
  const [loadingStates, setLoadingStates] = useState(false);
  const [loadingCities, setLoadingCities] = useState(false);

  const [globalError, setGlobalError] = useState(null);

  const citiesPath = useMemo(() => {
    const params = new URLSearchParams();
    if (stateCode.trim()) params.set("state_code", stateCode.trim());
    const n = Number(limit);
    if (Number.isFinite(n) && n > 0) {
      params.set("limit", String(n));
    }
    return `/cities?${params.toString()}`;
  }, [stateCode, limit]);

  const loadHello = useCallback(async () => {
    setGlobalError(null);
    setLoadingHello(true);
    setHelloErr(null);
    try {
      setHello(await fetchJson("/hello"));
    } catch (e) {
      setHelloErr(e.message);
      setGlobalError("Error when fetching data.");
    } finally {
    setLoadingHello(false);
    }
  }, []);

  const loadStates = useCallback(async () => {
    setGlobalError(null);
    setLoadingStates(true);
    setStatesErr(null);
    try {
      setStatesResp(await fetchJson("/state/read"));
    } catch (e) {
      setStatesErr(e.message);
      setGlobalError("Error while fetching data.");
    } finally {
    setLoadingStates(false);
    }
  }, []);

  const loadCities = useCallback(async () => {
    setGlobalError(null);
    setLoadingCities(true);
    setCitiesErr(null);
    try {
      setCities(await fetchJson(citiesPath));
    } catch (e) {
      setCitiesErr(e.message);
      setGlobalError("Error while fetching data.");
    } finally {
    setLoadingCities(false);
    }
  }, [citiesPath]);

  useEffect(() => {
    loadHello();
  }, [loadHello]);

  useEffect(() => {
  loadCities();
  }, [loadCities]);

  const citiesArray = Array.isArray(cities)
  ? cities
  : cities?.cities;

  return (
    <div className="app-shell">
      {globalError && (
        <div className="error-banner">
          {globalError}
        </div>
      )}
      <div className="badge">ENG404 Frontend Demo</div>
      <h1 className="app-title">ENG404 CRA Frontend</h1>
      <p className="app-subtitle">
        This frontend hits and displays data from 3 backend endpoints: <code>/hello</code>,{" "}
        <code>/state/read</code>, <code>/cities</code>.
      </p>

      <GeoMap apiBase={API_URL} />
        
      <HelloHealthCard apiBase={API_URL} />

      <Card title="2) GET /state/read">
        <button className="btn" onClick={loadStates} disabled={loadingStates}>
        {loadingStates ? "Loading..." : "Load"}
        </button>
        {loadingStates && <p className="path">Loading...</p>}
        {statesErr && <p className="path" style={{ color: "crimson" }}>{statesErr}</p>}
        {statesResp && (
          <>
            <p>
              Records: <b>{statesResp["Number of Records"]}</b>
            </p>

            {/* Preview only to keep output short */}
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
            <input
              className="input"
              type="number"
              min="1"
              max="200"
              value={limit}
              onChange={(e) => setLimit(e.target.value)}
            />
          </label>
          <button className="btn" onClick={loadCities} disabled={loadingCities}>
            {loadingCities ? "Loading..." : "Load"}
          </button>

          <button
            className="btn"
            onClick={() => {
              setCities(null);
              setCitiesErr(null);
            }}
          >
            Clear
          </button>
            
          {loadingCities && <p className="path">Loading...</p>}
          <span className="path">
            Path: <code>{citiesPath}</code>
          </span>
        </div>

        {citiesErr && <p className="path" style={{ color: "crimson" }}>{citiesErr}</p>}

        {Array.isArray(citiesArray) && (
          <>
            <p>
              Results: <b>{citiesArray.length}</b>
            </p>
            <ul className="list">
              {citiesArray.map((c, idx) => (
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
