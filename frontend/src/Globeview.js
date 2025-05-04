import React, { useRef, useState, useEffect } from "react";
import Globe from "react-globe.gl";
import * as topojson from "topojson-client";
import "./GlobeView.css";

export default function GlobeView() {
  const globeEl = useRef();
  const [countries, setCountries] = useState([]);
  const [hoverD, setHoverD] = useState();
  const [activeCountry, setActiveCountry] = useState();
  const [globeReady, setGlobeReady] = useState(false);

  // Fetch world data
  useEffect(() => {
    fetch("https://unpkg.com/world-atlas@2/countries-110m.json")
      .then(res => res.json())
      .then(topology => {
        const geojson = topojson.feature(
          topology,
          topology.objects.countries
        ).features;
        setCountries(geojson);
      });
  }, []);

  // Auto-rotate when ready
  useEffect(() => {
    if (globeReady && globeEl.current) {
      const controls = globeEl.current.controls();
      controls.autoRotate = true;
      controls.autoRotateSpeed = 0.3;
    }
  }, [globeReady]);

  return (
    <div style={{ position: "relative", width: "100vw", height: "100vh" }}>
      <Globe
        ref={globeEl}
        onGlobeReady={() => setGlobeReady(true)}
        
        // Light background globe texture
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-day.jpg"
        bumpImageUrl="//unpkg.com/three-globe/example/img/earth-topology.png"
        
        // Lighting & atmosphere
        showAtmosphere={true}
        atmosphereColor="lightskyblue"
        atmosphereAltitude={0.25}
        ambientLightColor="#ffffff"
        ambientLightIntensity={0.6}
        pointLightColor="#ffffff"
        pointLightIntensity={1}
        
        // Country polygons
        polygonsData={countries}
        polygonCapColor={() => "rgba(200, 200, 200, 0.3)"} // Consistent light fill
        polygonSideColor={() => "rgba(0, 0, 0, 0.15)"}     // Consistent side color
        
        // BORDER HIGHLIGHT - only change border color on hover
        polygonStrokeColor={feat => 
          feat === hoverD 
            ? "rgba(251, 255, 0, 0.9)" // Bright white for hover
            : "rgba(150, 150, 150, 0.3)" // Subtle gray normally
        }
        
        // Slightly increase border width overall for visibility
        polygonStrokeWidth={0.5}
        
        // Very slight raise on hover for subtle 3D effect
        polygonAltitude={feat => feat === hoverD ? 0.02 : 0.01}
        
        // Country label on hover
        polygonLabel={feat => `
          <div style="text-align:center;font-family:sans-serif;background:rgba(0,0,0,0.5);padding:3px 8px;border-radius:3px;">
            <b>${feat?.properties?.name || ''}</b><br/>
            <span style="font-size:0.8em">Click for news</span>
          </div>
        `}
        
        // Interaction
        onPolygonHover={setHoverD}
        onPolygonClick={setActiveCountry}
        
        // Transitions
        polygonsTransitionDuration={300}
        
        width={window.innerWidth}
        height={window.innerHeight}
      />

      {activeCountry && (
        <div className="info-box">
          <h3>{activeCountry.properties.name}</h3>
          <p>News & analytics will appear here.</p>
        </div>
      )}
    </div>
  );
}




// // src/GlobeView.js - for displaying a globe with country polygons
// import React, { useRef, useState, useEffect } from "react";
// import Globe from "react-globe.gl";
// import * as topojson from "topojson-client";
// import "./GlobeView.css";

// export default function GlobeView() {
//   const globeEl = useRef();
//   const [countries, setCountries] = useState([]);
//   const [hoverD, setHoverD] = useState();
//   const [activeCountry, setActiveCountry] = useState();
//   const [globeReady, setGlobeReady] = useState(false); // Track when globe is ready

//   // Fetch world data
//   useEffect(() => {
//     fetch("https://unpkg.com/world-atlas@2/countries-110m.json")
//       .then(res => res.json())
//       .then(topology => {
//         const geojson = topojson.feature(
//           topology,
//           topology.objects.countries
//         ).features;
//         setCountries(geojson);
//       });
//   }, []);

//   // Only set auto-rotate AFTER the globe is ready
//   useEffect(() => {
//     if (globeReady && globeEl.current) {
//       const controls = globeEl.current.controls();
//       controls.autoRotate = true;
//       controls.autoRotateSpeed = 0.3;
//     }
//   }, [globeReady]); // Depend on globeReady, not just on mount

//   return (
//     <div style={{ position: "relative", width: "100vw", height: "100vh" }}>
//       <Globe
//         ref={globeEl}
//         onGlobeReady={() => setGlobeReady(true)} // Set flag when globe is ready
//         globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
//         bumpImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
//         showAtmosphere
//         atmosphereColor="lightblue"
//         atmosphereAltitude={0.25}
        
//         // Country polygons
//         polygonsData={countries}
//         polygonCapColor={feat => feat === hoverD ? "orange" : "#00ADB5"}
//         polygonSideColor={() => "rgba(0,0,0,0.15)"}
//         polygonStrokeColor={() => "#111"}
//         polygonLabel={feat => `<b>${feat?.properties?.name || ''}</b><br/>Click to see news...`}
//         polygonAltitude={feat => feat === hoverD ? 0.06 : 0.01}
//         onPolygonHover={setHoverD}
//         onPolygonClick={setActiveCountry}

//         // Lighting
//         ambientLightColor="#cccccc"
//         ambientLightIntensity={0.6}
//         pointLightColor="white"
//         pointLightIntensity={1.0}
//         pointLightAltitude={2}

//         // glow
//         globeGlowColor="#123"
//         globeGlowCoefficient={0.4}
//         globeGlowPower={2}
//         globeGlowRadiusScale={1.1}

//         width={window.innerWidth}
//         height={window.innerHeight}
//       />

//       {activeCountry && (
//         <div className="info-box">
//           <h3>{activeCountry.properties.name}</h3>
//           <p>News & analytics will appear here.</p>
//         </div>
//       )}
//     </div>
//   );
// }
