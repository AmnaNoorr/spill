# New Features Implementation Summary

This document summarizes the newly implemented features that were missing from the SRS.

## ✅ Newly Implemented Features

### 1. Rumor Update and Versioning (FR-2.4)
**Location:** `backend/routes/markets.py` - `update_market()` and `get_market_versions()` endpoints

**Features:**
- Submitters can update rumors by creating linked versions
- Each version maintains a version number
- Original market becomes parent of new versions
- New versions can have updated text, category, and stake
- Duplicate detection prevents duplicate updates
- AI analysis performed on new versions

**API Endpoints:**
```
POST /markets/<market_id>/update
Body: {
  "user_id": "user_id",
  "text": "Updated rumor text",
  "category": "Category",
  "stake": 50.0 (optional)
}

GET /markets/<market_id>/versions
```

**Database Changes:**
- Added `parent_market_id` to markets table
- Added `version_number` to markets table

### 2. Oracle Reputation Tracking (FR-5.5)
**Location:** `backend/services/reputation_service.py` and `backend/routes/oracles.py`

**Features:**
- Tracks oracle accuracy over time
- Calculates reputation score (0-100) based on correct/incorrect reports
- Awards +2 reputation points for correct reports
- Penalizes -1 reputation point for incorrect reports
- Reputation-weighted consensus calculation
- Top oracles leaderboard

**API Endpoints:**
```
GET /oracles/reputation/<oracle_id>
GET /oracles/reputation/top?limit=20
```

**Database Changes:**
- Added `oracle_reputation` to users table (0-100)
- Added `oracle_reports_count` to users table
- Added `oracle_correct_count` to users table
- Added `oracle_incorrect_count` to users table
- Added `was_correct` to oracle_reports table
- Added `reputation_awarded` to oracle_reports table

**Reputation Calculation:**
- Starting reputation: 50.0
- Accuracy-based: `(correct_count / total_count) * 100`
- Bonus/Penalty: +2 for correct, -1 for incorrect
- Final reputation clamped to 0-100

### 3. Automated Evidence Fetching (FR-5.2)
**Location:** `backend/services/evidence_service.py` and `backend/routes/oracles.py`

**Features:**
- Fetches content from URLs automatically
- Extracts text content from HTML pages
- Supports JSON and text content types
- AI-powered evidence summarization
- Relevance checking against rumor text
- Batch URL processing

**API Endpoints:**
```
POST /oracles/evidence/fetch
Body: {
  "urls": ["https://example.com/proof1", ...],
  "rumor_text": "Rumor text",
  "market_id": "market_id" (optional)
}

POST /oracles/evidence/auto/<market_id>
```

**Features:**
- URL validation
- Content extraction from HTML/JSON/text
- Title extraction from HTML
- Content length limiting (5000 chars)
- AI summarization of evidence
- Error handling for failed fetches

### 4. Enhanced Oracle Consensus (FR-5.3 Enhancement)
**Location:** `backend/services/oracle_service.py` - `check_consensus()` method

**Enhancements:**
- Reputation-weighted consensus calculation
- Considers both simple majority and weighted consensus
- Higher reputation oracles have more influence
- Dual threshold checking (simple + weighted)

**Consensus Logic:**
1. Calculate simple majority (unweighted)
2. Calculate weighted consensus (reputation-weighted)
3. Check both against threshold (60%)
4. Consensus reached if either exceeds threshold

## 📋 Database Migration

**File:** `backend/database/migration_add_versioning_reputation.sql`

Run this SQL script in your Supabase SQL Editor to add the new columns:

```sql
-- Markets versioning
ALTER TABLE markets 
ADD COLUMN IF NOT EXISTS parent_market_id UUID REFERENCES markets(id),
ADD COLUMN IF NOT EXISTS version_number INTEGER DEFAULT 1;

-- Users oracle reputation
ALTER TABLE users
ADD COLUMN IF NOT EXISTS oracle_reputation DECIMAL(5, 2) DEFAULT 50.0,
ADD COLUMN IF NOT EXISTS oracle_reports_count INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS oracle_correct_count INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS oracle_incorrect_count INTEGER DEFAULT 0;

-- Oracle reports tracking
ALTER TABLE oracle_reports
ADD COLUMN IF NOT EXISTS was_correct BOOLEAN,
ADD COLUMN IF NOT EXISTS reputation_awarded DECIMAL(5, 2) DEFAULT 0.0;
```

## 🔧 Technical Details

### Reputation Service
- **Starting Reputation:** 50.0 (neutral)
- **Correct Report Bonus:** +2 points
- **Incorrect Report Penalty:** -1 point
- **Accuracy Calculation:** `(correct / total) * 100`
- **Final Reputation:** Clamped to 0-100 range

### Evidence Service
- **URL Validation:** Checks scheme and netloc
- **Content Extraction:** Removes HTML tags, extracts text
- **Content Limits:** 5000 chars per URL, 1000 chars for AI processing
- **Timeout:** 10 seconds per URL
- **Error Handling:** Graceful failure, continues with other URLs

### Versioning System
- **Parent Tracking:** Original market ID stored in `parent_market_id`
- **Version Numbers:** Sequential (1, 2, 3, ...)
- **Version Tree:** All versions linked to same parent
- **Query:** Get all versions with `parent_market_id` or `id = parent_id`

## 📝 API Usage Examples

### Update Market (Create Version)
```javascript
await marketsAPI.updateMarket(marketId, {
  user_id: userId,
  text: "Updated rumor text",
  category: "Academic",
  stake: 60.0  // Optional
});
```

### Get Market Versions
```javascript
const versions = await marketsAPI.getMarketVersions(marketId);
console.log(versions.version_count); // Number of versions
console.log(versions.versions); // Array of all versions
```

### Get Oracle Reputation
```javascript
const stats = await oracleAPI.getOracleReputation(oracleId);
console.log(stats.oracle.reputation); // 0-100
console.log(stats.oracle.accuracy); // Percentage
```

### Get Top Oracles
```javascript
const topOracles = await oracleAPI.getTopOracles(10);
topOracles.oracles.forEach(oracle => {
  console.log(`${oracle.rank}. ${oracle.pseudonym} - ${oracle.reputation}`);
});
```

### Fetch Evidence
```javascript
const evidence = await oracleAPI.fetchEvidence(
  ['https://example.com/proof1', 'https://example.com/proof2'],
  'Rumor text here',
  marketId  // Optional
);
console.log(evidence.ai_summary); // AI-generated summary
```

## 🔄 Automatic Features

### Reputation Updates
- Automatically updated when market resolves
- Calculated based on oracle report correctness
- Stored in both user table and oracle_reports table

### Evidence Integration
- Automatically fetched when oracle submits report with URLs
- AI summary generated automatically
- Stored in oracle report

### Consensus Weighting
- Automatically uses reputation for consensus calculation
- Higher reputation oracles have more influence
- Works alongside simple majority voting

## 🚀 Next Steps

1. **Frontend UI Components:**
   - Market version history view
   - Oracle reputation display
   - Evidence viewer component
   - Top oracles leaderboard

2. **Enhanced Features:**
   - Web search API integration for auto-evidence
   - University/official source checking
   - News API integration
   - Evidence credibility scoring

3. **Production Improvements:**
   - Cache evidence fetching results
   - Rate limiting for evidence fetching
   - Background jobs for auto-evidence
   - Reputation decay over time

## 📊 Statistics

All new features include comprehensive error handling, logging, and validation. The implementation follows the existing codebase patterns and integrates seamlessly with the current architecture.

