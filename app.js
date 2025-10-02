// MedDrone Operations Center JavaScript

// API Configuration
const API_BASE_URL = 'http://localhost:8080/api';

// Application Data - Now fetched from API
const appData = {
  demo_users: {
    "admin": {"password": "admin123", "role": "Administrator", "full_name": "System Administrator"},
    "fleet_mgr": {"password": "fleet123", "role": "Fleet Manager", "full_name": "Fleet Operations Manager"},
    "medical": {"password": "medical123", "role": "Medical Coordinator", "full_name": "Medical Supply Coordinator"},
    "demo": {"password": "demo123", "role": "Observer", "full_name": "Demo User"}
  },
  drone_fleet: [],
  medical_supplies: [],
  kpi_data: {
    "total_drones": 15,
    "active_missions": 8,
    "success_rate": 94.5,
    "avg_delivery_time": 12.3
  }
};

// Application State
let currentUser = null;
let charts = {};
let updateIntervals = {};
let isInitialized = false;

// API Functions
async function apiRequest(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });
    
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request error:', error);
    throw error;
  }
}

async function fetchKPIs() {
  try {
    const data = await apiRequest('/dashboard/kpis');
    appData.kpi_data = data;
    return data;
  } catch (error) {
    console.error('Failed to fetch KPIs:', error);
    return appData.kpi_data; // Return cached data on error
  }
}

async function fetchFleetStatus() {
  try {
    const data = await apiRequest('/fleet/status');
    appData.drone_fleet = data;
    return data;
  } catch (error) {
    console.error('Failed to fetch fleet status:', error);
    return appData.drone_fleet; // Return cached data on error
  }
}

async function fetchMedicalSupplies() {
  try {
    const data = await apiRequest('/medical/inventory');
    appData.medical_supplies = data;
    return data;
  } catch (error) {
    console.error('Failed to fetch medical supplies:', error);
    return appData.medical_supplies; // Return cached data on error
  }
}

async function fetchAlerts() {
  try {
    const data = await apiRequest('/alerts');
    return data;
  } catch (error) {
    console.error('Failed to fetch alerts:', error);
    return [];
  }
}

async function fetchActivities() {
  try {
    const data = await apiRequest('/activities');
    return data;
  } catch (error) {
    console.error('Failed to fetch activities:', error);
    return [];
  }
}

// Utility Functions
function formatTime(date) {
  return new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(date);
}

function animateValue(element, start, end, duration) {
  if (!element) return;
  
  const startTime = performance.now();
  const isFloat = end % 1 !== 0;
  
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const current = start + (end - start) * progress;
    
    if (isFloat) {
      element.textContent = current.toFixed(1);
    } else {
      element.textContent = Math.floor(current);
    }
    
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  
  requestAnimationFrame(update);
}

// Authentication Functions
function showLoginError(message) {
  const errorDiv = document.getElementById('login-error');
  if (errorDiv) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    
    setTimeout(() => {
      errorDiv.classList.add('hidden');
    }, 5000);
  }
}

function clearLoginForm() {
  const usernameField = document.getElementById('username');
  const passwordField = document.getElementById('password');
  const errorDiv = document.getElementById('login-error');
  
  if (usernameField) {
    usernameField.value = '';
  }
  if (passwordField) {
    passwordField.value = '';
  }
  if (errorDiv) {
    errorDiv.classList.add('hidden');
  }
}

async function handleLogin(event) {
  event.preventDefault();
  event.stopPropagation();
  
  const usernameField = document.getElementById('username');
  const passwordField = document.getElementById('password');
  
  if (!usernameField || !passwordField) {
    showLoginError('Login form error. Please refresh the page.');
    return false;
  }
  
  // Get values and ensure they're clean
  const username = usernameField.value.trim();
  const password = passwordField.value.trim();
  
  if (!username || !password) {
    showLoginError('Please enter both username and password.');
    return false;
  }
  
  try {
    // Try API authentication first
    const response = await apiRequest('/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    
    if (response.success) {
      currentUser = response.user;
    } else {
      throw new Error('API authentication failed');
    }
  } catch (error) {
    // Fallback to local authentication
    console.log('API auth failed, trying local auth:', error);
    const user = appData.demo_users[username];
    if (!user || user.password !== password) {
      showLoginError('Invalid username or password.');
      clearLoginForm();
      return false;
    }
    
    currentUser = {
      username: username,
      ...user
    };
  }
  
  // Clear the form
  clearLoginForm();
  
  // Hide login screen and show main app
  const loginScreen = document.getElementById('login-screen');
  const mainApp = document.getElementById('main-app');
  
  if (loginScreen && mainApp) {
    loginScreen.classList.add('hidden');
    mainApp.classList.remove('hidden');
    
    // Update user info in header
    const userNameEl = document.getElementById('user-name');
    const userRoleEl = document.getElementById('user-role');
    
    if (userNameEl) userNameEl.textContent = currentUser.full_name;
    if (userRoleEl) userRoleEl.textContent = currentUser.role;
    
    // Initialize the application after a short delay
    setTimeout(() => {
      initializeMainApp();
    }, 100);
  } else {
    showLoginError('Application error. Please refresh the page.');
  }
  
  return false;
}

function handleLogout() {
  currentUser = null;
  
  // Clear all intervals
  Object.values(updateIntervals).forEach(interval => {
    if (interval) clearInterval(interval);
  });
  updateIntervals = {};
  
  // Destroy all charts
  Object.values(charts).forEach(chart => {
    if (chart && typeof chart.destroy === 'function') {
      chart.destroy();
    }
  });
  charts = {};
  
  // Hide main app and show login screen
  const loginScreen = document.getElementById('login-screen');
  const mainApp = document.getElementById('main-app');
  
  if (loginScreen && mainApp) {
    mainApp.classList.add('hidden');
    loginScreen.classList.remove('hidden');
  }
  
  // Clear and reset login form
  clearLoginForm();
  
  // Reset to dashboard page
  showPage('dashboard');
  
  // Focus username field
  const usernameField = document.getElementById('username');
  if (usernameField) {
    setTimeout(() => {
      usernameField.focus();
    }, 100);
  }
}

// Navigation Functions
function showPage(pageId) {
  console.log('showPage called with:', pageId);
  
  // Hide all pages
  document.querySelectorAll('.page').forEach(page => {
    page.classList.remove('active');
  });
  
  // Remove active class from all nav items
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.remove('active');
  });
  
  // Show selected page
  const targetPage = document.getElementById(`${pageId}-page`);
  console.log('Target page element:', targetPage);
  if (targetPage) {
    targetPage.classList.add('active');
  } else {
    console.error('Page not found:', `${pageId}-page`);
  }
  
  // Add active class to selected nav item
  const navItem = document.querySelector(`[data-page="${pageId}"]`);
  console.log('Nav item element:', navItem);
  if (navItem) {
    navItem.classList.add('active');
  } else {
    console.error('Nav item not found for page:', pageId);
  }
  
  // Initialize page-specific content
  setTimeout(() => {
    initializePage(pageId);
  }, 50);
}

function initializePage(pageId) {
  switch (pageId) {
    case 'dashboard':
      initializeDashboard();
      break;
    case 'fleet':
      initializeFleetManagement();
      break;
    case 'analytics':
      initializeAnalytics();
      break;
    case 'inventory':
      initializeInventory();
      break;
    case 'maintenance':
      initializeMaintenance();
      break;
    case 'tracking':
      initializeTracking();
      break;
  }
}

// Dashboard Functions
async function initializeDashboard() {
  try {
    // Fetch latest data from API
    await Promise.all([
      fetchKPIs(),
      fetchFleetStatus(),
      fetchMedicalSupplies()
    ]);
    
    // Animate KPI values
    const totalDronesEl = document.getElementById('total-drones');
    const activeMissionsEl = document.getElementById('active-missions');
    const successRateEl = document.getElementById('success-rate');
    const avgDeliveryEl = document.getElementById('avg-delivery');
    
    if (totalDronesEl) animateValue(totalDronesEl, 0, appData.kpi_data.total_drones, 1000);
    if (activeMissionsEl) animateValue(activeMissionsEl, 0, appData.kpi_data.active_missions, 1200);
    if (successRateEl) {
      animateValue(successRateEl, 0, appData.kpi_data.success_rate, 1500);
      setTimeout(() => {
        successRateEl.textContent = appData.kpi_data.success_rate.toFixed(1) + '%';
      }, 1600);
    }
    if (avgDeliveryEl) {
      animateValue(avgDeliveryEl, 0, appData.kpi_data.avg_delivery_time, 1800);
      setTimeout(() => {
        avgDeliveryEl.textContent = appData.kpi_data.avg_delivery_time.toFixed(1) + ' min';
      }, 1900);
    }
    
    // Initialize fleet status chart
    setTimeout(() => {
      initializeFleetStatusChart();
    }, 200);
    
    // Start real-time updates
    if (updateIntervals.dashboard) {
      clearInterval(updateIntervals.dashboard);
    }
    
    updateIntervals.dashboard = setInterval(async () => {
      await updateDashboardData();
    }, 5000);
    
  } catch (error) {
    console.error('Failed to initialize dashboard:', error);
    // Initialize with default data if API fails
    initializeDashboardWithDefaults();
  }
}

function initializeDashboardWithDefaults() {
  // Fallback initialization with static data
  const totalDronesEl = document.getElementById('total-drones');
  const activeMissionsEl = document.getElementById('active-missions');
  const successRateEl = document.getElementById('success-rate');
  const avgDeliveryEl = document.getElementById('avg-delivery');
  
  if (totalDronesEl) animateValue(totalDronesEl, 0, 15, 1000);
  if (activeMissionsEl) animateValue(activeMissionsEl, 0, 8, 1200);
  if (successRateEl) {
    animateValue(successRateEl, 0, 94.5, 1500);
    setTimeout(() => {
      successRateEl.textContent = '94.5%';
    }, 1600);
  }
  if (avgDeliveryEl) {
    animateValue(avgDeliveryEl, 0, 12.3, 1800);
    setTimeout(() => {
      avgDeliveryEl.textContent = '12.3 min';
    }, 1900);
  }
  
  setTimeout(() => {
    initializeFleetStatusChart();
  }, 200);
}

function initializeFleetStatusChart() {
  const canvas = document.getElementById('fleet-status-chart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  const statusCounts = appData.drone_fleet.reduce((acc, drone) => {
    acc[drone.status] = (acc[drone.status] || 0) + 1;
    return acc;
  }, {});
  
  if (charts.fleetStatus) {
    charts.fleetStatus.destroy();
  }
  
  charts.fleetStatus = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: Object.keys(statusCounts),
      datasets: [{
        data: Object.values(statusCounts),
        backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
}

async function updateDashboardData() {
  try {
    // Fetch latest data from API
    const [kpiData, fleetData] = await Promise.all([
      fetchKPIs(),
      fetchFleetStatus()
    ]);
    
    // Update KPI displays
    const totalDronesEl = document.getElementById('total-drones');
    const activeMissionsEl = document.getElementById('active-missions');
    const successRateEl = document.getElementById('success-rate');
    const avgDeliveryEl = document.getElementById('avg-delivery');
    
    if (totalDronesEl) totalDronesEl.textContent = kpiData.total_drones;
    if (activeMissionsEl) activeMissionsEl.textContent = kpiData.active_missions;
    if (successRateEl) successRateEl.textContent = kpiData.success_rate.toFixed(1) + '%';
    if (avgDeliveryEl) avgDeliveryEl.textContent = kpiData.avg_delivery_time.toFixed(1) + ' min';
    
    // Update fleet status chart if it exists
    if (charts.fleetStatus) {
      charts.fleetStatus.destroy();
      setTimeout(() => {
        initializeFleetStatusChart();
      }, 100);
    }
    
  } catch (error) {
    console.error('Failed to update dashboard data:', error);
    // Fallback to local simulation
    updateDashboardDataLocal();
  }
}

function updateDashboardDataLocal() {
  const variation = 0.1;
  
  // Update success rate slightly
  const successRateEl = document.getElementById('success-rate');
  if (successRateEl) {
    const currentSuccessRate = parseFloat(successRateEl.textContent);
    const newSuccessRate = Math.max(90, Math.min(100, currentSuccessRate + (Math.random() - 0.5) * variation));
    successRateEl.textContent = newSuccessRate.toFixed(1) + '%';
  }
  
  // Update delivery time
  const avgDeliveryEl = document.getElementById('avg-delivery');
  if (avgDeliveryEl) {
    const currentDeliveryTime = parseFloat(avgDeliveryEl.textContent);
    const newDeliveryTime = Math.max(8, Math.min(20, currentDeliveryTime + (Math.random() - 0.5) * 0.5));
    avgDeliveryEl.textContent = newDeliveryTime.toFixed(1) + ' min';
  }
  
  // Simulate battery level changes
  appData.drone_fleet.forEach(drone => {
    if (drone.status === 'Active' && drone.battery > 20) {
      drone.battery = Math.max(20, drone.battery - Math.random() * 2);
    } else if (drone.status === 'Charging' && drone.battery < 100) {
      drone.battery = Math.min(100, drone.battery + Math.random() * 5);
    }
  });
}

// Fleet Management Functions
async function initializeFleetManagement() {
  const fleetGrid = document.getElementById('fleet-grid');
  if (!fleetGrid) return;
  
  try {
    // Fetch latest fleet data
    const fleetData = await fetchFleetStatus();
    
    fleetGrid.innerHTML = '';
    
    fleetData.forEach(drone => {
      const droneCard = createDroneCard(drone);
      fleetGrid.appendChild(droneCard);
    });
  } catch (error) {
    console.error('Failed to initialize fleet management:', error);
    // Fallback to cached data
    fleetGrid.innerHTML = '';
    appData.drone_fleet.forEach(drone => {
      const droneCard = createDroneCard(drone);
      fleetGrid.appendChild(droneCard);
    });
  }
}

function createDroneCard(drone) {
  const card = document.createElement('div');
  card.className = 'drone-card';
  
  const batteryClass = drone.battery > 60 ? 'high' : drone.battery > 30 ? 'medium' : 'low';
  const statusClass = drone.status.toLowerCase().replace(' ', '-');
  
  card.innerHTML = `
    <div class="drone-header">
      <div class="drone-id">${drone.id}</div>
      <div class="drone-status drone-status--${statusClass}">${drone.status}</div>
    </div>
    <div class="drone-details">
      <div class="drone-detail">
        <span class="drone-detail-label">Mission:</span>
        <span class="drone-detail-value">${drone.mission}</span>
      </div>
      <div class="drone-detail">
        <span class="drone-detail-label">Location:</span>
        <span class="drone-detail-value">${drone.location}</span>
      </div>
      <div class="drone-detail">
        <span class="drone-detail-label">Battery:</span>
        <div class="battery-indicator">
          <div class="battery-bar">
            <div class="battery-fill battery-fill--${batteryClass}" style="width: ${drone.battery}%"></div>
          </div>
          <span class="drone-detail-value">${Math.round(drone.battery)}%</span>
        </div>
      </div>
    </div>
  `;
  
  return card;
}

// Analytics Functions
function initializeAnalytics() {
  setTimeout(() => {
    initializeSuccessRateChart();
    initializeDeliveryTimeChart();
    initializeUtilizationChart();
    initializeMissionDistributionChart();
  }, 100);
}

function initializeSuccessRateChart() {
  const canvas = document.getElementById('success-rate-chart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const data = [92.5, 94.2, 91.8, 95.1, 93.7, 96.2, 94.5];
  
  if (charts.successRate) {
    charts.successRate.destroy();
  }
  
  charts.successRate = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Success Rate (%)',
        data: data,
        borderColor: '#1FB8CD',
        backgroundColor: 'rgba(31, 184, 205, 0.1)',
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: false,
          min: 85,
          max: 100
        }
      }
    }
  });
}

function initializeDeliveryTimeChart() {
  const canvas = document.getElementById('delivery-time-chart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  const labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
  const data = [13.2, 12.8, 11.9, 12.3];
  
  if (charts.deliveryTime) {
    charts.deliveryTime.destroy();
  }
  
  charts.deliveryTime = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Avg Delivery Time (min)',
        data: data,
        backgroundColor: '#FFC185'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function initializeUtilizationChart() {
  const canvas = document.getElementById('utilization-chart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  const labels = ['LLA-001', 'LLA-002', 'LLA-003', 'LLA-004', 'LLA-005'];
  const data = [87, 65, 92, 23, 78];
  
  if (charts.utilization) {
    charts.utilization.destroy();
  }
  
  charts.utilization = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Utilization (%)',
        data: data,
        borderColor: '#B4413C',
        backgroundColor: 'rgba(180, 65, 60, 0.2)'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          beginAtZero: true,
          max: 100
        }
      }
    }
  });
}

function initializeMissionDistributionChart() {
  const canvas = document.getElementById('mission-distribution-chart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  const labels = ['Medical Delivery', 'Emergency Response', 'Supply Drop', 'Surveillance', 'Maintenance'];
  const data = [35, 28, 20, 12, 5];
  
  if (charts.missionDistribution) {
    charts.missionDistribution.destroy();
  }
  
  charts.missionDistribution = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
}

// Inventory Functions
async function initializeInventory() {
  const inventoryGrid = document.getElementById('inventory-grid');
  if (!inventoryGrid) return;
  
  try {
    // Fetch latest medical supplies data
    const suppliesData = await fetchMedicalSupplies();
    
    inventoryGrid.innerHTML = '';
    
    suppliesData.forEach(supply => {
      const inventoryCard = createInventoryCard(supply);
      inventoryGrid.appendChild(inventoryCard);
    });
  } catch (error) {
    console.error('Failed to initialize inventory:', error);
    // Fallback to cached data
    inventoryGrid.innerHTML = '';
    appData.medical_supplies.forEach(supply => {
      const inventoryCard = createInventoryCard(supply);
      inventoryGrid.appendChild(inventoryCard);
    });
  }
}

function createInventoryCard(supply) {
  const card = document.createElement('div');
  card.className = 'inventory-card';
  
  // Handle both old and new data structures
  const itemName = supply.item_name || supply.item;
  const currentStock = supply.current_stock || supply.stock;
  const minThreshold = supply.min_stock_level || supply.min_threshold;
  const status = supply.quality_status || supply.status;
  
  const stockPercentage = (currentStock / (minThreshold * 2)) * 100;
  const statusClass = status.toLowerCase().replace(' ', '-');
  const fillClass = status === 'Good' ? 'good' : 'low';
  
  card.innerHTML = `
    <div class="inventory-header">
      <div class="inventory-item">${itemName}</div>
      <div class="inventory-status inventory-status--${statusClass}">${status}</div>
    </div>
    <div class="stock-info">
      <div class="stock-numbers">
        <span class="current-stock">${currentStock} ${supply.unit_of_measure || 'units'}</span>
        <span class="min-threshold">Min: ${minThreshold}</span>
      </div>
      <div class="stock-bar">
        <div class="stock-fill stock-fill--${fillClass}" style="width: ${Math.min(100, stockPercentage)}%"></div>
      </div>
    </div>
  `;
  
  return card;
}

// Maintenance Functions
function initializeMaintenance() {
  setTimeout(() => {
    initializeComponentHealthChart();
  }, 100);
}

function initializeComponentHealthChart() {
  const canvas = document.getElementById('component-health-chart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  const labels = ['Propellers', 'Battery', 'GPS', 'Camera', 'Motors', 'Sensors'];
  const data = [85, 92, 78, 88, 95, 82];
  
  if (charts.componentHealth) {
    charts.componentHealth.destroy();
  }
  
  charts.componentHealth = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Health Score (%)',
        data: data,
        backgroundColor: data.map(value => {
          if (value >= 90) return '#1FB8CD';
          if (value >= 70) return '#FFC185';
          return '#B4413C';
        })
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      }
    }
  });
}

// Tracking Functions
function initializeTracking() {
  if (updateIntervals.tracking) {
    clearInterval(updateIntervals.tracking);
  }
  
  updateIntervals.tracking = setInterval(() => {
    updateFlightProgress();
  }, 3000);
}

function updateFlightProgress() {
  const progressBars = document.querySelectorAll('.flight-item .progress-fill');
  
  progressBars.forEach(bar => {
    const currentWidth = parseInt(bar.style.width) || 0;
    if (currentWidth < 100) {
      const newWidth = Math.min(100, currentWidth + Math.random() * 5);
      bar.style.width = newWidth + '%';
      
      const progressText = bar.parentElement.nextElementSibling;
      if (progressText) {
        progressText.textContent = Math.round(newWidth) + '% Complete';
      }
      
      // Update ETA
      const etaElement = bar.closest('.flight-item').querySelector('.flight-eta');
      if (etaElement) {
        const remainingTime = Math.max(1, Math.round((100 - newWidth) * 0.2));
        etaElement.textContent = `ETA: ${remainingTime} min`;
      }
    }
  });
}

// Initialize Main Application
function initializeMainApp() {
  if (isInitialized) return;
  
  // Initialize Lucide icons
  if (typeof lucide !== 'undefined' && lucide.createIcons) {
    lucide.createIcons();
  }
  
  // Show dashboard by default
  showPage('dashboard');
  
  // Setup navigation event listeners
  const navItems = document.querySelectorAll('.nav-item');
  console.log('Found nav items:', navItems.length);
  navItems.forEach(item => {
    console.log('Setting up listener for:', item.getAttribute('data-page'));
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const pageId = item.getAttribute('data-page');
      console.log('Nav item clicked:', pageId);
      if (pageId) {
        showPage(pageId);
      }
    });
  });
  
  // Setup quick action buttons
  document.querySelectorAll('.action-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      alert('Feature would be implemented in production system');
    });
  });
  
  isInitialized = true;
}

// Main initialization function
function initializeSystem() {
  // Initialize Lucide icons
  if (typeof lucide !== 'undefined' && lucide.createIcons) {
    lucide.createIcons();
  }
  
  // Setup login form
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
  }
  
  // Setup logout button
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      handleLogout();
    });
  }
  
  // Auto-focus username field
  const usernameField = document.getElementById('username');
  if (usernameField) {
    usernameField.focus();
  }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', initializeSystem);

// Handle window resize for charts
window.addEventListener('resize', () => {
  Object.values(charts).forEach(chart => {
    if (chart && typeof chart.resize === 'function') {
      chart.resize();
    }
  });
});

// Simulate real-time data updates
setInterval(() => {
  const timeElements = document.querySelectorAll('.alert-time, .activity-time');
  
  timeElements.forEach((el, index) => {
    const minutes = (index + 1) * 2 + Math.floor(Math.random() * 3);
    if (el) {
      el.textContent = `${minutes} min ago`;
    }
  });
}, 30000);

// Export for potential external use
window.MedDroneApp = {
  showPage,
  handleLogin,
  handleLogout,
  currentUser: () => currentUser,
  appData
};