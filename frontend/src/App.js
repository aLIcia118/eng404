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

function Card({ title, subtitle, meta, children }) {
  return (
    <div className="card">
      <div className="card-header">
        <div>
          {subtitle && <p className="card-eyebrow">{subtitle}</p>}
          <h2 className="card-title">{title}</h2>
        </div>
        {meta && <span className="card-meta">{meta}</span>}
      </div>
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
  const [lastTouched, setLastTouched] = useState({ hello: null, states: null, cities: null });

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
  const [cityQuery, setCityQuery] = useState("");
  const [sortDir, setSortDir] = useState("asc");
  const [visibleCount, setVisibleCount] = useState(10);

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

  const formatTimestamp = useCallback((date) => {
    if (!date) return "Not fetched yet";
    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  }, []);

  const loadHello = useCallback(async () => {
    setGlobalError(null);
    setLoadingHello(true);
    setHelloErr(null);
    try {
      setHello(await fetchJson("/hello"));
      setLastTouched((prev) => ({ ...prev, hello: new Date() }));
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
      setLastTouched((prev) => ({ ...prev, states: new Date() }));
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
      setVisibleCount(10);
      setLastTouched((prev) => ({ ...prev, cities: new Date() }));
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

  const filteredCities = useMemo(() => {
    if (!Array.isArray(citiesArray)) return [];
    const q = cityQuery.trim().toLowerCase();
    return citiesArray.filter((c) =>
      q ? String(c.name || "").toLowerCase().includes(q) : true
    );
  }, [citiesArray, cityQuery]);

  const sortedCities = useMemo(() => {
    const arr = [...filteredCities];
    arr.sort((a, b) => {
      const aName = String(a.name || "");
      const bName = String(b.name || "");
      return sortDir === "desc"
        ? bName.localeCompare(aName)
        : aName.localeCompare(bName);
    });
    return arr;
  }, [filteredCities, sortDir]);

  const visibleCities = useMemo(
    () => sortedCities.slice(0, visibleCount),
    [sortedCities, visibleCount]
  );

  return (
    <div className="app-shell">
      {globalError && (
        <div className="error-banner">
          {globalError}
        </div>
      )}

      <header className="hero">
        <div>
          <div className="hero-badge">ENG404 Frontend Demo</div>
          <h1 className="hero-title">API observability at a glance</h1>
          <p className="hero-copy">
            Explore three backend endpoints, map city data, and validate health without leaving this page. Every
            interaction explains what it fetches and when it last ran.
          </p>
          <div className="hero-actions">
            <span className="pill">Base URL: {API_URL}</span>
            <span className="pill pill-quiet">3 endpoints wired</span>
            <span className="pill pill-quiet">Leaflet map preview</span>
          </div>
        </div>
        <div className="hero-card">
          <p className="muted">How to read this page</p>
          <ul className="hero-list">
            <li><b>Map</b> auto-loads top NY cities and clusters markers.</li>
            <li><b>Health</b> measures latency and shows raw JSON when needed.</li>
            <li><b>States & cities</b> cards reveal payloads with concise previews.</li>
          </ul>
        </div>
      </header>

      <div className="meta-bar">
        <span className="meta-chip">
          <span className="chip-label">/hello</span>
          <span>{formatTimestamp(lastTouched.hello)}</span>
        </span>
        <span className="meta-chip">
          <span className="chip-label">/state/read</span>
          <span>{formatTimestamp(lastTouched.states)}</span>
        </span>
        <span className="meta-chip">
          <span className="chip-label">/cities</span>
          <span>{formatTimestamp(lastTouched.cities)}</span>
        </span>
      </div>

      <div className="layout-grid">
        <GeoMap apiBase={API_URL} />
        <HelloHealthCard apiBase={API_URL} />
      </div>

      <Card
        title="2) GET /state/read"
        subtitle="Full state catalog"
        meta={formatTimestamp(lastTouched.states)}
      >
        <div className="card-toolbar">
          <div className="endpoint-chip">GET /state/read</div>
          <button className="btn" onClick={loadStates} disabled={loadingStates}>
            {loadingStates ? "Loading..." : "Refresh"}
          </button>
        </div>

        {statesErr && <p className="path error-text">{statesErr}</p>}

        {loadingStates && <p className="path">Contacting backend...</p>}

        {statesResp && (
          <>
            <p className="meta">Records available: <b>{statesResp["Number of Records"]}</b></p>

            <div className="card-subsection">
              <p className="muted">Preview (first 10 to keep things tidy)</p>
              <JsonBox
                value={{
                  "States Preview":
                    Array.isArray(statesResp["States"])
                      ? statesResp["States"].slice(0, 10)
                      : Object.fromEntries(Object.entries(statesResp["States"] || {}).slice(0, 10)),
                }}
              />
            </div>
          </>
        )}
      </Card>

      <Card
        title="3) GET /cities (query params)"
        subtitle="Filter cities by state and limit"
        meta={formatTimestamp(lastTouched.cities)}
      >
        <div className="controls">
          <label className="control">
            <span className="label">state_code</span>
            <input className="input" value={stateCode} onChange={(e) => setStateCode(e.target.value)} placeholder="NY" />
          </label>
          <label className="control">
            <span className="label">limit</span>
            <input
              className="input"
              type="number"
              min="1"
              max="200"
              value={limit}
              onChange={(e) => setLimit(e.target.value)}
            />
          </label>
          <label className="control">
            <span className="label">search</span>
            <input
              className="input"
              value={cityQuery}
              onChange={(e) => {
                setCityQuery(e.target.value);
                setVisibleCount(10);
              }}
              placeholder="e.g. York"
            />
          </label>

          <label className="control">
            <span className="label">sort</span>
            <select
              className="input"
              value={sortDir}
              onChange={(e) => setSortDir(e.target.value)}
            >
              <option value="asc">A → Z</option>
              <option value="desc">Z → A</option>
            </select>
          </label>

          <div className="control-group">
            <button className="btn" onClick={loadCities} disabled={loadingCities}>
              {loadingCities ? "Loading..." : "Run query"}
            </button>
            <button
              className="btn btn-ghost"
              onClick={() => {
                setCities(null);
                setCitiesErr(null);
                setCityQuery("");
                setSortDir("asc");
                setVisibleCount(10);
              }}
            >
              Clear
            </button>
          </div>
        </div>

        <div className="path-row">
          <span className="endpoint-chip muted">Path: {citiesPath}</span>
          <span className="muted">Auto-loads on mount with NY & limit 10.</span>
        </div>

        {citiesErr && <p className="path error-text">{citiesErr}</p>}

        {loadingCities && <p className="path">Crunching results...</p>}

        {Array.isArray(citiesArray) && (
          <>
            <p className="meta">
              Results: <b>{filteredCities.length}</b> (showing {visibleCities.length})
            </p>

            <ul className="list">
              {visibleCities.map((c, idx) => (
                <li key={idx} className="city-item">
                  <div className="city-name">{c.name}</div>
                  <div className="city-meta">{c.state_code}</div>
                </li>
              ))}
            </ul>

            {visibleCities.length < filteredCities.length && (
              <button
                className="btn"
                onClick={() => setVisibleCount((n) => n + 10)}
              >
                Load more
              </button>
            )}
          </>
        )}

        {cities && !Array.isArray(cities) && <JsonBox value={cities} />}
      </Card>
    </div>
  );
}
