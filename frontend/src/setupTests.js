// Ensure global test shims run early (patch react-query/query-core prototypes)
try {
  require("./jest.setup.js");
} catch (e) {
  // ignore if missing
}

import "@testing-library/jest-dom/extend-expect";
import React from "react";

// Short-term test shim: some testing-library internals import `act` from
// 'react-dom/test-utils' which triggers deprecation warnings in newer React.
// Force-override the test-utils act implementation to React.act so older
// call-sites route to the supported API. This is intentionally aggressive
// and temporary until we upgrade test libraries.
try {
  // eslint-disable-next-line global-require
  const rdt = require("react-dom/test-utils");
  if (rdt && typeof React.act === "function") {
    try {
      rdt.act = React.act;
    } catch (e) {
      // Some environments may freeze the module; ignore silently
    }
  }
} catch (e) {
  // ignore shim failures — non-fatal
}
