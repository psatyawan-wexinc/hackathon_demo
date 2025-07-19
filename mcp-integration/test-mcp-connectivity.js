#!/usr/bin/env node

/**
 * MCP Connectivity Test Script
 * Tests individual MCP servers for basic functionality
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

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

class MCPConnectivityTest {
    constructor() {
        this.envPath = path.join(__dirname, 'config/.env');
        this.credentials = {};
        this.testResults = {
            timestamp: new Date().toISOString(),
            tests: {}
        };
    }

    // Load environment variables
    loadEnvironment() {
        try {
            if (!fs.existsSync(this.envPath)) {
                throw new Error('.env file not found');
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

    // Test MCP server startup
    async testMCPServer(name, command, args, timeout = 10000) {
        return new Promise((resolve) => {
            log('blue', `Testing ${name}...`);
            
            const env = { ...process.env, ...this.credentials };
            const child = spawn(command, args, { 
                env,
                stdio: ['pipe', 'pipe', 'pipe']
            });

            let stdout = '';
            let stderr = '';
            let timedOut = false;

            const timer = setTimeout(() => {
                timedOut = true;
                child.kill('SIGTERM');
            }, timeout);

            child.stdout.on('data', (data) => {
                stdout += data.toString();
            });

            child.stderr.on('data', (data) => {
                stderr += data.toString();
            });

            child.on('close', (code) => {
                clearTimeout(timer);
                
                const result = {
                    name,
                    command: `${command} ${args.join(' ')}`,
                    success: !timedOut && (code === 0 || stdout.length > 0),
                    code,
                    stdout: stdout.substring(0, 500),
                    stderr: stderr.substring(0, 500),
                    timedOut
                };

                if (result.success) {
                    log('green', `✓ ${name} test passed`);
                } else {
                    log('red', `✗ ${name} test failed (code: ${code}, timeout: ${timedOut})`);
                }

                resolve(result);
            });

            child.on('error', (error) => {
                clearTimeout(timer);
                log('red', `✗ ${name} test error: ${error.message}`);
                resolve({
                    name,
                    command: `${command} ${args.join(' ')}`,
                    success: false,
                    error: error.message,
                    timedOut: false
                });
            });

            // Send a simple MCP initialization message
            try {
                const initMessage = JSON.stringify({
                    jsonrpc: "2.0",
                    id: 1,
                    method: "initialize",
                    params: {
                        protocolVersion: "2024-11-05",
                        capabilities: {
                            resources: {},
                            tools: {}
                        },
                        clientInfo: {
                            name: "connectivity-test",
                            version: "1.0.0"
                        }
                    }
                }) + '\n';
                
                child.stdin.write(initMessage);
                child.stdin.end();
            } catch (e) {
                // Some servers might not accept stdin immediately
            }
        });
    }

    // Run all connectivity tests
    async runConnectivityTests() {
        log('cyan', '🔧 Starting MCP connectivity tests...');

        if (!this.loadEnvironment()) {
            return false;
        }

        const tests = [
            {
                name: 'Playwright MCP',
                command: 'npx',
                args: ['@playwright/mcp@latest']
            },
            {
                name: 'Knowledge Graph MCP',
                command: 'npx',
                args: ['-y', 'mcp-knowledge-graph', '--memory-path', this.credentials.KNOWLEDGE_GRAPH_MEMORY_PATH || './config/credentials/knowledge_graph_memory.jsonl']
            },
            {
                name: 'Memory Bank MCP',
                command: 'npx',
                args: ['@movibe/memory-bank-mcp']
            },
            {
                name: 'Perplexity Sonar MCP',
                command: 'npx',
                args: ['-y', '@felores/perplexity-sonar-mcp']
            }
        ];

        for (const test of tests) {
            this.testResults.tests[test.name] = await this.testMCPServer(
                test.name, 
                test.command, 
                test.args
            );
        }

        this.generateReport();
        return this.allTestsPassed();
    }

    // Check if all tests passed
    allTestsPassed() {
        return Object.values(this.testResults.tests).every(test => test.success);
    }

    // Generate test report
    generateReport() {
        console.log('\n' + '='.repeat(60));
        log('cyan', 'MCP CONNECTIVITY TEST REPORT');
        console.log('='.repeat(60));

        const results = this.testResults.tests;
        const passed = Object.values(results).filter(test => test.success).length;
        const total = Object.keys(results).length;

        log('blue', `Report Time: ${this.testResults.timestamp}`);
        log('blue', `Tests Passed: ${passed}/${total}`);

        console.log('\n📊 Test Results:');
        for (const [name, result] of Object.entries(results)) {
            const icon = result.success ? '✅' : '❌';
            const color = result.success ? 'green' : 'red';
            console.log(`  ${icon} ${name}: ${colors[color]}${result.success ? 'PASS' : 'FAIL'}${colors.reset}`);
            
            if (!result.success) {
                if (result.error) {
                    console.log(`      Error: ${result.error}`);
                }
                if (result.stderr) {
                    console.log(`      Stderr: ${result.stderr.substring(0, 100)}...`);
                }
            }
        }

        if (this.allTestsPassed()) {
            console.log('\n🎉 All MCP servers are working correctly!');
        } else {
            console.log('\n⚠️  Some MCP servers have issues. Check the details above.');
        }

        // Save detailed report
        const reportPath = path.join(__dirname, 'config/connectivity-report.json');
        try {
            fs.writeFileSync(reportPath, JSON.stringify(this.testResults, null, 2));
            log('blue', `Detailed report saved to: ${reportPath}`);
        } catch (error) {
            log('red', `Failed to save report: ${error.message}`);
        }

        console.log('\n' + '='.repeat(60));
    }
}

// CLI execution
if (require.main === module) {
    const tester = new MCPConnectivityTest();
    tester.runConnectivityTests().then(success => {
        process.exit(success ? 0 : 1);
    }).catch(error => {
        log('red', `Connectivity test failed: ${error.message}`);
        process.exit(1);
    });
}

module.exports = MCPConnectivityTest;