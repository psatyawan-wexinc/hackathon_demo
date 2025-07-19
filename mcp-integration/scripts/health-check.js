#!/usr/bin/env node

/**
 * MCP Health Check Script
 * Monitors the health and connectivity of all MCP servers
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const { spawn } = require('child_process');

// Colors for console output
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m'
};

function log(level, message) {
    const timestamp = new Date().toISOString();
    const color = colors[level] || colors.reset;
    console.log(`${color}[${level.toUpperCase()}] ${timestamp}: ${message}${colors.reset}`);
}

class MCPHealthChecker {
    constructor() {
        this.envPath = path.join(__dirname, '../config/.env');
        this.credentials = {};
        this.pidFilePath = '/tmp/mcp_pids.txt';
        this.healthReport = {
            timestamp: new Date().toISOString(),
            overall: 'UNKNOWN',
            servers: {}
        };
    }

    // Load environment variables
    loadEnvironment() {
        try {
            if (!fs.existsSync(this.envPath)) {
                log('red', '.env file not found');
                return false;
            }

            const envContent = fs.readFileSync(this.envPath, 'utf8');
            const lines = envContent.split('\n');

            for (const line of lines) {
                const trimmed = line.trim();
                if (trimmed && !trimmed.startsWith('#')) {
                    const [key, ...valueParts] = trimmed.split('=');
                    if (key && valueParts.length > 0) {
                        this.credentials[key.trim()] = valueParts.join('=').trim();
                    }
                }
            }

            log('green', 'Environment variables loaded');
            return true;
        } catch (error) {
            log('red', `Failed to load environment: ${error.message}`);
            return false;
        }
    }

    // Check if process is running
    async checkProcess(pid) {
        return new Promise((resolve) => {
            const ps = spawn('ps', ['-p', pid]);
            ps.on('close', (code) => {
                resolve(code === 0);
            });
            ps.on('error', () => resolve(false));
        });
    }

    // Check HTTP endpoint
    async checkHttpEndpoint(url, timeout = 5000) {
        return new Promise((resolve) => {
            const urlObj = new URL(url);
            const options = {
                hostname: urlObj.hostname,
                port: urlObj.port || 80,
                path: urlObj.pathname,
                method: 'GET',
                timeout: timeout
            };

            const req = http.request(options, (res) => {
                resolve({
                    status: res.statusCode,
                    success: res.statusCode >= 200 && res.statusCode < 400
                });
            });

            req.on('error', () => resolve({ success: false, error: 'Connection failed' }));
            req.on('timeout', () => resolve({ success: false, error: 'Timeout' }));
            req.end();
        });
    }

    // Test Perplexity API connectivity
    async testPerplexityAPI() {
        const apiKey = this.credentials.PERPLEXITY_API_KEY;
        if (!apiKey) {
            return { success: false, error: 'API key not configured' };
        }

        return new Promise((resolve) => {
            const https = require('https');
            const postData = JSON.stringify({
                model: 'llama-3.1-sonar-small-128k-online',
                messages: [{ role: 'user', content: 'test' }],
                max_tokens: 1
            });

            const options = {
                hostname: 'api.perplexity.ai',
                port: 443,
                path: '/chat/completions',
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(postData)
                },
                timeout: 10000
            };

            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', (chunk) => data += chunk);
                res.on('end', () => {
                    resolve({
                        success: res.statusCode === 200,
                        status: res.statusCode,
                        response: data.substring(0, 200)
                    });
                });
            });

            req.on('error', (error) => {
                resolve({ success: false, error: error.message });
            });

            req.on('timeout', () => {
                resolve({ success: false, error: 'Request timeout' });
            });

            req.write(postData);
            req.end();
        });
    }

    // Check file system paths
    checkPaths() {
        const paths = [
            { name: 'Knowledge Graph Memory', path: this.credentials.KNOWLEDGE_GRAPH_MEMORY_PATH },
            { name: 'Memory Bank', path: this.credentials.MEMORY_BANK_PATH }
        ];

        const results = {};

        for (const pathConfig of paths) {
            if (!pathConfig.path) {
                results[pathConfig.name] = { success: false, error: 'Path not configured' };
                continue;
            }

            try {
                const resolvedPath = path.resolve(pathConfig.path);
                const exists = fs.existsSync(resolvedPath);
                const stats = exists ? fs.statSync(resolvedPath) : null;

                results[pathConfig.name] = {
                    success: exists,
                    path: resolvedPath,
                    exists: exists,
                    type: stats ? (stats.isDirectory() ? 'directory' : 'file') : 'missing',
                    size: stats ? stats.size : 0,
                    modified: stats ? stats.mtime.toISOString() : null
                };
            } catch (error) {
                results[pathConfig.name] = {
                    success: false,
                    error: error.message,
                    path: pathConfig.path
                };
            }
        }

        return results;
    }

    // Check running processes
    async checkRunningProcesses() {
        const results = {};

        if (!fs.existsSync(this.pidFilePath)) {
            log('yellow', 'No PID file found - servers may not be running');
            return results;
        }

        try {
            const pidContent = fs.readFileSync(this.pidFilePath, 'utf8');
            const pids = pidContent.split('\n').filter(pid => pid.trim());

            for (const pid of pids) {
                const isRunning = await this.checkProcess(pid);
                results[`Process ${pid}`] = {
                    success: isRunning,
                    pid: pid,
                    status: isRunning ? 'running' : 'stopped'
                };
            }
        } catch (error) {
            log('red', `Failed to read PID file: ${error.message}`);
        }

        return results;
    }

    // Generate comprehensive health report
    async generateHealthReport() {
        log('cyan', '🏥 Starting MCP health check...');

        if (!this.loadEnvironment()) {
            this.healthReport.overall = 'FAILED';
            return this.healthReport;
        }

        // Check running processes
        log('blue', 'Checking running processes...');
        this.healthReport.servers.processes = await this.checkRunningProcesses();

        // Check file system paths
        log('blue', 'Checking file system paths...');
        this.healthReport.servers.paths = this.checkPaths();

        // Test Perplexity API
        log('blue', 'Testing Perplexity API connectivity...');
        this.healthReport.servers.perplexity = await this.testPerplexityAPI();

        // Check HTTP endpoints (if any)
        log('blue', 'Checking HTTP endpoints...');
        // Note: Most MCP servers use stdio, but we can check if any HTTP endpoints are configured
        
        // Determine overall health
        const allChecks = [
            ...Object.values(this.healthReport.servers.processes || {}),
            ...Object.values(this.healthReport.servers.paths || {}),
            this.healthReport.servers.perplexity
        ];

        const successCount = allChecks.filter(check => check && check.success).length;
        const totalChecks = allChecks.filter(check => check).length;

        if (totalChecks === 0) {
            this.healthReport.overall = 'NO_DATA';
        } else if (successCount === totalChecks) {
            this.healthReport.overall = 'HEALTHY';
        } else if (successCount > totalChecks / 2) {
            this.healthReport.overall = 'DEGRADED';
        } else {
            this.healthReport.overall = 'UNHEALTHY';
        }

        return this.healthReport;
    }

    // Display health report
    displayHealthReport() {
        const report = this.healthReport;
        
        console.log('\n' + '='.repeat(60));
        log('cyan', 'MCP HEALTH REPORT');
        console.log('='.repeat(60));

        // Overall status
        const statusColor = {
            'HEALTHY': 'green',
            'DEGRADED': 'yellow', 
            'UNHEALTHY': 'red',
            'FAILED': 'red',
            'NO_DATA': 'yellow'
        }[report.overall] || 'blue';

        log(statusColor, `Overall Status: ${report.overall}`);
        log('blue', `Report Time: ${report.timestamp}`);

        // Process status
        if (report.servers.processes && Object.keys(report.servers.processes).length > 0) {
            console.log('\n📊 Running Processes:');
            for (const [name, status] of Object.entries(report.servers.processes)) {
                const color = status.success ? 'green' : 'red';
                const icon = status.success ? '✅' : '❌';
                console.log(`  ${icon} ${name}: ${colors[color]}${status.status}${colors.reset}`);
            }
        } else {
            console.log('\n⚠️  No running processes found');
        }

        // Path status
        if (report.servers.paths) {
            console.log('\n📁 File System Paths:');
            for (const [name, status] of Object.entries(report.servers.paths)) {
                const color = status.success ? 'green' : 'red';
                const icon = status.success ? '✅' : '❌';
                console.log(`  ${icon} ${name}: ${colors[color]}${status.success ? status.type : status.error}${colors.reset}`);
                if (status.path) {
                    console.log(`      Path: ${status.path}`);
                }
            }
        }

        // API status
        if (report.servers.perplexity) {
            console.log('\n🌐 API Connectivity:');
            const status = report.servers.perplexity;
            const color = status.success ? 'green' : 'red';
            const icon = status.success ? '✅' : '❌';
            console.log(`  ${icon} Perplexity API: ${colors[color]}${status.success ? 'Connected' : (status.error || 'Failed')}${colors.reset}`);
            if (status.status) {
                console.log(`      HTTP Status: ${status.status}`);
            }
        }

        // Recommendations
        console.log('\n💡 Recommendations:');
        if (report.overall === 'HEALTHY') {
            console.log('  🎉 All systems operational!');
        } else {
            if (!report.servers.processes || Object.keys(report.servers.processes).length === 0) {
                console.log('  🚀 Run "npm run start" to launch MCP servers');
            }
            if (report.servers.perplexity && !report.servers.perplexity.success) {
                console.log('  🔑 Check your Perplexity API key in .env file');
            }
            if (report.servers.paths) {
                for (const [name, status] of Object.entries(report.servers.paths)) {
                    if (!status.success) {
                        console.log(`  📂 Create missing path for ${name}`);
                    }
                }
            }
        }

        console.log('\n' + '='.repeat(60));
    }

    // Save health report
    saveHealthReport() {
        const reportPath = path.join(__dirname, '../config/health-report.json');
        try {
            fs.writeFileSync(reportPath, JSON.stringify(this.healthReport, null, 2));
            log('blue', `Health report saved to: ${reportPath}`);
        } catch (error) {
            log('red', `Failed to save health report: ${error.message}`);
        }
    }

    // Main health check method
    async performHealthCheck() {
        await this.generateHealthReport();
        this.displayHealthReport();
        this.saveHealthReport();
        
        return this.healthReport.overall === 'HEALTHY';
    }
}

// CLI execution
if (require.main === module) {
    const checker = new MCPHealthChecker();
    checker.performHealthCheck().then(healthy => {
        process.exit(healthy ? 0 : 1);
    }).catch(error => {
        log('red', `Health check failed: ${error.message}`);
        process.exit(1);
    });
}

module.exports = MCPHealthChecker;