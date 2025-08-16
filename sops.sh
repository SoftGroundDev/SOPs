#!/bin/bash

# SOPs Knowledge Base Management Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_PID_FILE="$SCRIPT_DIR/.server.pid"
PORT=8000

case "$1" in
    start)
        echo "🚀 Starting SOPs Knowledge Base..."
        if [ -f "$SERVER_PID_FILE" ] && ps -p $(cat "$SERVER_PID_FILE") > /dev/null 2>&1; then
            echo "❌ Server is already running (PID: $(cat "$SERVER_PID_FILE"))"
            echo "   Use 'stop' to stop the server first"
            exit 1
        fi
        
        cd "$SCRIPT_DIR"
        python3 serve.py &
        echo $! > "$SERVER_PID_FILE"
        
        echo "✅ Server started successfully!"
        echo "📖 Web Interface: http://localhost:$PORT"
        echo "📝 Obsidian Vault: http://localhost:$PORT/vault/"
        echo "📋 Templates: http://localhost:$PORT/vault/templates/"
        echo ""
        echo "💡 To stop the server: $0 stop"
        ;;
        
    stop)
        echo "⏹️  Stopping SOPs Knowledge Base..."
        if [ -f "$SERVER_PID_FILE" ]; then
            PID=$(cat "$SERVER_PID_FILE")
            if ps -p $PID > /dev/null 2>&1; then
                kill $PID
                echo "✅ Server stopped (PID: $PID)"
            else
                echo "⚠️  Server was not running"
            fi
            rm -f "$SERVER_PID_FILE"
        else
            echo "⚠️  No PID file found. Server may not be running."
            # Try to kill any running server anyway
            pkill -f "python3 serve.py" || true
        fi
        ;;
        
    restart)
        echo "🔄 Restarting SOPs Knowledge Base..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    status)
        if [ -f "$SERVER_PID_FILE" ] && ps -p $(cat "$SERVER_PID_FILE") > /dev/null 2>&1; then
            echo "✅ Server is running (PID: $(cat "$SERVER_PID_FILE"))"
            echo "📖 Web Interface: http://localhost:$PORT"
        else
            echo "❌ Server is not running"
            [ -f "$SERVER_PID_FILE" ] && rm -f "$SERVER_PID_FILE"
        fi
        ;;
        
    open)
        if [ -f "$SERVER_PID_FILE" ] && ps -p $(cat "$SERVER_PID_FILE") > /dev/null 2>&1; then
            echo "🌐 Opening SOPs Knowledge Base..."
            open "http://localhost:$PORT" 2>/dev/null || xdg-open "http://localhost:$PORT" 2>/dev/null || echo "Please open http://localhost:$PORT in your browser"
        else
            echo "❌ Server is not running. Start it first with: $0 start"
            exit 1
        fi
        ;;
        
    logs)
        echo "📋 Server logs:"
        echo "Check terminal output or use 'status' command"
        ;;
        
    *)
        echo "📚 SOPs Knowledge Base Management"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|open}"
        echo ""
        echo "Commands:"
        echo "  start     Start the knowledge base server"
        echo "  stop      Stop the knowledge base server"
        echo "  restart   Restart the knowledge base server"
        echo "  status    Check if the server is running"
        echo "  open      Open the web interface in your browser"
        echo ""
        echo "Examples:"
        echo "  $0 start     # Start the server"
        echo "  $0 open      # Open in browser"
        echo "  $0 stop      # Stop the server"
        exit 1
        ;;
esac
