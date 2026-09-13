# Workshop maintenance

- Read the microsoft-foundry skill before changing Foundry integration code.
- Keep the Korean beginner and practitioner paths aligned with executable commands.
- Use only the bundled synthetic data. Do not access company or Microsoft 365 data.
- Do not provision, deploy, assign roles, change the default Azure subscription,
  publish, or push without a separate request to perform that action.
- Keep offline fixtures visibly distinct from real Azure execution. Never fall
  back to another model, endpoint, retrieval provider, or fixture after an error.
- Preserve prompt, dataset, corpus, response, and evaluator lineage. Errors and
  missing rows must not improve an evaluation score.
- Holdout is for final acceptance, not prompt development or regression harvesting.
- Keep Preview/limited-access features optional and date all compatibility claims.
- Run the offline tests, Ruff, Python compilation, and documentation checks.
  Record live Azure checks separately; upstream results are not this edition's results.
