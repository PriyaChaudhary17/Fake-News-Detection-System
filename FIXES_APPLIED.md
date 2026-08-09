# Fixes Applied

## 1. History page blank
The backend `/history` endpoint returns:
`{ "logs": [...] }`
but `History.jsx` was doing `setHistory(response.data)`, which stored an object instead of an array. The next render called `.slice()` on that object and React crashed, producing a blank page.

Fixed by reading `response.data.logs` and adding loading/error handling.

## 2. Admin page blank after refresh
`get_all_users()` returned MongoDB documents containing `_id: ObjectId(...)`. Flask cannot JSON-serialize MongoDB `ObjectId`, so `/api/admin/users` could return HTTP 500.

Fixed by excluding `_id` and `password` from the admin user response.

Admin frontend was also made defensive so an API error cannot turn `users` or `logs` into `undefined` and crash the page.

## 3. Missing Report route
`Analyze.jsx` navigated to `/report`, but `App.jsx` had no `/report` route even though `Report.jsx` existed.

Added the missing route.

## 4. Safer result normalization
`resultShape.js` now safely handles missing arrays and provides a verification method label for the report.

## How to run
Backend:
`python -m backend.app`

Frontend:
`cd frontend/vite-project`
`npm install`
`npm run dev`

Make sure MongoDB is running on:
`mongodb://localhost:27017/`

Then open:
`http://localhost:5173`
