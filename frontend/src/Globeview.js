import React, { useRef, useState, useEffect } from "react";
import Globe from "react-globe.gl";

// Example country data with lat/lng (expand as needed)
const COUNTRIES = [
  { name: "United States", lat: 38, lng: -97, code: "US" },
  { name: "India", lat: 21, lng: 78, code: "IN" },
  { name: "Japan", lat: 36, lng: 138, code: "JP" },
  { name: "France", lat: 46, lng: 2, code: "FR" },
  { name: "Brazil", lat: -14, lng: -51, code: "BR" },
  { name: "Australia", lat: -25, lng: 133, code: "AU" }
];

export default function GlobeView() {
  const globeEl = useRef();
  const [activeCountry, setActiveCountry] = useState(null);

  // When a country is selected from dropdown or clicked, rotate globe
  useEffect(() => {
    if (activeCountry && globeEl.current) {
      globeEl.current.pointOfView(
        { lat: activeCountry.lat, lng: activeCountry.lng, altitude: 1.5 },
        1000
      );
    }
  }, [activeCountry]);

  return (
    <div style={{ position: "relative", height: "80vh", width: "100%" }}>
      <div style={{ position: "absolute", top: 20, left: 20, zIndex: 2 }}>
        <select
          onChange={e => {
            const country = COUNTRIES.find(c => c.code === e.target.value);
            setActiveCountry(country);
          }}
          defaultValue=""
        >
          <option value="" disabled>
            Select a country...
          </option>
          {COUNTRIES.map(c => (
            <option key={c.code} value={c.code}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <Globe
        ref={globeEl}
        width={window.innerWidth}
        height={window.innerHeight * 0.8}
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-dark.jpg"
        pointsData={COUNTRIES}
        pointLat="lat"
        pointLng="lng"
        pointColor={() => "orange"}
        pointAltitude={() => 0.05}
        pointRadius={() => 0.5}
        onPointClick={setActiveCountry}
        pointLabel={d => d.name}
      />

      {activeCountry && (
        <div
          style={{
            position: "absolute",
            right: 30,
            top: 30,
            background: "white",
            padding: 20,
            borderRadius: 8,
            boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
            zIndex: 3,
            minWidth: 220
          }}
        >
          <h3>{activeCountry.name}</h3>
          <div style={{ color: "#888" }}>
            {/* Placeholder for news, sentiment, fun facts, etc. */}
            <p>Top news and analytics will appear here!</p>
          </div>
        </div>
      )}
    </div>
  );
}
