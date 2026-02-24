import React, { useMemo, useState, useEffect } from "react";
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

  // --- Derived data for UI ---
  const statesArray = useMemo(() => {
    const raw = statesResp?.["States"];
    if (!raw) return [];
    if (Array.isArray(raw)) return raw;
    return Object.values(raw);
  }, [statesResp]);

  const statesPreview = useMemo(() => statesArray.slice(0, 24), [statesArray]);

  // const citiesArray = useMemo(() => {
  //   if (!cities) return [];
  //   if (Array.isArray(cities)) return cities;
  //   return cities.cities ?? cities.results ?? [];
  // }, [cities]);

  const recordCount =
    statesResp?.["Number of Records"] ??
    statesResp?.["Number of records"] ??
    statesArray.length;

  const loadHello = async () => {
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

  useEffect(() => {
    loadHello();
  }, []);

  const safeCities = Array.isArray(cities)
  ? cities
  : (cities?.cities ?? cities?.results ?? []);

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

      <Card title="1) GET /hello">
        <button className="btn" onClick={loadHello} disabled={loadingHello}>
  {loadingHello ? "Loading..." : "Load"} </button>
        {helloErr && <p className="path" style={{ color: "crimson" }}>{helloErr}</p>}
        {hello && <JsonBox value={hello} />}
      </Card>

      <Card title="2) GET /state/read">
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
              <p className="empty">No states found. (Have you loaded data into MongoDB?)</p>
            ) : (
              <div className="grid">
                {statesPreview.map((s, idx) => (
                  <div className="tile" key={s.code ?? s._id ?? idx}>
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
                <li className="listItem" key={c._id ?? `${c.name}-${idx}`}>
                  <span className="cityName">{c.name ?? "Unknown City"}</span>
                  <span className="pill">{c.state_code ?? stateCode.toUpperCase()}</span>
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
