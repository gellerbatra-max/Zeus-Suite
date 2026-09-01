# UI Mockups

High-fidelity static mockups illustrating key application screens, matching the color palette
and typography intent established for the suite (primary blue #1565C0, dark navy top bar
#37474F, Inter typeface -- rendered here with Helvetica Neue as a close local substitute since
Inter wasn't available in this rendering environment).

## Status
A live, editable Figma design file was started for this suite (design tokens, text/effect
styles, Button and Status Badge components) but building further screens is currently blocked
by the connected Figma account's Starter-plan MCP call limit. The Marker Making workspace screen
below was rendered statically instead so work could continue; treat it as a visual reference for
Claude Code's UI implementation, not an editable design source.

## Included
- `marker_making_workspace.png` -- the Marker Making & Production Output workspace: top bar,
  tool palette (Select/Rotate/Flip/Layrule/Match/Pan), a nested-piece marker canvas with fabric
  ruler and utilization readout, and the Automatic Nesting panel showing the async job pattern
  (fabric width / marker length / order quantity inputs, Run Nesting Solve action, and a live
  job-status card with progress bar) that ties to `03_marker_making_production/
  02_automatic_nesting_workflow.png`.

## Not yet built
Screens for the Data Management Platform, Pattern Design & Grading, Format Interchange, and the
3D Virtual Sampling / Digital Twin application, plus the remaining Marker Making screens (cut-data
generation/export, bundle tag & MES registration) -- continue this set once the Figma rate limit
resets, or extend the static-render approach used here.
