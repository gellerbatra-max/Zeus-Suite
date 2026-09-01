# Function Definitions — ## Style Converter
*A batch utility that converts older MicroMark pattern styles into the newer AccuMark format, so they can be used in modern Pattern Design, Marker Making, and Order Entry.*

### Main workflow functions

**Select style(s) to convert** — You type or pick the name of the MicroMark style(s) you want converted. If you have a lot of styles (the manual recommends this above roughly 2,000 at once), you can use a wildcard (a search pattern like `ABC*`) to grab many styles in one go and convert them in smaller groups rather than all at once, which keeps the process manageable.

**Inspection Options** — A settings screen where you turn on automatic sorting of problem styles. When enabled, any style that comes out of the conversion with a warning or an error gets automatically copied into its own folder (by default under `C:\ads`), so you don't have to hunt through the whole batch to find the ones that need attention.

**Convert / Run** — The button that actually starts the conversion process on the style(s) you've selected.

**Results dialog** — A summary screen that appears once conversion finishes, telling you how many styles converted, and (if Inspection Options is on) asking whether to go ahead and copy the flagged styles into their problem folders.

**Report Results** — A button that opens a spreadsheet-style file (CSV) listing every warning and error found during the conversion, usually in a program like Excel, so you have a permanent record you can review, sort, and act on later.

**Style Converter Viewer** — A side-by-side comparison screen that shows you the old MicroMark version of a piece and the new AccuMark version overlaid on top of each other, so you can visually spot any differences.
- **Measure function** — A tool inside the Viewer that lets you click and measure exactly how far apart two points are, useful for checking how much a shape shifted during conversion.
- **Snap to Geometry** — A tool that lines up the two overlaid versions of the piece precisely, so any real differences between them are easier to see clearly instead of being hidden by a slight misalignment.

### Problems the software finds and flags as errors (these usually mean the piece needs manual correction)

**Intersection error while grading piece** — The piece's outline crosses over itself on the base size or on a graded (resized) version. Fix it by opening the piece in Pattern Design and correcting the outline shape or the grading rules that control how it resizes.

**Piece modification has invalidated a corner angle** — A seam corner style that was previously set on a point no longer fits the piece's current shape. Fix it in Pattern Design by reassigning the corner type or adjusting the piece's shape.

**Unable to store, 2 F points required** — The old style had two grain lines (lines showing fabric direction), which AccuMark doesn't support. Remove one of the two grain lines in the old MicroMark software before converting again.

**Failed MicroMark grading** — Usually means a required update step wasn't run on the style/grade-rule folders, or a grade rule is missing/damaged. Run the Update process on those folders and try converting again.

**Invalid matching lines** — Lines used for matching plaids/stripes across pieces must run parallel or exactly perpendicular to the fabric's grain line; this piece has one that doesn't. Needs to be corrected in the original pattern.

**Rule Table missing** — The grading instructions (rule table) that tell the software how to resize this piece can't be found. Locate the correct rule table and place it in the expected folder, or point the style at a different, existing rule table.

**MicroMark sizes missing** — The style refers to a "synonym table" (a way of renaming sizes) that Style Converter can't fully process. Remove the synonym table reference from the style, or edit it down to a simple rename with no actual size variation.

**Missing OPP Grade Axis** — Some grade points need a reference direction ("OPP axis") defined that isn't set up. Define it either in the old MicroMark data or after conversion in AccuMark.

**Cannot find rule –1** — The piece has a placeholder/invalid grading rule number assigned to a point. Go into the old MicroMark pattern and assign a real, valid rule number to that point.

### Problems the software finds and flags as warnings (informational — often no action needed, but worth checking)

**Piece was flipped, grain line realigned to maintain flip state** — The piece was saved facing the opposite way it was originally drawn; the software automatically adjusted the grain line marking to keep the resizing correct despite the flip.

**Piece with grain line converted to F Rotation will not rotate the same way in AM marking as in MK marking** — A heads-up that this particular piece may lay out slightly differently when nesting/marking in AccuMark compared to how it used to behave in the old MicroMark software.

**Piece message has been truncated** — A note/description on the piece was shortened because AccuMark's description field (20 characters) is smaller than MicroMark's (32 characters); some of the original text was cut off.

**Cut lines are not present in MicroMark piece — sew perimeter is used for comparison** — This piece never had a separate "seam allowance already added" outline defined, so the software compared and saved it using the sew-line outline instead.

**Unavailable rules converted to 0 growth** — A grading rule the piece pointed to doesn't actually exist, so that point/line was set to not grow or shrink between sizes (0 growth) instead.

**Tangent rule not valid on points, replaced with 0 growth** — A type of grading rule meant only for notches was mistakenly applied to a regular point; the software set it to no growth instead of applying it incorrectly.

### Differences the Viewer can highlight when comparing the old and new versions of a piece

**Intersection Moved** — A corner where two edges of the piece meet has shifted position between the old and new version; use the Measure tool to see exactly how far.

**Curves Different** — A curved section of the piece (like an armhole) came out a slightly different shape after conversion, shown highlighted on screen for one size at a time.

**Changes in Notches** — A notch (small cutting guide mark) moved position, disappeared, or an extra one appeared compared to the original piece.

**Overall Perimeter Changes** — The piece's entire outline shifted position (not shape) because its reference origin point changed during conversion.

**Sizes has variations and can not be converted** — The old style used "Variation Sizes" (a MicroMark-specific sizing feature) that Style Converter cannot handle directly; this needs to be resolved through the synonym/size-code setup described in "MicroMark sizes missing" above before it can convert successfully.
