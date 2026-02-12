import "./App.css";

function App() {
  return (
    <div className="container">
      <header className="header">
        <h1>API Documentation</h1>
        <p className="subtitle">Base URL: /</p>
      </header>

      <section className="group">
        <h2>Cities</h2>

        <div className="endpoint post">
          <span className="method">POST</span>
          <span className="path">/cities</span>
          <p>Create a new city</p>
        </div>

        <div className="endpoint get">
          <span className="method">GET</span>
          <span className="path">/cities</span>
          <p>Return all cities</p>
        </div>

        <div className="endpoint get">
          <span className="method">GET</span>
          <span className="path">/cities/{'{city_id}'}</span>
          <p>Get city by id</p>
        </div>

        <div className="endpoint patch">
          <span className="method">PATCH</span>
          <span className="path">/cities/{'{city_id}'}</span>
          <p>Update a city</p>
        </div>

        <div className="endpoint delete">
          <span className="method">DELETE</span>
          <span className="path">/cities/{'{city_id}'}</span>
          <p>Delete a city</p>
        </div>
      </section>

      <section className="group">
        <h2>State</h2>

        <div className="endpoint get">
          <span className="method">GET</span>
          <span className="path">/state/read</span>
          <p>Return all states and count</p>
        </div>

        <div className="endpoint get">
          <span className="method">GET</span>
          <span className="path">/state/{'{state_code}'}</span>
          <p>Get state by code</p>
        </div>
      </section>
    </div>
  );
}

export default App;
