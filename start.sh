#!/bin/bash
# SAP Sales Outreach Engine - Startup Script
# Usage: ./start.sh

echo "========================================="
echo "  SAP Sales Outreach Engine"
echo "========================================="
echo ""

# Get the directory where this script lives
DIR="$(cd "$(dirname "$0")" && pwd)"

# Start backend
echo "[1/2] Starting backend API server..."
cd "$DIR/backend"
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
echo "  Backend running on http://localhost:8000"
echo "  API docs at   http://localhost:8000/docs"
echo ""

# Start frontend
echo "[2/2] Starting frontend dev server..."
cd "$DIR/frontend"
npm run dev &
FRONTEND_PID=$!
echo ""

echo "========================================="
echo "  Dashboard: http://localhost:5173"
echo "  API docs:  http://localhost:8000/docs"
echo "========================================="
echo ""
echo "Press Ctrl+C to stop both servers."
echo ""

# Trap Ctrl+C to kill both processes
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID 2>/dev/null
    wait $FRONTEND_PID 2>/dev/null
    echo "Done. Goodbye!"
    exit 0
}
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
