/**
 * CyberArk Health Dashboard - Frontend JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Charger les données initiales
    fetchDashboardData();
    
    // Configurer l'actualisation automatique toutes les 30 secondes
    setInterval(fetchDashboardData, 30000);
    
    // Configurer les gestionnaires d'événements
    setupEventHandlers();
});

/**
 * Récupère les données du tableau de bord depuis l'API
 */
function fetchDashboardData() {
    fetch('/api/dashboard')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur réseau lors de la récupération des données');
            }
            return response.json();
        })
        .then(data => {
            updateDashboard(data);
            updateLastUpdateTime(data.last_update);
        })
        .catch(error => {
            console.error('Erreur:', error);
            showErrorMessage('Impossible de récupérer les données. Veuillez rafraîchir la page ou réessayer plus tard.');
        });
}

/**
 * Met à jour les éléments du tableau de bord avec les nouvelles données
 */
function updateDashboard(data) {
    // Mettre à jour les compteurs généraux
    updateComponentStatus(data.component_status);
    updateVaultStatus(data.vault_status);
    updateAccountsStatus(data.accounts_status);
    updateSystemHealth(data.system_health);
    
    // Mettre à jour les tableaux d'activités
    updateRecentActivities(data.recent_activities);
    updateFailedLogins(data.failed_logins);
}

/**
 * Met à jour la section des états des composants
 */
function updateComponentStatus(componentStatus) {
    const componentContainer = document.getElementById('component-status');
    if (!componentContainer || !componentStatus || !componentStatus.Items) return;
    
    const componentList = document.getElementById('component-list');
    if (componentList) {
        componentList.innerHTML = '';
        
        // Calculer les statistiques globales
        let totalComponents = 0;
        let connectedComponents = 0;
        
        componentStatus.Items.forEach(item => {
            totalComponents += item['Total Amount'] || 0;
            connectedComponents += item['Connected'] || 0;
            
            // Créer un élément de liste pour chaque type de composant
            const listItem = document.createElement('li');
            listItem.className = 'component-item';
            
            // Déterminer le statut
            let statusClass = 'status-ok';
            if (item['Disconnected'] > 0) {
                statusClass = item['Disconnected'] === item['Total Amount'] ? 'status-error' : 'status-warning';
            }
            
            listItem.innerHTML = `
                <div class="component-name">
                    <span class="status-indicator ${statusClass}"></span>
                    ${item['Component Type']}
                </div>
                <div class="component-status">
                    ${item['Connected']} / ${item['Total Amount']} connectés
                </div>
            `;
            
            componentList.appendChild(listItem);
        });
        
        // Mettre à jour le pourcentage global
        const percentConnected = totalComponents > 0 ? Math.round((connectedComponents / totalComponents) * 100) : 0;
        const globalStatusElement = document.getElementById('component-global-status');
        if (globalStatusElement) {
            globalStatusElement.textContent = `${percentConnected}%`;
            
            // Mettre à jour la couleur en fonction du pourcentage
            if (percentConnected >= 90) {
                globalStatusElement.className = 'metric-value text-success';
            } else if (percentConnected >= 70) {
                globalStatusElement.className = 'metric-value text-warning';
            } else {
                globalStatusElement.className = 'metric-value text-danger';
            }
        }
    }
}

/**
 * Met à jour la section des informations sur le coffre-fort
 */
function updateVaultStatus(vaultStatus) {
    if (!vaultStatus || !vaultStatus.Safes) return;
    
    const safesElement = document.getElementById('total-safes');
    const accountsElement = document.getElementById('total-accounts');
    const versionElement = document.getElementById('vault-version');
    const licenseElement = document.getElementById('license-status');
    
    if (safesElement) safesElement.textContent = vaultStatus.Safes.Total_Safes || 0;
    if (accountsElement) accountsElement.textContent = vaultStatus.Safes.Total_Accounts || 0;
    if (versionElement) versionElement.textContent = vaultStatus.Safes.Version || 'Inconnu';
    
    if (licenseElement) {
        licenseElement.textContent = vaultStatus.Safes.License_Status || 'Inconnu';
        
        // Appliquer une classe de couleur en fonction du statut de la licence
        licenseElement.className = 'metric-value';
        if (vaultStatus.Safes.License_Status === 'Valid') {
            licenseElement.classList.add('text-success');
        } else if (vaultStatus.Safes.License_Status === 'Expiring Soon') {
            licenseElement.classList.add('text-warning');
        } else if (vaultStatus.Safes.License_Status === 'Expired') {
            licenseElement.classList.add('text-danger');
        }
    }
}

/**
 * Met à jour la section des informations sur les comptes
 */
function updateAccountsStatus(accountsStatus) {
    if (!accountsStatus || !accountsStatus.value) return;
    
    const managedElement = document.getElementById('managed-accounts');
    const nonManagedElement = document.getElementById('non-managed-accounts');
    const pendingElement = document.getElementById('pending-accounts');
    const failedElement = document.getElementById('failed-accounts');
    
    if (managedElement) managedElement.textContent = accountsStatus.value.Managed_Accounts || 0;
    if (nonManagedElement) nonManagedElement.textContent = accountsStatus.value.Non_Managed_Accounts || 0;
    if (pendingElement) pendingElement.textContent = accountsStatus.value.Pending_Accounts || 0;
    if (failedElement) failedElement.textContent = accountsStatus.value.Failed_Accounts || 0;
    
    // Mettre à jour le graphique si présent
    updateAccountsChart(accountsStatus.value);
}

/**
 * Met à jour la section des informations sur la santé du système
 */
function updateSystemHealth(systemHealth) {
    if (!systemHealth) return;
    
    const cpuElement = document.getElementById('cpu-usage');
    const memoryElement = document.getElementById('memory-usage');
    const diskElement = document.getElementById('disk-usage');
    const networkElement = document.getElementById('network-latency');
    
    if (cpuElement) {
        cpuElement.textContent = `${systemHealth.CPU_Usage || 0}%`;
        updateStatusColor(cpuElement, systemHealth.CPU_Usage, 80, 90);
    }
    
    if (memoryElement) {
        memoryElement.textContent = `${systemHealth.Memory_Usage || 0}%`;
        updateStatusColor(memoryElement, systemHealth.Memory_Usage, 80, 90);
    }
    
    if (diskElement) {
        diskElement.textContent = `${systemHealth.Disk_Usage || 0}%`;
        updateStatusColor(diskElement, systemHealth.Disk_Usage, 80, 90);
    }
    
    if (networkElement) {
        networkElement.textContent = `${systemHealth.Network_Latency || 0} ms`;
        updateStatusColor(networkElement, systemHealth.Network_Latency, 50, 100, true);
    }
}

/**
 * Met à jour la couleur d'un élément en fonction de seuils
 */
function updateStatusColor(element, value, warningThreshold, dangerThreshold, isInverted = false) {
    element.className = 'metric-value';
    
    if (isInverted) {
        // Pour les valeurs où plus bas est mieux (comme la latence)
        if (value < warningThreshold) {
            element.classList.add('text-success');
        } else if (value < dangerThreshold) {
            element.classList.add('text-warning');
        } else {
            element.classList.add('text-danger');
        }
    } else {
        // Pour les valeurs où plus bas est mieux (comme l'utilisation CPU)
        if (value < warningThreshold) {
            element.classList.add('text-success');
        } else if (value < dangerThreshold) {
            element.classList.add('text-warning');
        } else {
            element.classList.add('text-danger');
        }
    }
}

/**
 * Met à jour la section des activités récentes
 */
function updateRecentActivities(activities) {
    const activitiesTable = document.getElementById('recent-activities-table');
    if (!activitiesTable || !activities) return;
    
    const tbody = activitiesTable.querySelector('tbody');
    if (tbody) {
        tbody.innerHTML = '';
        
        activities.slice(0, 5).forEach(activity => {
            const row = document.createElement('tr');
            
            const timestamp = new Date(activity.Timestamp);
            const formattedDate = timestamp.toLocaleString();
            
            // Déterminer la classe de gravité
            let severityClass = '';
            if (activity.Severity === 'Critical') {
                severityClass = 'text-danger';
            } else if (activity.Severity === 'Warning') {
                severityClass = 'text-warning';
            }
            
            row.innerHTML = `
                <td>${formattedDate}</td>
                <td>${activity.Username}</td>
                <td>${activity.EventType}</td>
                <td class="${severityClass}">${activity.Description}</td>
            `;
            
            tbody.appendChild(row);
        });
    }
}

/**
 * Met à jour la section des tentatives de connexion échouées
 */
function updateFailedLogins(logins) {
    const loginsTable = document.getElementById('failed-logins-table');
    if (!loginsTable || !logins) return;
    
    const tbody = loginsTable.querySelector('tbody');
    if (tbody) {
        tbody.innerHTML = '';
        
        logins.slice(0, 5).forEach(login => {
            const row = document.createElement('tr');
            
            const timestamp = new Date(login.Timestamp);
            const formattedDate = timestamp.toLocaleString();
            
            row.innerHTML = `
                <td>${formattedDate}</td>
                <td>${login.Username}</td>
                <td>${login.Source_IP}</td>
                <td>${login.Reason}</td>
            `;
            
            tbody.appendChild(row);
        });
    }
}

/**
 * Met à jour l'heure de la dernière mise à jour
 */
function updateLastUpdateTime(timestamp) {
    const lastUpdateElement = document.getElementById('last-update-time');
    if (lastUpdateElement && timestamp) {
        const updateTime = new Date(timestamp);
        lastUpdateElement.textContent = updateTime.toLocaleString();
    }
}

/**
 * Met à jour le graphique des comptes si Chart.js est disponible
 */
function updateAccountsChart(accountsData) {
    // Vérifier si Chart.js est disponible
    if (typeof Chart === 'undefined' || !accountsData) return;
    
    const chartCanvas = document.getElementById('accounts-chart');
    if (!chartCanvas) return;
    
    // Détruire le graphique existant s'il y en a un
    if (window.accountsChart) {
        window.accountsChart.destroy();
    }
    
    // Créer un nouveau graphique
    window.accountsChart = new Chart(chartCanvas, {
        type: 'doughnut',
        data: {
            labels: ['Gérés', 'Non gérés', 'En attente', 'Échoués'],
            datasets: [{
                data: [
                    accountsData.Managed_Accounts || 0,
                    accountsData.Non_Managed_Accounts || 0,
                    accountsData.Pending_Accounts || 0,
                    accountsData.Failed_Accounts || 0
                ],
                backgroundColor: [
                    '#10b981',  // Vert - Géré
                    '#f59e0b',  // Orange - Non géré
                    '#3b82f6',  // Bleu - En attente
                    '#ef4444'   // Rouge - Échoué
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

/**
 * Configure les gestionnaires d'événements pour l'interface utilisateur
 */
function setupEventHandlers() {
    // Gestionnaire pour le bouton d'actualisation manuelle
    const refreshButton = document.getElementById('refresh-data');
    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            fetchDashboardData();
        });
    }
    
    // Gestionnaire pour le basculement entre les onglets
    const tabButtons = document.querySelectorAll('[data-tab]');
    if (tabButtons.length > 0) {
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                const tabId = this.getAttribute('data-tab');
                showTab(tabId);
            });
        });
    }
}

/**
 * Affiche un onglet et masque les autres
 */
function showTab(tabId) {
    // Masquer tous les contenus d'onglets
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.style.display = 'none';
    });
    
    // Afficher le contenu de l'onglet sélectionné
    const selectedTab = document.getElementById(tabId);
    if (selectedTab) {
        selectedTab.style.display = 'block';
    }
    
    // Mettre à jour les classes active des boutons d'onglets
    const tabButtons = document.querySelectorAll('[data-tab]');
    tabButtons.forEach(button => {
        if (button.getAttribute('data-tab') === tabId) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
}

/**
 * Affiche un message d'erreur
 */
function showErrorMessage(message) {
    const errorContainer = document.getElementById('error-container');
    if (errorContainer) {
        errorContainer.textContent = message;
        errorContainer.style.display = 'block';
        
        // Masquer le message après 5 secondes
        setTimeout(() => {
            errorContainer.style.display = 'none';
        }, 5000);
    }
}