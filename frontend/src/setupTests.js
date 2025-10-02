// Ensure global test shims run early (patch react-query/query-core prototypes)
try {
	require('./jest.setup.js')
} catch (e) {
	// ignore if missing
}

import '@testing-library/jest-dom/extend-expect'
 
