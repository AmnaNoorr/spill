# SipsNSecrets API Reference

## New Endpoints

### Oracle Reports

#### Submit Oracle Report
**POST** `/oracles/submit`

Submit an evidence-based truth report for a market.

**Request Body:**
```json
{
  "oracle_id": "user-uuid",
  "market_id": "market-uuid",
  "verdict": "true" | "false",
  "evidence": ["https://example.com/proof1", "https://example.com/proof2"],
  "stake": 5.0
}
```

**Response:**
```json
{
  "report": {
    "id": "report-uuid",
    "oracle_id": "user-uuid",
    "market_id": "market-uuid",
    "verdict": "true",
    "evidence": [...],
    "stake": 5.0,
    "ai_summary": "Summary of evidence...",
    "status": "pending"
  },
  "consensus": {
    "consensus_reached": false,
    "outcome": null,
    "true_votes": 1,
    "false_votes": 0,
    "total_votes": 1,
    "true_percentage": 1.0,
    "false_percentage": 0.0,
    "threshold": 0.6
  }
}
```

#### Get Oracle Reports
**GET** `/oracles/reports/<market_id>`

Get all oracle reports for a market.

**Response:**
```json
{
  "reports": [
    {
      "id": "report-uuid",
      "oracle_id": "user-uuid",
      "verdict": "true",
      "evidence": [...],
      "ai_summary": "...",
      "created_at": "2024-01-01T00:00:00Z",
      "users": {
        "pseudonym": "user123"
      }
    }
  ],
  "consensus": {
    "consensus_reached": true,
    "outcome": "true",
    "true_votes": 5,
    "false_votes": 2,
    "total_votes": 7,
    "true_percentage": 0.71,
    "false_percentage": 0.29,
    "threshold": 0.6
  }
}
```

#### Resolve Market
**POST** `/oracles/resolve`

Resolve a market through oracle consensus.

**Request Body:**
```json
{
  "market_id": "market-uuid",
  "outcome": "true" | "false"  // Optional - checks consensus if not provided
}
```

**Response:**
```json
{
  "message": "Market resolved successfully",
  "outcome": "true",
  "settlement": {
    "payouts": {
      "user-uuid-1": 50.0,
      "user-uuid-2": 25.0
    },
    "winners": ["user-uuid-1", "user-uuid-2"],
    "losers": ["user-uuid-3"],
    "total_paid": 75.0
  }
}
```

### Market Management

#### Delete Market
**DELETE** `/markets/<market_id>/delete`

Delete an unresolved market (only submitter can delete).

**Request Body:**
```json
{
  "user_id": "user-uuid"
}
```

**Response:**
```json
{
  "message": "Market deleted successfully",
  "market_id": "market-uuid",
  "total_cc_returned": 150.0,
  "users_refunded": 5
}
```

**Error Responses:**
- `403`: Only submitter can delete
- `400`: Market already resolved
- `404`: Market not found

## Rate Limiting

Rate limits are applied to the following endpoints:

- **Market Submission**: 5 requests per 60 seconds
- **Trading**: 20 requests per 60 seconds

**Rate Limit Response (429):**
```json
{
  "error": "Rate limit exceeded. Maximum 20 requests per 60 seconds."
}
```

## Duplicate Detection

When submitting a market, the system automatically checks for duplicates using:
1. TF-IDF similarity (threshold: 0.7)
2. Embedding-based similarity (threshold: 0.85)

**Duplicate Detection Response:**
```json
{
  "error": "Duplicate rumor detected",
  "duplicate_check": {
    "is_duplicate": true,
    "similar_to": "market-uuid",
    "similarity": 0.85,
    "similar_text": "Similar rumor text..."
  }
}
```

## Frontend Integration

### JavaScript Examples

```javascript
// Submit oracle report
const report = await oracleAPI.submitReport({
  oracle_id: userId,
  market_id: marketId,
  verdict: 'true',
  evidence: ['https://proof.com'],
  stake: 5.0
});

// Get reports for a market
const reports = await oracleAPI.getReports(marketId);
console.log(reports.consensus);

// Resolve market
const resolution = await oracleAPI.resolveMarket(marketId);

// Delete market
await marketsAPI.deleteMarket(marketId, userId);
```

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `403`: Forbidden (authorization errors)
- `404`: Not Found
- `429`: Too Many Requests (rate limit)
- `500`: Internal Server Error

Error responses follow this format:
```json
{
  "error": "Error message description"
}
```


