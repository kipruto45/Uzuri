// Ensure global test shims run early (patch react-query/query-core prototypes)
try {
	require('./jest.setup.js')
} catch (e) {
	// ignore if missing
}

import '@testing-library/jest-dom/extend-expect'

// Shim: some tests / libraries import act from 'react-dom/test-utils' which
// now warns in React 18+. Re-export React.act onto the deprecated location so
// existing tests and third-party libs don't emit noisy deprecation warnings.
// This is safe in the test environment and keeps CI logs clean until we
// update all imports to use React.act directly.
try {
	// eslint-disable-next-line global-require
	const React = require('react')
	// eslint-disable-next-line global-require
	const testUtils = require('react-dom/test-utils')
	// Always point the deprecated export to React.act when available so older
	// imports don't emit deprecation warnings during test runs.
	if (testUtils && typeof React.act === 'function') {
		try {
			testUtils.act = React.act
		} catch (e) {
			// ignore if readonly or unexpected
		}
	}
} catch (e) {
	// best-effort shim; ignore if modules unavailable in some environments
}
