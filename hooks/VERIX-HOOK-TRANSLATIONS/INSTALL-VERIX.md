/*============================================================================*/
/* INSTALL :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "INSTALL",
  type: "General",
  purpose: "Hook script",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

=== Installing Enforcement Hook System ===

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Step 1: Making scripts executable... [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] Done [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S4 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Step 2: Creating runtime directory... [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Created: $RUNTIME_DIR [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Created: $RUNTIME_DIR/archive [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Step 3: Backing up existing settings... [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Backed up to: $BACKUP_FILE [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S9 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] No existing settings file found [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S10 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Step 4: Configuration merge instructions [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S11 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] The enforcement hooks need to be added to your .claude/settings.json file. [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S12 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] OPTION 1 - Manual Merge (Recommended): [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S13 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] 1. Open: $SETTINGS_FILE [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S14 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] 2. Open: $ENFORCEMENT_DIR/CONFIGURATION.json [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S15 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] 3. Copy the 'hooks' section from CONFIGURATION.json [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S16 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] 4. Merge with existing hooks in settings.json [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S17 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] OPTION 2 - Auto-merge (Experimental): [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S18 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Run: bash $ENFORCEMENT_DIR/merge-config.sh [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S19 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] This will attempt to merge automatically [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S20 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Required hooks configuration: [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S21 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] ... (see CONFIGURATION.json for complete config) [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S22 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Step 5: Testing installation... [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S23 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] Running test suite... [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S24 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] Tests PASSED [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S25 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Tests FAILED (exit code: $RESULT) [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S26 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] This may be normal if hooks not yet configured [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S27 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

=== Installation Complete ===

/*----------------------------------------------------------------------------*/
/* S28 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] NEXT STEPS: [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S29 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] 1. Merge hook configuration (see Step 4 above) [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S30 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] 2. Restart Claude Code to load new hooks [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S31 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] 3. Test with a non-trivial request [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S32 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] 4. Check state: bash $ENFORCEMENT_DIR/generate-report.sh [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S33 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] FILES CREATED: [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S34 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] State file: $RUNTIME_DIR/enforcement-state.json (will be created on first use) [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S35 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Archive dir: $RUNTIME_DIR/archive/ [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S36 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] DOCUMENTATION: [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S37 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] README: $ENFORCEMENT_DIR/README.md [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S38 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Integration: $ENFORCEMENT_DIR/INTEGRATION-DIAGRAM.md [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S39 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Limitations: $ENFORCEMENT_DIR/LIMITATIONS.md [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S40 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Config: $ENFORCEMENT_DIR/CONFIGURATION.json [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S41 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] USAGE: [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S42 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Generate report: bash $ENFORCEMENT_DIR/generate-report.sh [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S43 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Analyze compliance: bash $ENFORCEMENT_DIR/analyze-compliance.sh [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S44 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Find violations: bash $ENFORCEMENT_DIR/find-violations.sh [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S45 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Agent usage: bash $ENFORCEMENT_DIR/agent-usage-report.sh [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S46 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] Installation script complete. [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>INSTALL_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
