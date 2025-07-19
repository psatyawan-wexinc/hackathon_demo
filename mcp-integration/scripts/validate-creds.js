#!/usr/bin/env node

/**
 * MCP Credential Validation Script
 * Validates all required credentials before launching MCP servers
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Colors for console output
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m'
};

function log(level, message) {
    const timestamp = new Date().toISOString();
    const color = colors[level] || colors.reset;
    console.log(`${color}[${level.toUpperCase()}] ${timestamp}: ${message}${colors.reset}`);
}

class CredentialValidator {
    constructor() {
        this.envPath = path.join(__dirname, '../config/.env');
        this.credentials = {};
        this.errors = [];
        this.warnings = [];
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

            log('green', `Loaded ${Object.keys(this.credentials).length} environment variables`);
            return true;
        } catch (error) {
            log('red', `Failed to load environment: ${error.message}`);
            return false;
        }
    }

    // Validate Perplexity API key
    async validatePerplexityKey() {
        const apiKey = this.credentials.PERPLEXITY_API_KEY;
        
        if (!apiKey) {
            this.errors.push('PERPLEXITY_API_KEY is required but not set');
            return false;
        }

        if (apiKey === 'your_perplexity_api_key_here') {
            this.errors.push('PERPLEXITY_API_KEY contains placeholder value');
            return false;
        }

        // Basic format validation
        if (apiKey.length < 10) {
            this.errors.push('PERPLEXITY_API_KEY appears to be too short');
            return false;
        }

        log('green', '✓ Perplexity API key format validation passed');

        // Optional: Test API connectivity (requires network)
        try {
            const isValid = await this.testPerplexityAPI(apiKey);
            if (isValid) {
                log('green', '✓ Perplexity API key connectivity test passed');
            } else {
                this.warnings.push('Perplexity API key connectivity test failed');
            }
        } catch (error) {
            this.warnings.push(`Perplexity API connectivity test error: ${error.message}`);
        }

        return true;
    }

    // Test Perplexity API connectivity
    testPerplexityAPI(apiKey) {
        return new Promise((resolve) => {
            const options = {
                hostname: 'api.perplexity.ai',
                port: 443,
                path: '/chat/completions',
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                },
                timeout: 5000
            };

            const req = https.request(options, (res) => {
                // Even a 401 means the API endpoint is reachable
                resolve(res.statusCode !== 500);
            });

            req.on('error', () => resolve(false));
            req.on('timeout', () => resolve(false));
            
            // Send minimal test payload
            req.write(JSON.stringify({
                model: 'llama-3.1-sonar-small-128k-online',
                messages: [{ role: 'user', content: 'test' }],
                max_tokens: 1
            }));
            req.end();
        });
    }

    // Validate file paths
    validatePaths() {
        const paths = [
            { key: 'KNOWLEDGE_GRAPH_MEMORY_PATH', required: true },
            { key: 'MEMORY_BANK_PATH', required: true }
        ];

        for (const pathConfig of paths) {
            const pathValue = this.credentials[pathConfig.key];
            
            if (!pathValue && pathConfig.required) {
                this.errors.push(`${pathConfig.key} is required but not set`);
                continue;
            }

            if (pathValue === `./config/credentials/${pathConfig.key.toLowerCase()}.jsonl` ||
                pathValue.includes('your_') || pathValue.includes('_here')) {
                this.warnings.push(`${pathConfig.key} contains placeholder value`);
                continue;
            }

            // Create directory if it doesn't exist
            try {
                const dir = path.dirname(path.resolve(pathValue));
                if (!fs.existsSync(dir)) {
                    fs.mkdirSync(dir, { recursive: true });
                    log('blue', `Created directory: ${dir}`);
                }

                // Create file if it doesn't exist
                if (!fs.existsSync(pathValue)) {
                    if (pathConfig.key === 'KNOWLEDGE_GRAPH_MEMORY_PATH') {
                        fs.writeFileSync(pathValue, '');
                    } else {
                        fs.mkdirSync(pathValue, { recursive: true });
                    }
                    log('blue', `Created path: ${pathValue}`);
                }

                log('green', `✓ ${pathConfig.key} path validated`);
            } catch (error) {
                this.errors.push(`Failed to create path for ${pathConfig.key}: ${error.message}`);
            }
        }
    }

    // Validate optional credentials
    validateOptionalCredentials() {
        const optional = ['GITHUB_TOKEN', 'CUSTOM_MCP_ENDPOINT'];
        
        for (const key of optional) {
            const value = this.credentials[key];
            if (value && (value.includes('your_') || value.includes('_here'))) {
                this.warnings.push(`${key} contains placeholder value (optional)`);
            } else if (value) {
                log('green', `✓ ${key} is configured`);
            }
        }
    }

    // Generate validation report
    generateReport() {
        const report = {
            timestamp: new Date().toISOString(),
            status: this.errors.length === 0 ? 'PASS' : 'FAIL',
            errors: this.errors,
            warnings: this.warnings,
            validatedCredentials: Object.keys(this.credentials).filter(
                key => !key.includes('KEY') || !this.credentials[key].includes('your_')
            )
        };

        const reportPath = path.join(__dirname, '../config/validation-report.json');
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
        
        log('blue', `Validation report saved to: ${reportPath}`);
        return report;
    }

    // Main validation method
    async validate() {
        log('blue', '🔍 Starting credential validation...');

        if (!this.loadEnvironment()) {
            return false;
        }

        await this.validatePerplexityKey();
        this.validatePaths();
        this.validateOptionalCredentials();

        const report = this.generateReport();

        // Print summary
        console.log('\n' + '='.repeat(50));
        log('blue', 'VALIDATION SUMMARY');
        console.log('='.repeat(50));
        
        if (this.errors.length > 0) {
            log('red', `❌ ${this.errors.length} error(s) found:`);
            this.errors.forEach(error => console.log(`  - ${error}`));
        }

        if (this.warnings.length > 0) {
            log('yellow', `⚠️  ${this.warnings.length} warning(s):`);
            this.warnings.forEach(warning => console.log(`  - ${warning}`));
        }

        if (this.errors.length === 0) {
            log('green', '✅ All required credentials validated successfully!');
            return true;
        } else {
            log('red', '❌ Credential validation failed. Please fix errors before launching MCP servers.');
            return false;
        }
    }
}

// CLI execution
if (require.main === module) {
    const validator = new CredentialValidator();
    validator.validate().then(success => {
        process.exit(success ? 0 : 1);
    }).catch(error => {
        log('red', `Validation failed: ${error.message}`);
        process.exit(1);
    });
}

module.exports = CredentialValidator;