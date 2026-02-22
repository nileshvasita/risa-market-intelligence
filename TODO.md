# Market Intelligence Hub - TODO

## Deployment
- [ ] Link GCP billing account to `risa-market-intelligence` project
- [ ] Create Dockerfile for Cloud Run
- [ ] Deploy to Cloud Run with IAP (restrict to @risalabs.ai)
- [ ] Custom domain: intel.risalabs.ai (Cloud Run domain mapping or load balancer)
- [ ] Make GitHub repo private after deployment
- [ ] Migrate TODO to GitHub Projects board

## Data Expansion
- [ ] Add more states (currently 6 of 50: CA, TX, WA, FL, NY, MA)
- [ ] Deep-dive enrichment for top centers (MD Anderson, MSK, Dana-Farber, Moffitt) - similar to Stanford
- [ ] People-to-workflow mapping (link real stakeholders to workflows they own)
- [ ] More EHR vendor data for newer centers

## Features
- [ ] **People/Org enrichment** - LinkedIn profiles, titles, contact info, org details (evaluate Apollo, Clearbit, or manual enrichment)
- [ ] **UI/UX review** - full usability audit, make portal presentable for external users
- [ ] **Enhanced Chat** - more relevant, precise answers; better context retrieval; source citations
- [ ] **Tutor Hub** - deep-dive learning module for oncology market (may spin off as independent project)
- [ ] Workflow gap analysis (missing: pharmacy, research/trials ops, quality reporting, value-based care)
- [ ] Export functionality (CSV/PDF for centers, people, workflows)
- [ ] Dashboard/analytics view (summary stats, charts, trends)
- [ ] Saved filters and custom views
- [ ] Activity log / change history for notes and edits

## Infrastructure
- [ ] Migrate SQLite to PostgreSQL (Cloud SQL) for production
- [ ] Auth layer (Google OAuth, @risalabs.ai only)
- [ ] Automated data backup schedule
- [ ] CI/CD pipeline (auto-deploy on merge to main)

## Done
- [x] Hash-based routing (reload stays on current view)
- [x] Clean up stale git branches
- [x] Cancer Centers module with filters, search, detail modals, editable notes
- [x] Interactive Leaflet.js map with 327 centers
- [x] Market Map with 9 collapsible categories
- [x] Organizations directory with cross-linking
- [x] People directory (127 stakeholders)
- [x] Stanford deep-dive (45 people)
- [x] Workflows module (305 workflows, 3 view modes)
- [x] AI chat with Claude + general knowledge fallback
- [x] Full cross-module search
- [x] GitHub repo with branch protection
