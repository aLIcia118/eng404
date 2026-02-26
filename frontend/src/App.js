import React, { useMemo, useState, useEffect } from "react";
import "./App.css";
import { useApi } from "./useAPI"; 

const { request } = useApi();

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

  // Endpoint 4: /health/db (MongoDB status)
  const [healthStatus, setHealthStatus] = useState(null);
  const [healthErr, setHealthErr] = useState(null);

  // Endpoint 5: /endpoints (API documentation)
  const [endpoints, setEndpoints] = useState(null);
  const [endpointsErr, setEndpointsErr] = useState(null);

  const [loadingHello, setLoadingHello] = useState(false);
  const [loadingStates, setLoadingStates] = useState(false);
  const [loadingCities, setLoadingCities] = useState(false);
  const [loadingHealth, setLoadingHealth] = useState(false);
  const [loadingEndpoints, setLoadingEndpoints] = useState(false);

  const [globalError, setGlobalError] = useState(null);

  // Tabs
  const [activeTab, setActiveTab] = useState("explorer");

  // State search (left panel)
  const [stateQuery, setStateQuery] = useState("");

  const citiesPath = useMemo(() => {
    const params = new URLSearchParams();
    if (stateCode.trim()) params.set("state_code", stateCode.trim());
    const n = Number(limit);
    if (Number.isFinite(n) && n > 0) {
      params.set("limit", String(n));
    }

    
    return `/cities?${params.toString()}`;
  }, [stateCode, limit]);

  const loadHello = async () => {
    setGlobalError(null);
    setLoadingHello(true);
    setHelloErr(null);
    try {
      setHello(await request("/hello"));
    } catch (e) {
      setHelloErr(e.message);
      setGlobalError("Error when fetching data.");
    } finally {
      setLoadingHello(false);
    }
  };

  const loadStates = async () => {
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
  };

  const loadCities = async () => {
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
  };

  const loadHealth = async () => {
    setGlobalError(null);
    setLoadingHealth(true);
    setHealthErr(null);
    try {
      setHealthStatus(await fetchJson("/health/db"));
    } catch (e) {
      setHealthErr(e.message);
      setGlobalError("Error while fetching health status.");
    } finally {
    setLoadingHealth(false);
    }
  };

  const loadEndpoints = async () => {
    setGlobalError(null);
    setLoadingEndpoints(true);
    setEndpointsErr(null);
    try {
      const data = await fetchJson("/endpoints");
      setEndpoints(data);
    } catch (e) {
      setEndpointsErr(e.message);
      setGlobalError("Error while fetching endpoints.");
    } finally {
    setLoadingEndpoints(false);
    }
  };

  useEffect(() => {
    loadHello();
    loadHealth();
    loadEndpoints();
  }, []);

  const refreshAll = async () => {
    setGlobalError(null);
    await Promise.all([
      loadHello(),
      loadStates(),
      loadCities(),
    ]);
  };

  
  // --- Derived data  ---

  // 1) normalize states into an array
  const statesArray = useMemo(() => {
    const raw = statesResp?.["States"];
    if (!raw) return [];
    if (Array.isArray(raw)) return raw;
    return Object.values(raw);
  }, [statesResp]);

  // 2) search/filter states
  const filteredStates = useMemo(() => {
    const q = stateQuery.trim().toLowerCase();
    if (!q) return statesArray;
    return statesArray.filter((s) => {
      const name = (s.name ?? "").toLowerCase();
      const code = (s.code ?? "").toLowerCase();
      return name.includes(q) || code.includes(q);
    });
  }, [statesArray, stateQuery]);

  // 3) selected state object (for title)
  const selectedState = useMemo(() => {
    const code = stateCode.trim().toUpperCase();
    return statesArray.find((s) => (s.code ?? "").toUpperCase() === code) ?? null;
  }, [statesArray, stateCode]);

  // 4) record count (safe fallback)
  const recordCount =
    statesResp?.["Number of Records"] ??
    statesResp?.["Number of records"] ??
    statesArray.length;

  // 5) preview slice for the grid
  const statesPreview = useMemo(() => filteredStates.slice(0, 24), [filteredStates]);

  // 6) normalize cities into an array
  const safeCities = useMemo(() => {
    if (!cities) return [];
    if (Array.isArray(cities)) return cities;
    return cities.cities ?? cities.results ?? [];
  }, [cities]);

  const citiesCount = safeCities.length;

  
  return (
    <div className="app-shell">
      {globalError && (
        <div className="error-banner">
          {globalError}
        </div>
      )}
      <div className="badge">ENG404 Frontend Demo</div>
      {/* <h1 className="app-title">ENG404 CRA Frontend</h1> */}
      <p className="app-subtitle">
        This frontend hits and displays data from 3 backend endpoints: <code>/hello</code>,{" "}
        <code>/state/read</code>, <code>/cities</code>.
      </p>
      <div style={{ marginBottom: "18px" }}>
        <button className="btn" onClick={refreshAll} style={{ backgroundColor: "#06b6d4" }}>
          🔄 Refresh All Data
        </button>
      </div>

      <Card title="System Health">
        <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
          <span style={{
            display: "inline-block",
            width: "12px",
            height: "12px",
            borderRadius: "50%",
            backgroundColor: healthStatus?.ok ? "#22c55e" : "#ef4444"
          }}></span>
          <span style={{ fontWeight: "600" }}>
            {healthStatus?.ok ? "MongoDB Connected" : "MongoDB Disconnected"}
          </span>
          <button className="btn" onClick={loadHealth} disabled={loadingHealth} style={{ marginLeft: "auto", padding: "4px 8px", fontSize: "0.85rem" }}>
            {loadingHealth ? "Checking..." : "Refresh"}
          </button>
        </div>
        {healthErr && <p className="path" style={{ color: "crimson", marginTop: "8px" }}>{healthErr}</p>}
        {healthStatus && <p className="path" style={{ marginTop: "8px" }}>{healthStatus.message}</p>}
      </Card>

      <Card title="1) GET /hello">
        <button className="btn" onClick={loadHello} disabled={loadingHello}>
  {loadingHello ? "Loading..." : "Load"} </button>
        {helloErr && <p className="path" style={{ color: "crimson" }}>{helloErr}</p>}
        {hello && <JsonBox value={hello} />}
      </Card>

      <Card title="2) GET /state/read">
          <div style={{ margin: "12px 0" }}>
            <input
              className="input"
              placeholder="Search state name or code..."
              value={stateQuery}
              onChange={(e) => setStateQuery(e.target.value)}
            />
          </div>
        <button className="btn" onClick={loadStates} disabled={loadingStates}>
        {loadingStates ? "Loading..." : "Load"}
        </button>
        {loadingStates && <p className="path">Loading...</p>}
        {statesErr && <p className="path" style={{ color: "crimson" }}>{statesErr}</p>}
        {statesResp && (
          <>
            <p>
              Records: <b>{recordCount}</b>
            </p>

            {statesArray.length === 0 ? (
              <p className="empty">No states found.</p>
            ) : (
              <div className="grid">
                {statesPreview.map((s, idx) => (
                  <div
                    className="tile"
                    style={{ cursor: "pointer" }}
                    onClick={() => {
                      setStateCode(s.code);
                      loadCities();
                    }}
                  >
                    <div className="tile-title">{s.name ?? "Unknown State"}</div>
                    <div className="tile-meta">{s.code ?? ""}</div>
                  </div>
                ))}
              </div>
            )}
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
          {loadingCities && <p className="path">Loading...</p>}
          <span className="path">
            Path: <code>{citiesPath}</code>
          </span>
        </div>

        {citiesErr && <p className="path" style={{ color: "crimson" }}>{citiesErr}</p>}

        {cities && !citiesErr && safeCities.length === 0 && (
          <p className="empty">No cities found for that query.</p>
        )}

        {safeCities.length > 0 && (
          <>
            <p>
              Results: <b>{citiesCount}</b>
            </p>
            <ul className="list">
              {safeCities.map((c, idx) => (
                <li className="city-item">
                  <div className="city-name">{c.name ?? "Unknown City"}</div>
                  <div className="city-meta">State: {c.state_code ?? stateCode.toUpperCase()}</div>
                </li>
              ))}
            </ul>
          </>
        )}

        {cities && !Array.isArray(cities) && <JsonBox value={cities} />}
      </Card>

      <Card title="API Documentation">
        <button className="btn" onClick={loadEndpoints} disabled={loadingEndpoints}>
          {loadingEndpoints ? "Loading..." : "Load Endpoints"}
        </button>
        {loadingEndpoints && <p className="path">Loading...</p>}
        {endpointsErr && <p className="path" style={{ color: "crimson" }}>{endpointsErr}</p>}
        {endpoints && (
          <div>
            <p style={{ marginBottom: "12px" }}>
              Total endpoints: <b>{endpoints["Available endpoints"]?.length || 0}</b>
            </p>
            <ul className="list" style={{ fontSize: "0.9rem" }}>
              {endpoints["Available endpoints"]?.map((ep, idx) => (
                <li key={idx} style={{ padding: "6px 0", fontFamily: "monospace", color: "var(--ocean)" }}>
                  {ep}
                </li>
              ))}
            </ul>
          </div>
        )}
      </Card>
     </div>
  );
}
