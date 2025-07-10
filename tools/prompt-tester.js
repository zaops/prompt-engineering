#!/usr/bin/env node

/**
 * Prompt Testing Framework
 * 
 * A simple framework for testing prompts across different scenarios
 * and measuring consistency and quality.
 */

const fs = require('fs');
const path = require('path');

class PromptTester {
    constructor() {
        this.testResults = [];
        this.config = {
            iterations: 3,
            timeout: 30000,
            outputDir: './test-results'
        };
    }

    /**
     * Load test configuration from file
     */
    loadConfig(configPath) {
        try {
            const configData = fs.readFileSync(configPath, 'utf8');
            const config = JSON.parse(configData);
            this.config = { ...this.config, ...config };
            console.log('✅ Configuration loaded successfully');
        } catch (error) {
            console.error('❌ Error loading configuration:', error.message);
            process.exit(1);
        }
    }

    /**
     * Load test cases from file
     */
    loadTestCases(testCasesPath) {
        try {
            const testData = fs.readFileSync(testCasesPath, 'utf8');
            this.testCases = JSON.parse(testData);
            console.log(`✅ Loaded ${this.testCases.length} test cases`);
            return this.testCases;
        } catch (error) {
            console.error('❌ Error loading test cases:', error.message);
            process.exit(1);
        }
    }

    /**
     * Validate prompt structure
     */
    validatePrompt(prompt) {
        const issues = [];
        
        // Check for basic structure
        if (!prompt || prompt.trim().length === 0) {
            issues.push('Prompt is empty');
        }
        
        if (prompt.length < 10) {
            issues.push('Prompt is too short');
        }
        
        if (prompt.length > 2000) {
            issues.push('Prompt is very long (>2000 chars)');
        }
        
        // Check for clear instructions
        const instructionWords = ['write', 'create', 'analyze', 'explain', 'describe', 'generate'];
        const hasInstruction = instructionWords.some(word => 
            prompt.toLowerCase().includes(word)
        );
        
        if (!hasInstruction) {
            issues.push('No clear instruction verb found');
        }
        
        return {
            isValid: issues.length === 0,
            issues: issues,
            score: Math.max(0, 100 - (issues.length * 20))
        };
    }

    /**
     * Analyze prompt complexity
     */
    analyzeComplexity(prompt) {
        const words = prompt.split(/\s+/).length;
        const sentences = prompt.split(/[.!?]+/).length - 1;
        const avgWordsPerSentence = sentences > 0 ? words / sentences : words;
        
        let complexity = 'Simple';
        if (words > 100 || avgWordsPerSentence > 20) {
            complexity = 'Complex';
        } else if (words > 50 || avgWordsPerSentence > 15) {
            complexity = 'Medium';
        }
        
        return {
            wordCount: words,
            sentenceCount: sentences,
            avgWordsPerSentence: Math.round(avgWordsPerSentence * 10) / 10,
            complexity: complexity
        };
    }

    /**
     * Run a single test case
     */
    async runTestCase(testCase) {
        console.log(`\n🧪 Running test: ${testCase.name}`);
        
        const validation = this.validatePrompt(testCase.prompt);
        const complexity = this.analyzeComplexity(testCase.prompt);
        
        const result = {
            name: testCase.name,
            prompt: testCase.prompt,
            validation: validation,
            complexity: complexity,
            expectedOutput: testCase.expectedOutput || null,
            criteria: testCase.criteria || [],
            timestamp: new Date().toISOString(),
            status: validation.isValid ? 'PASS' : 'FAIL'
        };
        
        // Check against criteria if provided
        if (testCase.criteria && testCase.criteria.length > 0) {
            result.criteriaResults = this.checkCriteria(testCase.prompt, testCase.criteria);
        }
        
        this.testResults.push(result);
        
        console.log(`   Status: ${result.status}`);
        console.log(`   Validation Score: ${validation.score}/100`);
        console.log(`   Complexity: ${complexity.complexity}`);
        
        if (validation.issues.length > 0) {
            console.log(`   Issues: ${validation.issues.join(', ')}`);
        }
        
        return result;
    }

    /**
     * Check prompt against specific criteria
     */
    checkCriteria(prompt, criteria) {
        const results = [];
        
        criteria.forEach(criterion => {
            let passed = false;
            let details = '';
            
            switch (criterion.type) {
                case 'contains':
                    passed = prompt.toLowerCase().includes(criterion.value.toLowerCase());
                    details = `Checking if prompt contains: "${criterion.value}"`;
                    break;
                    
                case 'length':
                    const wordCount = prompt.split(/\s+/).length;
                    passed = wordCount >= criterion.min && wordCount <= criterion.max;
                    details = `Word count: ${wordCount} (expected: ${criterion.min}-${criterion.max})`;
                    break;
                    
                case 'format':
                    if (criterion.value === 'question') {
                        passed = prompt.includes('?');
                        details = 'Checking if prompt contains questions';
                    } else if (criterion.value === 'numbered_list') {
                        passed = /\d+\./g.test(prompt);
                        details = 'Checking if prompt contains numbered lists';
                    }
                    break;
                    
                default:
                    details = `Unknown criterion type: ${criterion.type}`;
            }
            
            results.push({
                criterion: criterion.name || criterion.type,
                passed: passed,
                details: details
            });
        });
        
        return results;
    }

    /**
     * Generate test report
     */
    generateReport() {
        const totalTests = this.testResults.length;
        const passedTests = this.testResults.filter(r => r.status === 'PASS').length;
        const failedTests = totalTests - passedTests;
        
        const report = {
            summary: {
                total: totalTests,
                passed: passedTests,
                failed: failedTests,
                passRate: totalTests > 0 ? Math.round((passedTests / totalTests) * 100) : 0
            },
            results: this.testResults,
            generatedAt: new Date().toISOString()
        };
        
        return report;
    }

    /**
     * Save report to file
     */
    saveReport(report, filename) {
        try {
            // Ensure output directory exists
            if (!fs.existsSync(this.config.outputDir)) {
                fs.mkdirSync(this.config.outputDir, { recursive: true });
            }
            
            const filePath = path.join(this.config.outputDir, filename);
            fs.writeFileSync(filePath, JSON.stringify(report, null, 2));
            console.log(`\n📊 Report saved to: ${filePath}`);
        } catch (error) {
            console.error('❌ Error saving report:', error.message);
        }
    }

    /**
     * Print summary to console
     */
    printSummary(report) {
        console.log('\n' + '='.repeat(50));
        console.log('📊 TEST SUMMARY');
        console.log('='.repeat(50));
        console.log(`Total Tests: ${report.summary.total}`);
        console.log(`Passed: ${report.summary.passed} ✅`);
        console.log(`Failed: ${report.summary.failed} ❌`);
        console.log(`Pass Rate: ${report.summary.passRate}%`);
        console.log('='.repeat(50));
        
        if (report.summary.failed > 0) {
            console.log('\n❌ Failed Tests:');
            report.results
                .filter(r => r.status === 'FAIL')
                .forEach(result => {
                    console.log(`  - ${result.name}: ${result.validation.issues.join(', ')}`);
                });
        }
    }

    /**
     * Run all tests
     */
    async runAllTests(testCasesPath) {
        console.log('🚀 Starting prompt testing...');
        
        const testCases = this.loadTestCases(testCasesPath);
        
        for (const testCase of testCases) {
            await this.runTestCase(testCase);
        }
        
        const report = this.generateReport();
        this.printSummary(report);
        
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        this.saveReport(report, `test-report-${timestamp}.json`);
        
        return report;
    }
}

// CLI Interface
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log('Usage: node prompt-tester.js <test-cases.json> [config.json]');
        console.log('\nExample test-cases.json format:');
        console.log(JSON.stringify([
            {
                name: "Basic Analysis Prompt",
                prompt: "Analyze the following data and provide insights: [data]",
                criteria: [
                    { type: "contains", value: "analyze" },
                    { type: "length", min: 5, max: 50 }
                ]
            }
        ], null, 2));
        process.exit(1);
    }
    
    const tester = new PromptTester();
    
    // Load config if provided
    if (args[1]) {
        tester.loadConfig(args[1]);
    }
    
    // Run tests
    tester.runAllTests(args[0])
        .then(report => {
            process.exit(report.summary.failed > 0 ? 1 : 0);
        })
        .catch(error => {
            console.error('❌ Testing failed:', error.message);
            process.exit(1);
        });
}

module.exports = PromptTester;
