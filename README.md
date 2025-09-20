# VTOL Medical Drone System

A comprehensive medical drone operations center with real-time fleet management, medical inventory tracking, and mission analytics.

## Features

- 🚁 **Fleet Management**: Real-time drone status, battery monitoring, and mission tracking
- ⚕️ **Medical Inventory**: Comprehensive supply management with temperature monitoring
- 📊 **Analytics Dashboard**: Mission success rates, delivery trends, and performance metrics
- 🚨 **Alert System**: Real-time notifications for critical events
- 🔐 **Authentication**: Role-based access control with multiple user types
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## Quick Start

### Option 1: Easy Setup (Recommended)
```bash
# Install dependencies and start server
python start_server.py --install
python start_server.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python server.py
```

The application will be available at: **http://localhost:8080**

## Demo Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| fleet_mgr | fleet123 | Fleet Manager |
| medical | medical123 | Medical Coordinator |
| demo | demo123 | Observer |

## System Architecture

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Flask (Python)
- **Data Management**: Pandas, NumPy
- **Real-time Updates**: WebSocket simulation with polling
- **Authentication**: Role-based access control

## API Endpoints

The system provides RESTful API endpoints:

- `GET /api/dashboard/kpis` - Key performance indicators
- `GET /api/fleet/status` - Fleet status overview
- `GET /api/medical/inventory` - Medical supplies inventory
- `GET /api/alerts` - Active alerts
- `POST /api/login` - User authentication
- `POST /api/fleet/{id}/deploy` - Deploy drone
- `POST /api/fleet/{id}/recall` - Recall drone

## Features by Role

### Administrator
- Full system access
- User management
- System configuration
- Emergency protocols

### Fleet Manager
- Fleet control and monitoring
- Mission planning
- Performance analytics
- Maintenance scheduling

### Medical Coordinator
- Inventory management
- Delivery tracking
- Supply chain analytics
- Temperature monitoring

### Observer
- Read-only access
- Status monitoring
- Mission tracking

## Development

### Project Structure
```
vtol-medical-drone-system/
├── server.py              # Flask server
├── start_server.py        # Startup script
├── index.html             # Main web interface
├── app.js                 # Frontend JavaScript
├── style.css              # Styling
├── drone_data.py          # Drone management
├── medical_supplies.py    # Medical inventory
├── utils/
│   ├── alerts.py          # Alert system
│   └── authentication.py  # User management
└── requirements.txt       # Dependencies
```

### Adding New Features

1. **Backend**: Add new endpoints in `server.py`
2. **Frontend**: Update `app.js` with new API calls
3. **Data**: Extend data managers in respective Python files
4. **UI**: Add new components in `index.html` and `style.css`

## Troubleshooting

### Server Won't Start
- Check if port 8080 is available
- Verify all dependencies are installed
- Check Python version (3.7+ required)

### API Errors
- Ensure server is running on http://localhost:8080
- Check browser console for error messages
- Verify CORS is enabled (handled automatically)

### Data Not Loading
- Check network tab in browser dev tools
- Verify API endpoints are responding
- Check server logs for errors

## License

This project is for demonstration purposes. Please ensure compliance with local regulations when implementing drone operations.

## Support

For issues or questions, please check the browser console and server logs for error messages.
