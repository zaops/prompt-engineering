# Basic Text Analysis Examples

## Sentiment Analysis

### Simple Sentiment Classification

**Prompt:**
```
Classify the sentiment of this review as positive, negative, or neutral:

"The product arrived quickly and works as expected. Nothing extraordinary, but it does the job."
```

**Expected Output:**
```
Neutral
```

### Detailed Sentiment Analysis

**Prompt:**
```
Analyze the sentiment of this customer feedback and provide:
1. Overall sentiment (positive/negative/neutral)
2. Confidence level (1-10)
3. Key emotional indicators
4. Specific aspects mentioned (product, service, delivery, etc.)

Feedback: "I love the design and quality of this laptop, but the customer service was terrible when I had an issue. The delivery was also delayed by a week."
```

**Expected Output:**
```
1. Overall sentiment: Mixed (leaning negative)
2. Confidence level: 8/10
3. Key emotional indicators: "love" (positive), "terrible" (negative)
4. Specific aspects:
   - Product (positive): design, quality
   - Customer service (negative): terrible experience
   - Delivery (negative): delayed
```

## Text Summarization

### Basic Summary

**Prompt:**
```
Summarize this article in 3 bullet points:

[Article text here]
```

### Executive Summary

**Prompt:**
```
Create an executive summary of this report for C-level executives. Focus on:
- Key findings
- Business impact
- Recommended actions

Limit to 150 words and use professional language.

[Report content here]
```

## Content Classification

### Topic Classification

**Prompt:**
```
Classify this article into one of these categories:
- Technology
- Business
- Health
- Sports
- Entertainment
- Politics

Article: "The new smartphone features advanced AI capabilities that can predict user behavior and optimize battery life accordingly."
```

**Expected Output:**
```
Technology
```

### Content Moderation

**Prompt:**
```
Review this user comment for potential issues:
1. Inappropriate language (yes/no)
2. Spam content (yes/no)
3. Harmful content (yes/no)
4. Overall recommendation (approve/review/reject)

Comment: "This product is amazing! Check out my review blog at [suspicious-link].com for more details!!!"
```

**Expected Output:**
```
1. Inappropriate language: No
2. Spam content: Yes (promotional link)
3. Harmful content: No
4. Overall recommendation: Review (potential spam)
```
