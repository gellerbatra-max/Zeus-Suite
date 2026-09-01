# Richpeace DGS (Design and Grading System) — Full Function Catalogue
*437 documented functions, extracted from the Richpeace V8.0 manual*

**1 length fix** — Works the same way as 2 length fix, but applied with respect to border 1 instead of border 2.

**1 length fix 2 vertical** — Works the same way as 2 length fix 1 vertical, but with the roles of sides 1 and 2 reversed.

**1 vertical length** — Works the same way as 2 vertical length, but applied with respect to border 1 instead of border 2.

**2 length fix** — A cut-corner type that extends the sewing line of border 1 to the extension line of border 2; the length of segment 2 is entered in the dialog box and a line perpendicular to border 2 is drawn.

**2 length fix 1 vertical** — A cut-corner type where perpendicular lines OB and OA are drawn from point O through sides 1 and 2, a fixed-length line OC (e.g. 3.5cm) is drawn along the extension of side 2, and B and C are connected; commonly used for princess-line seams and two-piece sleeve armholes. Note that line BE and line BC are not collinear.

**2 notch type** — Defines the distance between adjacent notches when multiple notches are created together.

**2 vertical length** — A cut-corner type that extends border 2 to intersect border 1, then draws a line through the intersection point perpendicular to border 2; commonly used on the armhole of a princess-line seam.

**3PARC** — Draws an arc or circle through three points, for design lines or assistant lines of a pattern. Pressing shift toggles between three-point circle and three-point arc mode, and clicking three points creates the shape.

**Actual** — A plot option used to output the pieces at real size (1:1).

**Adaptive stretch** — When enabled, adjusts the height and spacing of repeated drawing elements (such as triangles) created with the intelligent pen so that the user-defined line pattern completes evenly. If disabled, the system uses the fixed defined height and distance, which can result in incomplete or deleted elements at the end of the line.

**Add Grade Data Label to Part Grading Table** — Adds a grade data label for specific grading points by clicking on a grade point or dragging a selection box around the grade points that should have their values added to the grading table.

**Add Seam** — Adds or modifies seam allowance on a pattern piece and lets you cut/shape the corners. It supports adding the same seam value to all sides at once, to selected (marqueed) sides, converting an existing seam by clicking a border line and entering a new value, clicking a border line directly with the tool active, dragging from one border point to another to define the seam, and right-clicking a corner point to change its cut-corner type.

**Add seam val auto** — Automatically adds a seam allowance (default 10mm, adjustable) to each pattern as it is created, when this option is selected.

**Add/replace unparallel curve** — Adds a new unparallel line or adjusts an existing unparallel border or assistant line. The user selects the line and a point on it, opens the Unparallel Curve dialog, chooses Add or Replace, and inputs a distance value (positive to increase, negative to decrease) to reshape the line, e.g., increasing bust/waist/bottom measurements by different amounts.

**Adjust curve** — Accessed by holding Shift and right-clicking a line with the Intelligent Pen; right-clicking in the middle of the line adjusts curve length while keeping both endpoints fixed, while right-clicking near one endpoint adjusts the curve from that side only.

**Adjust with dart or pleat merged** — Combines a dart and a pleat so they can be adjusted together; only works on suitable (matching) patterns. To use it, click the first dart/pleat and the second dart/pleat, right-click to confirm, then click the center line and drag to adjust the merged shape (e.g. adjusting a waistline), right-clicking again to finish.

**ALL EQ. / D.EQ.** — Refers to the pleat dialogue table settings; used within pleat configuration for setting equal spacing options.

**All group** — For line grading, when enabled, entering a grading value in one size group applies it to all size groups, improving efficiency; when disabled, it only affects the current group.

**All line in work view** — When enabled, entering a grading value on any grade line applies a similar grading value to all grade lines in the work view; when disabled, only the selected line is affected.

**All pattern down** — Moves all patterns from the pattern list into the work area. Accessed via Pattern > All pattern down or shortcut Ctrl+F12, then clicking all patterns in the list to move them.

**All pattern hang up** — Removes all patterns from the work area (sends them back to the pattern list). Accessed via Pattern > All pattern hang up or shortcut F12.

**All pattern in work view** — When enabled, clicking Grade applies grading to all patterns in the work view; when disabled, only the selected pattern is graded.

**All Size EQ** — Option in the Pleat dialog that applies to the actual value: the currently entered value becomes the benchmark and all other size groups are set equal to it.

**Angel** — Lets the user freely define the local coordinate system (angle) used for grading a point. The arrow shows the positive coordinate direction (short arrow = X, long arrow = Y); options include Last Point Direction, Next Point Direction, Right Rotate 90 Degree, and Left Rotate 90 Degree to set this coordinate orientation.

**Angel Bisector** — Equally divides a corner (angle) into segments, usable on both draft lines and patterns with the same operation. The user selects a square or two intersecting lines, inputs the number of equal divisions and drags to open the Angel Bisector dialogue, then sets the bisector length using options such as Value of Table (fixed input length), Same Length of the First Curve Selected (matches first selected line's length), Intersect with Line of Two End Points (endpoint lies on the connecting line of the two selected lines), Intersect with the Selected Curve (endpoint lies on a selected line), or The 0 of Angel Bisector (draws only one bisector when multiple exist).

**Angel line** — Creates any-angle lines, including vertical lines and tangent/parallel lines through a point on or off a line, for use in design lines and patterns. Supports making a corner line on a line, a vertical line through a point, and tangent/parallel lines, with shift toggling between reference line orientations and a dialog to input length and angle.

**Any direction line** — Inputs a grade line in any (arbitrary) direction on a pattern, using the same operation as inputting a horizontal line.

**Arc Corner** — Creates equal-distance or non-equal-distance arc corners, useful for making the bottom of a uniform, pockets, etc. Used in both design lines and patterns; you select two lines to round with an arc, can toggle between curve/arc corner styles, choose whether to preserve or delete the corner, and enter values in a dialog to finish.

**ARC cutline** — Creates a curved (radius/tangent) cut line connecting two unparallel lines. The user clicks or selects the two lines, opens the ARC cut line dialog, and inputs the desired value to generate the tangent curve.

**Arc Grading** — Grades an arc's angle, radius, or arc length. Used by clicking the arc with the tool to reveal the circle center point and open the Arc Grading dialog, then entering values and clicking Apply/Close. Dialog options include 'All size EQU' (make all sizes equal at the clicked point), 'Dispersion' (show other sizes as dispersion values relative to the basic size instead of absolute data), and 'Change P' (switch the fixed/unmoved point to the other side of the arc).

**ARC spread** — Creates an arc on a draft line, on a pattern, or in blank space. The user selects the line(s) that should stay fixed near a reference point and the line to be changed, then inputs a value in the Arc Spread dialog to apply the curvature; can also be applied directly by clicking a blank area and entering a value.

**Arrow key grading** — Grades a pattern using the keyboard's up/down/left/right arrow keys (or the arrows in its dialogue box). After setting sizes and colors in Edit Size & Measurement, select a grading point, then use arrow keys to move it step by step (pressing twice moves two steps); TAB cycles to the next grading point clockwise and SHIFT+TAB cycles counter-clockwise. The dialogue lets you edit DX/DY values directly, delete a grading value, define a custom step size, choose Relative or Absolute movement, and choose whether all sizes move by an equal difference/ratio or by individually specified amounts.

**Assist curve auto grading with curve line** — Automatically grades an assistant (auxiliary) line together with the border line it connects to. Select the pattern, use Pattern > Assist curve auto grading with curve line, choose the first option, and click OK; can be applied to all patterns at once.

**Assist Curve control point to grading (G)** — Switches assistant (auxiliary) curve control points to grading points. Operation: click the selected pattern, then Edit - Assistant point to grading point, and choose to convert all assistant line points on the line to grading points.

**Assist curve parallel grading** — Grades an inner (assistant) line of a pattern so that it remains parallel with and intersects the border line. Operated by clicking the graded side point, the non-graded side point, and then the border line.

**Assistant Button / Switch Selected Status (Key F)** — Digitizer mouse button function used to switch or toggle the currently selected status/option during pattern input.

**Assistant curve grading point to non grading (N)** — Converts all assistant line grading points back to non-grading points; operated the same way as Assist Curve control point to grading.

**Assistant curve notch** — Adds a notch on the border that an assistant line points to; when the assistant line's side/direction is adjusted, the notch placement changes accordingly. Clicking or marquee-selecting to one side of the assistant line adds the notch to only that border, while selecting at the center adds notches to both sides; right-clicking the notch allows editing its properties. On patterns with seam allowance, the notch is shown only on the seam.

**Assistant line** — Sets the line type used for assistant (construction) lines when plotting.

**Auto Adjust font height for printing** — When printing a pattern on a single sheet of paper (e.g., A4), this tool automatically adjusts the height of the grade data label and measurement variable font to prevent text from printing too small. Clicking in a blank area adjusts the font height based on the current printer settings, and clicking on a 'Grade data label' or 'Measurement Var font' lets you reposition it.

**Auto Arrange Patterns** — Menu command (Edit menu) that automatically arranges all patterns placed in the work area, typically used to prepare patterns before plotting.

**Auto Arrange Sewing Order** — Automatically arranges the sewing order for a pattern that has many sewing lines. The user selects the lines needing a sewing order, clicks the starting sewing line, opens the Auto Arrange Sewing Order dialogue, selects an operating range option (e.g. "only parallel lines") and effect, inputs a starting index number for the sewing line, and clicks OK; the system automatically calculates parallel line quantity to assign sequential order to the selected lines.

**Auto confirm sign** — When enabled, the system automatically identifies whether an input grading value should be treated as positive or negative, regardless of the sign typed by the user.

**Auto Confirm Sign Icon** — Icon that automatically completes/confirms grading, used to finish grading for front and back waist length, armhole depth, front collar, and darts (V dart and fastigiate dart).

**Auto Design** — Imports a style file created in formula design and allows editing of its size and measurement values. Select the desired style from the Auto Design dialog (which shows the style picture, structure picture, and size table), modify size values as needed (including via a 3D measurement tool), and click OK to automatically generate the pattern and design lines.

**Auto smooth** — An option in Move and Rotate Adjust that causes the system to automatically create a smooth line without requiring manual adjustment.

**Autoarrange pattern** — Automatically arranges the patterns in the work area to simplify manual layout. Operation: arrange patterns roughly in the work area, click Edit - Auto arrange pattern, set which sizes to exclude (mark them white), and the system arranges patterns according to paper width.

**AVE.Size** — Option in the Pleat dialog that sets the dispersion between adjacent sizes to be equal.

**average interval** — When enabled, entering a grading value for a non-base size causes the other sizes to be graded with equal intervals automatically; when disabled, different values can be entered per size.

**Base point** — Inputs a base point on a grade line, which is used to confirm the direction of grading; select the tool, click the position on the pattern, then click Grade.

**Bias Attr** — Field in the Pleat dialog used to set the bias direction and distance of the pleat sign.

**Border 1, 2 Intersect** — A cut-corner type in the Add Seam dialog where the seams at the piece's corner extend naturally and intersect with each other.

**Browse File** — Displays all files under a selected path in the Open dialogue; files without style/pattern data are marked with an '×'.

**Button hole** — Adds button holes to a pattern and allows modifying existing button holes; on graded patterns the number of button holes can be set to be equal or unequal across sizes. Button holes can be placed automatically based on a specified offset, quantity and spacing (entered in the 'Add button hole' dialogue, which also sets angle and button-hole type/shape), distributed automatically along a selected line, or given different quantities on different sizes; existing button holes can be edited via a right-click dialogue.

**Button Hole (Key 9)** — Digitizer mouse button function used to input a button hole marking on the pattern.

**Camera Input** — A tool/workflow for digitizing patterns by photographing them with a camera instead of a digitizer. Requires specific hardware (a camera with minimum 3 megapixels and remote control capability, a mounting rig, a flat table, and a printed grid background) set up according to specified dimensions and camera height.

**Change border segment** — Interchanges a design/assistant line with a pattern border line (or vice versa), and can also be used to make one pattern's border replace another's. Select or marquee the line, right-click to flip its orientation horizontally/vertically if needed, then click on the target object and right-click to finish; dragging points allows swapping which side becomes the border.

**Change border to assistant curve** — Converts a pattern's border into a closed assistant line matching another pattern, effectively merging two separate pattern pieces' outlines into one assistant line by clicking corresponding key points on each pattern (or pressing Enter for offset).

**Change Grade Label Position** — Moves a grade data label to a new location by clicking it and dragging it to the destination position.

**Check Sewing Order** — Switch the cursor to the sewing template tool, move it outside the pattern, and type a number (e.g. 3) to select the slot line with that number; continuing selects the next numbers in sequence (4, 5, 6...). If a pattern is selected, only that pattern's lines are shown; otherwise all lines with the given number are shown.

**Circle** — Reads the center point of a circular drill mark on the pattern, done before or after finishing the border line by pressing 0.

**Circle (Key 0)** — Digitizer mouse button function used to input a circular marking point on the pattern.

**Clear all assist curve in pattern** — Deletes all assist (auxiliary) curves belonging to the selected pattern. Select the pattern, use Pattern > Delete all assist curve, choose the first option, and click OK; can be applied to all patterns at once.

**Clear assist curve grading** — Deletes grading applied to assist (auxiliary) curves on the selected pattern. Select the pattern, use Pattern > Clear assist curve grading, choose the first option, and click OK; can be applied to all patterns at once.

**Clear corner notch** — Clears/removes corner notches that were created using the corner notch tool. Select the pattern, use Pattern > Clear corner notch, choose the first option, and click OK; can be applied to all patterns at once.

**Clear pattern grading** — Clears the grading values currently applied to the selected pattern. Select the grading value to clear, open Pattern > Clear pattern grading, choose the first option, and click OK; can be applied to all patterns in the work area or style at once.

**Clear select pattern** — Clears the current modification operation on the selected pattern and returns it to the pattern list, effectively reverting to the state before the modifications without affecting the work area version. This differs from deletion since the pattern is only removed from the work area, not destroyed.

**Clear text of pattern** — Clears text that was written onto the pattern using the Text (T) tool, excluding pattern info on the grainline. Select the pattern with text, use Pattern > Clear text of pattern, choose the first option, and click OK.

**Close/Finish (Key 2)** — Digitizer mouse button function used to close a line or finish the current input operation (e.g. finishing reading a pattern, dart, or assistant line).

**Closed Assistant Line** — Tool for adding a closed internal assistant line to a pattern: after reading the border line, the user clicks this tool, inputs points according to their type, and presses the finish key to complete the closed loop.

**Color Setup** — Sets the colors used for the Pattern List box, the working area (window background, operation prompt colors, measure prompt color, remark color, selected/unselected pattern colors, fill pattern colors for path comparison, scan image color, grid color), and size colors. Operation: click the icon to open the Setup Color dialog, choose an option and item, pick a color, click Apply, and repeat for all needed items before clicking OK to confirm.

**Colour setup** — Sets or changes the color used for design lines. Operation: choose a color from the pull-down list to draw new lines in that color, or click the tool's small triangle to open the pull-down list, select a color, then right-click or box-select existing lines to change their color.

**Compare length** — Measures the length of one or more lines, sums multiple length values, and can disperse the difference across multiple lines after comparison; also measures notch-to-point length. It can compare groups of lines against each other (e.g., comparing a sleeve arc length to the front and back armhole length) and displays the length difference (L) in the Compare Length dialog. Shortcut key: R.

**Compare Length Tool** — Tool used to check the dispersion (difference) between the armhole curve length and the sleeve curve length across sizes.

**Compare path work** — A comparison tool with a dialogue table of parameters for matching notches/points between two pattern paths. Options include adding equal-length notches from the start point (Fixed pattern/Stepped pattern), offsetting notch placement, flipping the stepped pattern once or twice, automatically matching two notches within a set dimension when skipping casing value, and returning the stepped pattern to its original position after comparison finishes (or leaving it at the stopped position if not selected).

**Compasses** — Creates fixed-length lines using single or double compasses. Single compasses makes a fixed-length line from a key point to a line (e.g., for shoulder, armhole, waist, or sleeve arc bias lines); double compasses makes two specified-length lines through two fixed points (e.g., for sleeve arc bias lines or lapel points), with an offset option for tasks like drawing a back trouser pocket.

**Connect/Adjust X/Y** — Moves an assistant line so it lies near/against the pattern border, while making the grading value at the assistant line's side point unchanged in the X (or Y) direction, applying the grading only in the Y (or X) direction. The user selects the assistant lines to move, right-clicks, then clicks the pattern border to snap them near it.

**Continue** — Allows resuming input of additional elements (such as notches or assistant lines) on a pattern that has already been returned to the packing list. Operation: select the pattern, click the Continue command, the pattern reappears in the dialogue table, then continue reading elements into it.

**Copy** — Copies the grading value(s) assigned to selected grade line(s) so they can be pasted onto other lines.

**Copy bitmap** — Copies a selected design line/picture (from the picture library) to the clipboard as a bitmap so it can be pasted into other software like Excel or Word. Operation: use the Pic lib tool to marquee-select the design line, right-click, then click Edit - Copy bitmap, and paste into external software.

**Copy Grading** — Copies the grading values (dx/dy) from one or more selected grading points so they can be pasted onto other points later.

**Copy grading value** — Copies grading values from a graded point/pattern to an ungraded point/pattern. Supports copying a single grading point, multiple grading points via marquee/drag selection, continuous pasting to multiple points by holding Ctrl while selecting, and copying in one direction or the opposite direction via a dialog option.

**Copy pattern** — Used together with Paste pattern to copy a selected pattern to the clipboard. Operation: select the pattern to copy, then click Edit - Copy pattern.

**Corner** — Shortcut V. Extends two lines until they cross and deletes the unselected/protruding part beyond the intersection. Operation: select the tool, click one line, then hover over the second line (cursor color changes to show the line that will be kept), and left- or right-click to complete.

**Corner connection** — Accessed by left-click-dragging a marquee box over two lines with the Intelligent Pen, then right-clicking; joins the two selected lines together at a corner.

**Corner notch** — A tool for adding notches at corners of a pattern piece, with the notch angle settable to 0°, 90°, 180°, or 270°. Notches are added to the border(s) that an assistant line points to: clicking or marquee-selecting to one side of the line adds a notch to that side's border only, while selecting at the center adds notches to both sides; the notch degree can also be adjusted by dragging a displayed green line to the desired angle.

**Corresponding length / adjust xy** — Sums the grading values of multiple lines and applies the combined grading to a single point, e.g., grading the waist according to a waist line. The user selects the tool, chooses X or Y direction (via Shift), selects the line(s) to grade with a marked grading point, right-clicks, then selects the reference line(s) to produce the graded result.

**Count and gap** — Sets a different notch number and the gap between notches.

**CR ARC** — Draws an arc or circle by clicking a center point and then entering an arc length value in a dialog box. Works the same way as CR Circle, and shift toggles between three-point circle and three-point arc modes; used for design lines or assistant lines of a pattern.

**Creat design line to pattern** — Creates a new design line on the pattern by clicking it. Select the pattern, use Pattern > Creat design line to pattern, choose the first option, and click OK; can be applied to all patterns at once.

**Creat shadow** — Creates a shadow copy of all points and lines of the selected pattern, useful for comparing against the original before making modifications. Select the pattern and use Pattern > Creat shadow (shortcut Ctrl+Q).

**Create Regular Sewing Template and Put Pattern to Regular Sewing Template** — Select the sewing template tool and drag on a blank area of the work area to open the Create Regular Template dialogue; enter values and click OK to generate a regular sewing template with a start point for machine needle matching. Move the pattern onto the template and right-click on a blank area of the template to merge the pattern and template into one part. Used for the Richpeace Auto-sewing template machine.

**Create sewing template** — Dialogue for creating a sewing template, where Blank width sets the distance of the pattern relative to the computer screen, and Radius sets the part of the plastic template that needs to be cut.

**Cross isometry line** — Accessed by holding Shift, pressing and dragging with the Intelligent Pen, then clicking two crossing side lines; creates an isometric line that intersects both selected lines.

**Current plotter** — A setup option used to select the model of plotter to use, chosen from a pull-down list of plotter names.

**Curve** — Draws a curve or straight line freely. Operation: for a straight line, click two points then right-click to open the Length and Angle dialog and enter values; to connect two existing points, right-click on each point then right-click again; to draw a curve, click at least three points then right-click to finish.

**Curve adjust** — Checks or adjusts the length of a curve relative to the straight line between its two endpoints, and can offset a side point of the line; usable for both design lines and pattern pieces. One cursor mode adjusts curve length/straightness via a dialog (with options such as length, straightness, and end-point offset, including DX/DY value copying between lines), while the other cursor mode (toggled with Shift, shortcut Shift+S) lets one side point of the line move freely by dragging.

**Curve aline** — Shortcut T. Extends multiple lines to align with either one target line (one-way extend) or two target lines (two-way extend). Operation for one-way: click or marquee-select lines a/b/c, right-click, then click target line d, move the cursor to the desired position and right-click to confirm. Operation for two-way: click or marquee-select lines a/b/c, right-click, then click target lines d and e.

**Custom curve** — Saves a curve shape defined by the user for reuse, and allows modifying the custom curve's properties (such as height and distance), for shapes like stars or triangles. To save, the user draws the line type, appoints required line-type points, selects the shape (click or drag a square), right-clicks, and clicks a point to open the Save As dialogue.

**Custom Curve (User-defined curve properties)** — Lets the user modify a user-defined curve's properties via the Custom Curve dialogue, setting parameters such as Height (the curve's peak height), Gap (minimum distance between two figures when adaptive stretch is off), Adaptive Stretch (whether equal-length lines stretch or not), Count and Gap (number of repeated figures, e.g. triangles, along the line and their spacing), Gradual Change (varying head and tail width/height for a graduated effect), and Split (making each figure a separate single shape rather than a continuous line).

**Custom dash** — Lets the user set the segment length and the gap distance between segments for a custom dashed line style used in sew lines.

**Cut Angle Bisector** — A cut-corner type used for making collar points; it cuts the corner along the perpendicular direction of the angle bisector, with the length of the resulting line entered in the length table.

**Cut Apart** — Used to amend or divide a pattern, or to deduct surplus material; usable on design lines and patterns, for example when making a big-bottom shirt or hem border. The user selects the operation line, the non-spread line, the spread line, and (if present) a divide line, then enters the total expansion value and mode in the Cut Apart dialog (Divide, Smooth, or Keep Form) to spread, connect, or reshape the pattern.

**Cut length** — Sets the length of material to be cut in a single cutting pass.

**Cut on bias** — A cut-corner type used for making sleeve placket or shirt placket corner seams; you enter the line length outside the seam line in the length dialog to define the corner width.

**Cut outside border** — When selected and using a cutter/plotter, cuts along the outside border line; enables the Fixed length and Cut length settings.

**Cut pattern** — Used together with Paste pattern to cut a selected pattern to the clipboard so it can be pasted elsewhere. Operation: select the pattern with the select ctrl point tool, then click Edit - Cut pattern.

**Dart combine** — A shift-variant of the dart/pleat merge tool used to delete a dart or change its width, and to change a designated border line. Operation: click the fixed point (e.g. hip point), then click the second dart point; click a third point to delete the dart, or click on blank space and enter a new dart width value to resize it instead.

**Dart line** — Adds a dart line to a dart; usable in design line mode. The user clicks the curve or fold line close to one side of the dart, then clicks the curve or fold line close to the other side (in the order matching how the dart points toward the middle) to define the dart line.

**Dart pleat** — Used when reading a dart or pleat; requires reading at least one border line. A V dart does not require reading other darts/pleats and needs no menu selection, and when reading multiple darts/pleats of the same type, the type only needs to be selected once.

**Dart/Pleat (Key 5)** — Digitizer mouse button function used to input dart or pleat points, such as dart first point, waist point, tip point and end point.

**Default parameter** — An options section for configuring default values used elsewhere in the system, including notch settings, seam allowance, point size, and dart drill distances.

**Delete** — Deletes the currently selected grading rule sort from the Grade Rule Dictionary.

**Delete all pattern in working area** — Deletes all patterns present in the work area's pattern list. Choose Pattern > Delete all pattern in working area and confirm Yes to delete all patterns, or No to cancel.

**Delete Grade Data Label** — Removes grade data labels: press Shift and click a blank area with the tool to input an option and delete labels generally, or press Shift and click/box-select specific grade points, then hover over the label until it highlights and press Delete to remove that point's label.

**Delete grade lines** — Deletes selected grade lines after confirming the action in a dialog box.

**Delete line** — While in edit mode, deletes a row from the grading rule table; the change must be saved with Save or Save As.

**Delete selected Pattern** — Deletes the currently selected pattern from the pattern list in the work area. Select the pattern, choose Pattern > Delete selected pattern (or Ctrl+D), and confirm Yes in the dialogue to delete it, or No to cancel.

**Delete shadow** — Deletes the shadow previously created on a pattern. Select the pattern and use Pattern > Delete shadow.

**Delete Slot** — Click on a slot with the eraser tool to delete it.

**Delete Stitching Line** — Removes a stitching line either by using the eraser tool, or by right-clicking on the pattern's stitching line and selecting the blank type instead of straight or curve.

**Design line** — A plot option that plots draft lines that have not yet been created into a finished pattern.

**Design toolbar** — Toggles whether the design toolbar is displayed.

**Dictionary** — Stores and sorts size names (and separately part names) so they can be selected and reused in sorted order.

**Digitizer notch type** — Sets the default notch reference point used by the Read Pattern (digitizing) function.

**Digitizer setup** — Configures settings for a digitizer input device, including digitizer model, digitizer size, communication port, 16-key mouse button function assignments, default button setup, digitizer menu area (rows/columns), and precision calibration (done by digitizing a 50cm x 50cm rectangle and entering the measured actual length). Includes a 'Print menu' button to automatically print the configured digitizer menu, and an 'Edit menu' option to set up pattern names for each digitizer input area for direct pattern info entry.

**Disjoin border and assist curve** — Disconnects the relationship between a border line and its assistant line so that grading the assistant line does not change the border line's grading value. Select the pattern, use Pattern > Disjoin border and assist curve, choose the first option, and click OK; can be applied to all patterns at once.

**Disp in g** — When working with a single group, after selecting the basic size and entering a dispersion (increment) value, clicking this calculates the different size values for that group; in group mode it only affects 'Disp in g'.

**Disp.g** — When working under a group, after selecting the group's basic size and entering a dispersion value, clicking this automatically calculates the basic size value for the group.

**Dispersion** — Toggle in the Pleat dialog: when selected, values are shown as actual dispersion between sizes; when not selected, values are shown as actual (absolute) values.

**Display relative grading or absoluted grading** — Toggles whether grading values are displayed as absolute values (difference between each size/group and the base size/group) or as relative values (difference between each size/group and the immediately preceding size/group).

**Display/Hide remark** — Shows or hides remarks/annotations, such as sizes recorded with the compare length tool or two-point measurement tool, on the pattern.

**Divide pattern** — Cuts a pattern piece into separate pieces along a selected assistant line. Select the tool, then click the assistant line on the pattern to perform the cut, with a prompt to confirm or cancel the division.

**Divider** — Adds equally spaced points on a line, or equal-distance points in opposite directions along a line; can be used on design lines and patterns. Shift toggles between adding equal points and equal-distance points in opposite directions, and right-click toggles whether equal lines are added at the points; can also divide only part of a line between two selected side points.

**Double compasses** — Accessed by pressing on a key point and dragging to another point with the Intelligent Pen; functions like a compass using two reference points to determine the new point location.

**Draw grainline** — When selected, draws the grainline when plotting or printing the pattern.

**Draw line** — Default left-click mode of the Intelligent Pen: click on a blank spot, key point, intersection, or line to start drawing a line; press Enter on a key point to offset before drawing; after the first point, right-click to switch to horizontal/vertical/45-degree line mode or free-direction line mode, and press Shift to toggle between curve and straight line.

**Draw line with Angel** — Draws a line at a specified angle and length, with an option for 'Opposite direction' to disperse the angle 360 degrees relative to the original degree.

**Draw sew border** — When selected, draws the sew border on the output.

**Draw sew border notch** — When selected, draws the notches for the sew border on the output.

**Drill** — Adds drill (button) marks to a pattern and allows modifying their attributes and number; on graded patterns, the number of drills can differ between sizes. Drills can be placed automatically based on a specified start offset, quantity, and horizontal/vertical spacing (via the Drill dialogue), added evenly along a selected line (via the 'Add drill at curve' dialogue, which only grades from the line's start and end points), or set to different quantities on different sizes; if the pattern shape is later modified, the spacing and quantity of drills remain fixed relative to the line's endpoints.

**Drill (Key 6)** — Digitizer mouse button function used to input a drill hole marking point on the pattern.

**Drill Attribute** — Dialog opened by right-clicking on a drill/button that sets its properties: mark it as an actual drill hole to be cut when connected to a cutting plotter, mark it as draw-only (drawn but not cut) when connected to a cutter or plotter, or select Drill M43/M44/M45 to define the hole size used by the cutter.

**Drill distance of dart** — Sets the distance from the drill mark to the top of a dart, and the distance from the drill mark to the waist point of a dart.

**Edge Ext Grading** — Extends one side line at a corner so that the corner angle is the same across different sizes. Operation: click the point to extend (B), the corner vertex (A), and the other side point (C) to bring up a Distance dialog, then input the desired value and click OK.

**Edit Notch** — A dialogue box (opened by right-clicking a notch) used to change a notch's position and properties. It lets you set the locate type (distance-based, measuring from a reference point, or proportion-based, measuring as a ratio of a reference length), choose grading vs. non-grading reference points, add multiple notches at once (two or three, spaced by a set gap), and control how notch position grades across sizes via Dispersion, All EQ, and related distance settings.

**Edit Size &Measurement** — Edits size names, measurements, and associated colors to facilitate grading and pattern-making; lets the user input fashion sizes that are adopted during auto grading and stores detailed size data. Accessed via Size > Edit size & Measurement (Ctrl+E), where size names and part names/measurements are entered into a table, with new rows added automatically as needed.

**Edit Size and Measurement** — Menu command (under Size menu) used to insert or add sizes and set the basic size for a pattern before digitizing or grading a graded pattern.

**Edit size table** — Opens a dialogue for setting up and editing the size table, including opening/saving size tables, managing size and part name dictionaries, switching between single and group size views, importing size files, and calculating dispersions.

**Edit table** — Enters edit mode in the Grade Rule Dictionary so an existing regulation can be modified; changes must then be saved with Save or Save As.

**Enable or disable assistant curve auto grading with border** — Toggles whether an assistant (inner) curve automatically follows grading changes made to the border line. When enabled (cursor switched via Shift), modifying the border grading updates the assistant line automatically, either on both sides or just one side depending on selection; when disabled, the assistant line does not update when the border is regraded.

**Equal height grade** — Makes the height of curves between two grading points equal across sizes after grading. Operation: use the Select Pattern Point tool to drag-select the curve to be treated, then click the Equal Height Grade icon.

**Equal notch** — Adds notches to two groups of lines and can also incorporate easing amounts. Operation: click or marquee-select the first line near point A, right-click; then click or marquee-select the second line near point C, right-click to open the Equal Notch dialog; input the appropriate values and click OK. Dialog parameters: Length1/Length2 are the selected line lengths before/after right-clicking; DL is the dispersion between the two line groups; Notch1/Notch2/Notch3 specify the notch length at successive positions along the lines, with the corresponding length on the second line equal to the notch value plus any easing.

**Equal spread** — Spreads a pattern equally according to appointed lines. Used on a pattern by clicking the non-spread line, then clicking the spread line, and right-clicking to complete the equal spread.

**Equal X** — Command that sets the X-direction grading value equal across sizes for the selected points; used after entering a value (e.g. 1cm) in the grading table for a non-basic size.

**Equal Y** — Command that makes the Y-direction grading value equal across sizes for selected points; can be used first, then followed by entering different values per size for non-equal Y grading.

**Equidistance curve** — Shortcut Q. Draws a line at an equal (parallel) distance from an existing line. Operation: click on the line with the tool, drag the cursor and click to open the Parallel dialog, input the offset value, and click OK.

**Equidistance curve intersect with two curve** — Shortcut B. Draws an equidistant curve that intersects with two other curves, capable of creating multiple offset lines at once. Operation: click the line to be offset (its color changes), click the side that intersects with the selected line, move the mouse to the desired position to open the Parallel dialog, input the value, and click OK.

**Eraser** — Deletes points, lines, or design lines, including assistant lines, notches, buttonholes, and dart/pleats. Click on the object to delete it, or drag a selection square to delete multiple objects together.

**Error** — A password-protected setting used to correct plotting size errors by entering the real measured width and length of a plotted 1m x 1m test rectangle, so the system can compensate for inaccurate output size.

**EXIT** — Closes and exits the software system.

**Export ASTM file** — Converts the current software's pattern file into ASTM format. Open the file to be converted, then use File > Output ASTM file, choose a save path, enter a file name, and click Save.

**Export to file** — A setup option that saves the pattern as a .plt file instead of sending it directly to a plotter, allowing it to be opened and plotted later from Plotcenter even without the design software.

**Extending the sewing line** — Extends the lines of borders 1 and 2 until they cross the seam, then cuts the corner along the direction of the line connecting the intersection points.

**Fastigiate Dart** — Tool/menu item for inputting a fastigiate (tapered) dart: the user selects it from the menu, then reads the dart's first point, waist point, tip point and end point (with curve points marked as needed); only one side is read due to symmetry.

**Fill pattern** — Toggle (Ctrl+J) that fills the pattern with color when selected; otherwise no fill is shown.

**Fix length** — Keeps a curve's length unchanged while letting its shape be adjusted; usable on both design lines and pattern pieces. Operation: click the curve to select it, then move a control point to the desired position — the curve reshapes without changing its total length.

**Fixed length** — Sets a fixed length to keep the pattern aligned/relevant with the paper when cutting.

**Fixed path** — When enabled, all files are saved only to a designated/appointed path, preventing files from being saved elsewhere and avoiding lost files; the system will prompt the user to save to the appointed path if they try to save elsewhere.

**Flank pieces** — Used for creating the side face (gusset) of a bag. The user selects a first pattern and clicks points A' and B', selects another pattern and clicks points A and B, then inputs parameter values to generate the side face piece.

**Flouncing** — Creates helical flouncing on a design line. Either click on a blank area to open the Flouncing dialog and input new data, or select the operation line by crossing/marquee selection, right-click, then choose the first and second segment lines and one of three flounce types before confirming.

**Fold out pattern** — Used to copy part of a pattern by mirroring it across a selected center line. The user selects the center line (or two points defining it), then selects the line to be mirrored to produce a symmetrical copy (e.g., copying a placket).

**Forfex** — Picks up (creates) a new pattern from enclosed design lines or assistant lines. Method 1: click or box-select the border lines and click right to auto-create a pattern from the enclosed area. Method 2: hold Shift and click inside enclosed areas to fill them with color (multiple areas can be added), then click right to finish. Method 3: click points along the border clockwise until the boundary closes (completed segments turn green), then click right to finish. After finishing, the tool switches to the pick-up-assistant-line tool. Shortcut key W.

**Forfex (with replace pattern dialogue)** — Used to cut out a new pattern from an existing one, or to create a new pattern that replaces the original. The user selects the tool, clicks along lines one by one, then right-clicks to open a dialogue offering 'create a new pattern' or 'create a new pattern and replace old one' (which replaces the original pattern by index while keeping elements like notches and text), then clicks OK to finish.

**Globe data** — Checks the area and perimeter of patterns by material or individually. Operation: click Pattern - Globe data to view the Globe data dialog; if 'different material' is checked, area/perimeter are calculated per pattern, otherwise calculated as actual total quantity.

**Grade Data Label** — Adds a dispersion (grading value) label to a graded pattern piece. Operation: choose View - Grade Data Label, click a blank spot on the work area to open the Create Grade Data Label dialog, select the desired option, and click OK.

**Grade Nest of Pattern** — Overlaps multiple separate patterns into a nested pattern, for example when a pattern has been digitized into DGS as separate pieces. The user holds shift to toggle overlap by area or by size, ensures all patterns' grainline directions match, selects the patterns to nest, then clicks the basic size and subsequently clicks other patterns in order from smallest to largest size.

**Grade rule Dictionary** — A dialog that manages saved grading rule sets ('regulations'/sorts). Clicking a saved regulation refreshes the dx and dy formulas shown in the Rule Grade Table; clicking a dx formula updates it without changing the current dy formula, and vice versa.

**Grade table** — Opens the Grade table for entering grading values. Click the icon, select one or more pattern control points, enter grading (dx/dy) values for sizes other than the base size, and use tools like Equal X/Equal Y/X Equal Y to apply the grading.

**Graded (Key E)** — Digitizer mouse button function used to mark/read a point as a graded point, moving from the basic size up through the other sizes in sequence.

**Grading by parallel and distance** — Grades a point (such as a shoulder point) so that it stays parallel across sizes at a given distance, using the Distance Point dialog. Operated by clicking two points on a reference line (e.g., back center) and then the target point, then entering the distance value and selecting the appropriate option in the dialog.

**Grading of assistant curve** — Grades an assistant line's intersection point on the pattern according to a specified length along the border line (e.g., an AB curve length). Used by double-clicking the assistant line point to open the Grading of Assistant Curve dialog, entering a value and options, and clicking Apply. The dialog includes a Length field (distance from the selected point to a reference point), a Locate/Angle reference point option, and a Dispersion option controlling whether values represent per-size differences or absolute distances, with buttons to apply a value to all sizes equally, by cursor-located size, or by dispersion from the basic size.

**Grading Point on a Curve (Key 7)** — Digitizer mouse button function used to input a point on a curve that carries its own grading value.

**Grading Point on One Line (Key 1)** — Digitizer mouse button function used to input a grading point that lies on a straight line.

**Grading toolbar** — Toggles whether the grading toolbar is displayed.

**Grainline** — Adjusts the direction, location, length, and text info of the grainline (weaveline) on a pattern piece. Clicking two points sets the grainline parallel to them; right-clicking rotates it in 45-degree steps; clicking on the pattern then right-clicking allows free rotation; dragging the middle moves it; dragging an end point adjusts its length; and using Shift plus right-click or left-click rotates the grainline's text label by 90 degrees or to any chosen direction. Rotating the grainline does not rotate the pattern itself.

**Grainline (have different direction)** — Sets the grainline of a graded pattern so that different sizes can have different grainline directions. The user switches from 'match all the size' to 'match one size' (via F11) and then clicks two pattern control points corresponding to the size being modified.

**Grainline (Key D)** — Digitizer mouse button function used to input the grainline of the pattern.

**Grainline fault Direction** — Sets the direction of the grainline. Click the arrow to open a pull-down menu, select the needed direction option, then click Apply and OK to apply it to the pattern's grainline.

**Group** — Toggles the size table view; by default a group of sizes is shown, but selecting this command switches to displaying a single group/size.

**Guide line parrallel** — Creates a guide line parallel to a reference based on two selected points, used to mark a specific placement/distance. Select two control points with the select tool, run Pattern > Guide line parallel to get a dashed guide line, then use the modify tool with Ctrl-click to input a distance and copy the guide line.

**Hang up select pattern** — Moves a selected pattern piece from the work area back to the pattern list. Used with the "select pattern control point" tool: select the pattern, then click this icon to send it back to the pattern list.

**Hide part assistant line** — Hides selected assistant (construction) lines on a pattern to make checking grading situations easier when there are many assistant lines. Operated by pressing Shift+U, then clicking or dragging a square over the assistant line(s) to hide them.

**Horizontal line** — Inputs a grade line in the horizontal direction on a pattern by clicking start and end points (and optionally a right-click to finish), usable across one or multiple patterns and with middle points added.

**Horizontal or vertical line** — Accessed by dragging with the right mouse button from a key point using the Intelligent Pen; draws a horizontal or vertical line, with right-click used to toggle between the two directions.

**Horz or vert line** — Forms a right-angle (horizontal or vertical) line between two points, including at a crossing point or a point on one side. Operation: click one point, right-click to switch between horizontal and vertical orientation, then click the second point.

**Horz/vertical adjust** — Adjusts a selected line (and the pattern edge it belongs to) so it becomes horizontal or vertical, typically used to clean up digitized/input patterns. Pressing Shift toggles between horizontal and vertical adjustment mode; selecting or marqueeing the line and right-clicking opens a dialogue box to choose the adjustment option and confirm. This changes pattern size slightly, so it is meant for small corrections rather than full realignment.

**Import** — Imports a size summary file (*.SML) into the size table.

**Inch fraction format** — When selected, inch measurements are displayed using a fraction format; when not selected, decimal format is used instead.

**Increase sew line of two point** — Adds a sew line between two specified points where the distances from the border line and between successive lines (A1/A2, B1/B2, C1/C2) can differ at the start and end points, producing a sew line whose width is unequal at the two ends while the curve height remains constant; this line cannot be stretched afterward.

**Increase/Decrease pattern** — Increases or decreases the size of an entire pattern. The user selects the pattern, right-clicks, drags and clicks to open the Increase/Decrease dialog, then inputs the desired value and confirms.

**Inner Border Line** — Tool for adding an inner border line (e.g. for a hollow or lining piece) to a pattern: after reading the outer border line, the user clicks this tool, inputs points per their type, and finishes with the Close/Finish key.

**Inner Fastigiate Dart** — Tool/menu item for inputting a fastigiate dart located on an inner border line, following the same operation as the standard fastigiate dart after the border line has been completed.

**Inner V Dart** — Tool/menu item for inputting a V dart located on an inner border line, following the same operation as the standard V dart after the border line has been completed.

**Input Pattern** — Digitizes a manually made paper pattern into the computer using a digitizer board and digitizer mouse. The user traces border lines, assistant lines, darts, pleats, drills, button holes, grainlines and grading points in a defined point order, using preset digitizer mouse buttons for different point types, finishing each pattern or line with a designated key.

**Input pattern dialogue table** — A parameter dialog shown when inputting a pattern; it lists selectable notch types and point types via dropdown arrows, and the notch type selected here becomes the notch shown when reading the pattern. When reading a curve grading point, only 3 buttons of the digitizer mouse can be used.

**Insert dart** — Inserts a dart or pleat on a selected line, used on design lines and patterns, typically for making Hubble-Hubble sleeves or three-dimensional pockets. If a spread line exists, select the operation line and spread/dart lines then enter values in the Spread Dart dialog; if there is no spread line, select the line and use the Gathering dialog to enter the dart or pleat value.

**Insert line** — While in edit mode, inserts a new row into the grading rule table; the change must be saved with Save or Save As.

**Insert or Edit Image** — Places an image, such as a logo or design line, onto a pattern. Supports *.BMP, *.JPG, *.GIF, *.PNG, *.TIF, *.DST, *.DSZ, *.DSB formats. The user drags a square on the pattern, browses to load a picture, inputs length, width, vertex, and angle, then clicks OK to place it; the image can then be moved, resized, rotated, or aligned to an axis via its midpoint, and deleted using the eraser tool.

**Inside border** — Creates a hollow (cut-out) shape inside a pattern. It can pick up an inside border from a design line (select the working pattern so its outline fills with color, then select the inside border line(s) and click right to finish), or from an area enclosed by assistant lines within the pattern (select or box-select the assistant line area and click right to finish).

**Intelligent Pen** — A multi-purpose shortcut tool (toolbar shortcut F) that combines many drawing/editing functions depending on mouse button and modifier keys used: drawing lines, making rectangles, adjusting lines, adjusting line length, creating corners, drawing dart lines, deleting, one-way/two-way extension, moving or copying lines/points, transferring darts, snipping/connecting lines, shrinking darts, isometric lines (crossing or non-crossing), compasses, set square, offsetting points/lines, and drawing horizontal/vertical lines.

**Intersection of two parallel** — Grades a pattern border line so that it stays parallel with, and intersects, the adjacent side; commonly used for grading collars in custom fashion. Used by clicking the target point on the border.

**Keep Angle** — Adjusts a corner's grading point along one side so that the angle at the corner stays equal across all sizes. Operation: select the tool, use shift to switch between adjusting the X or Y direction, then click the point to adjust (B), the corner vertex (A), and the other side's grading point (C).

**Keep angle apex grading** — Adjusts corner grading so that angle apexes of different graded sizes remain equal in angle; typically used for adjusting the back rise and collar corner. Clicking on a corner shows the degree change.

**Keep angle edge xy grading (Adjust XY)** — A grading tool related to keeping angle edge grading consistent in the X/Y direction, analogous to Keep angle apex grading; further function/operation details were not included in this excerpt.

**Keep form manually** — An option in Move and Rotate Adjust that allows the user to freely adjust a line's shape by hand rather than having it adjusted automatically.

**Keep shape grade** — Keeps the curve shape of other sizes identical to the basic size's curve shape after grading. Operation: use the Select Pattern Point tool to drag-select the curve to be treated, then click the Keep Shape Grade icon.

**Language** — Selects the display language for the interface; the chosen language is matched by the text used for 'Print pattern info' and 'Print global info' under the file menu.

**Latest used 5 file** — Provides quick access to the 5 most recently used files; clicking a file name in the File menu list opens that file.

**Length unit** — Sets the unit of measurement (cm, mm, or inch) and the precision to use; when inch is selected, the user can also choose between fraction format and decimal format.

**Line grade** — Grades the whole pattern using a line grading table. Operation: open the line grade table dialog, add vertical, horizontal, or any-direction lines outside the pattern (and midpoints/base points as needed), select a line and input values into the q1/q2/q3 columns, then click Apply to grade the pattern according to those values. The associated dialog also lets you copy/paste grading values between lines, force q1=q2=q3 to be equal, apply values to all lines or only selected ones, auto-distribute values across sizes evenly ('average interval'), grade all patterns/size groups in the work view, show/hide grade lines, delete all grade lines, and adjust settings such as relative (distance to neighboring size) versus absolute (distance to base size) modes, and saving/applying table values to all or only selected lines/patterns.

**Line grade table** — A grading tool for defining vertical and horizontal grading lines plus a base point on a pattern, then assigning grading values to selected lines (individually or several at once per size) and clicking Grade to apply the grading automatically. Grading line start/end points must fall outside the pattern outline, extra points can be added between them, a '+' value means the pattern grows and a '-' value means it shrinks, and lines with the same grading value can be selected together.

**Line thickness** — Controls the display thickness of design lines, border lines, and assistant lines; moving the control left makes lines thinner and right makes them thicker, and selecting 'use smooth curve' renders lines smoothly instead of jagged (sawtooth).

**Line type** — Sets or changes the line type/style used for design and assistant lines. Operation: choose a line type from the pull-down list to draw with it, or select a type from the tool's pull-down list and click/box-select existing lines to change their type; also used to set the dash length (L) and gap distance (D) for dashed lines, and the radius and spacing for circle-style lines.

**Line width** — Sets the line width used by the inkjet plotter.

**Load pattern position** — Restores a previously saved pattern arrangement position when opening a file that had positions saved. Operation: open the file, click Edit - Load pattern position, select the desired saved position and confirm.

**Make Interlining** — Creates interlining pieces from a pattern. You can add an equal-value interlining strip along one or more selected border/slope lines by marqueeing the border and entering a value in the Interlining dialog, or add interlining to an entire pattern by selecting the tool and clicking the pattern (its border turns grey) and entering a value. Parameters control the interlining's distance from the selected line (inward with '+', outward with '-'), whether the new piece's seam allowance increases or decreases, whether the new piece keeps a seam allowance, whether the slope line is shown on the original pattern, the naming of the new interlining piece (appending 'interlining' to the name), and whether the new piece's grainline stays the same or rotates 90 degrees relative to the original.

**Make pattern** — Creates a new circular or rectangular pattern piece. Use Pattern > Make pattern, select the desired option and input appropriate values, then click OK to generate the new pattern.

**Make Sewing Order Manually / Change Sewing Line Order** — Select this tool, click a number on the keyboard (e.g. 6), then click a sewing line near one side to assign it that sewing order number; repeat with subsequent numbers to set order for other lines. For closed sewing lines, an arrow shows the needle position and running direction.

**Make Slot on Assistant Line** — Creates a sewing template slot along an assistant (helper) line. Operation: select the Sewing Template tool, click an assistant line or drag between its two endpoints (or box-select multiple assistant lines) to open the Sewing Template dialog, input the desired value, and click OK.

**Making Slot on Inner Line** — Creates a sewing template by cutting a slot along an inner line of a pattern piece (e.g., a pocket flap with seam allowance). Operation: select the Sewing Template tool, drag from one point to another to open the sewing template dialog, input the desired values and click OK to generate a cut line; right-clicking on the pattern opens the Create Sewing Template dialog for entering further parameters, typically used for standard (non-automatic) template sewing machines.

**Matching Point Tool** — Used to check whether the needle on the auto sewing machine matches the sewing template's start point (or end point). Press Shift to switch to the corresponding cursor, then click the proper place to set it; matching points are created automatically when making a regular or normal sewing template, and can be changed with this tool.

**Measure two point distance** — Measures the distance between two points, or from a point to a line, including horizontal and vertical distance, on either pattern lines or design lines. Click the two points to measure (e.g. to measure a waist length); this tool can also be reached by holding Shift while using Compare length.

**Measurement var** — Records and saves measurement variables; lets the user view measurement data for different sizes and modify measurement variable names via a dialogue box.

**Middle point** — Inputs a middle grading point at the center of a grade line.

**Mirror** — Mirrors (copies or moves) a design line or pattern across a symmetry axis. Click two points (on a line or in blank space) to define the axis, then select the object(s) to mirror and click right to finish. By default it copies (Shift switches to move); by default the axis snaps to horizontal, vertical, or 45 degrees, but right-clicking allows any direction. Shortcut key K.

**Modify** — A shortcut toolbar (shortcut key A) tool used to adjust curve shape, change the number of control points, convert between curve points and turn points, and modify the properties of drills, button holes, pleats, and darts via right-click. It supports adjusting a single control point by dragging or entering a value, adding or deleting control points, converting point types with Shift, smoothing lines with Ctrl, changing control point count with number keys, and adjusting multiple control points proportionally, in parallel, or via a marquee-selected square; right-clicking a drill, button hole, or pleat opens its property dialog for editing.

**Modify All Drills of Style** — Option that, when selected, applies the radius change to every drill operation in the style so they all share the same radius.

**Modify notch type** — Modifies the type of one or more notches. Depending on selection, it can modify notch type/depth/width on a specific notch, on all notches of a selected pattern, or on all patterns in the workarea/file; it allows changing notch type, depth, and height but not the notch command type (cut/draw) or notch angle.

**Modify Stitching Line** — Right-click on a pattern that has a stitching line to open its dialogue table, then modify the settings and click OK to apply the change.

**Modify Two Side Length Equal Cut Corner** — Used with the Add Seam tool while holding Shift to make the two sides of a cut corner equal in length. Depending on which of the three icons is selected and the order in which the front line and front side line are clicked, the system sets both segments equal to the first-clicked side's length, the second-clicked side's length, or applies a combined effect, standardizing the corner regardless of the original unequal distances.

**Motif Lib** — Saves custom-designed stitch types (motifs) for reuse. Using the intelligent pen tool to draw a repeating stitch shape, then selecting the Motif Lib tool and clicking the points of that shape, the system generates (or lets the user input) a file name and saves the motif into the GMotif folder of Richpeace CAD v9 Enterprise; saved motifs can later be selected via the "Use motif" option in the sewing template tool.

**Move** — Copies or moves a selected group of points or lines. Select the objects and click right, then click a reference point and drag to the target position and click; clicking right after choosing the reference point mirrors the selection horizontally or vertically. By default it copies (Shift switches to move); right-click constrains movement to horizontal/vertical direction; pressing Enter while moving/copying opens an Offset dialogue for precise placement. Shortcut key G.

**Move (copy)** — Accessed by holding Shift, marquee-selecting one or more lines, and right-clicking with the Intelligent Pen; moves or copies the selection, with Shift toggling between move and copy, and Ctrl allowing movement/copying in any free direction.

**Move and rotate** — Moves and rotates one group of lines to align with another group of lines, for example moving a back pattern's lines to match the front. It can be done by clicking two corresponding reference points (near the collar on the shoulder bias line for each piece) or by clicking four corresponding points, then selecting the lines to move/rotate and clicking right to finish; by default it copies, and Shift switches it to move only.

**Move and Rotate Adjust** — A shortcut toolbar (shortcut key N) tool used to adjust a line after it has been moved and rotated, typically to align front and back armholes, hems, darts, and collars for comparison. It can be applied to both pattern pieces and design lines, and includes selecting lines, adjusting control points (including shared/public points moved vertically), and finishing with a right-click to smooth the line.

**Move pattern** — Shortcut space. Moves a pattern piece from one location to another, or aligns two pattern pieces to overlap at a common point. Operation: click on the pattern with the tool and drag it to the desired location then click to place it; to overlap two patterns at a point, click the tool, click on a pattern, drag to another pattern, select the overlapping point, and click OK. Skill: holding space while any other tool is active temporarily switches the cursor to the move-pattern tool, allowing drag-and-click placement.

**Move pattern to design pos** — Moves a pattern that was previously repositioned back to its original design line position. Select the pattern, use Pattern > Move pattern to design pos, choose the first option, and click OK; can be applied to all patterns at once.

**Neg X** — Reverses the sign of a grading point's X-direction grading value, changing +X to -X or vice versa.

**Neg XY** — Reverses the sign of both the X and Y grading values of a selected grading point simultaneously.

**Neg Y** — Reverses the sign of a grading point's Y-direction grading value, changing +Y to -Y or vice versa.

**New** — Creates a new file (Ctrl+N). If there are unsaved changes in the work area, prompts the user to save the current file first, offering a Save As dialogue to choose a path and filename.

**Next Grading Point** — Selects the next grading point relative to the currently selected point, following the clockwise order of points around the piece contour.

**No Denomination, Default is precision** — Sets a default fraction denominator based on the chosen precision, so that a decimal value and its equivalent fraction (e.g. 10.3 and 103/16 at 1/16 precision) are treated as the same value.

**Non Cross isometry line** — Accessed by left-click-dragging a line with the Intelligent Pen (without crossing another line); creates an isometric (equal-distance) line from the dragged line.

**Non Grading Point on a Curve (Key 4)** — Digitizer mouse button function used to input a point on a curve that does not have its own grading value.

**Non-grading Point on One Line (Key A)** — Digitizer mouse button function used to input a point on a straight line that does not have its own grading value.

**Notch** — Adds notches to a pattern, including turning a corner into a notch, adjusting notch direction, grading notches, and modifying a notch's position, size, and properties. Notches can be added on a control point by clicking it; on a line by clicking or marqueeing it and setting options/value in the Edit Notch dialog; at equal spacing along one or more selected lines via a marqueed square and the Edit Notch dialog; at equal spacing between two points by dragging from one point to another and choosing Proportion or Divider notch with a quantity; and on turned corners by holding Shift and clicking the corner point (with a seam value), by marqueeing corners to add notches to multiple corners at once, or by marqueeing/clicking the middle or one side of a line to add notches to both sides or just one side automatically.

**Notch (Key 3)** — Digitizer mouse button function used to input a notch point on the pattern border.

**Notch Attr** — Field in the Pleat (and dart) dialog used to set the notch type, width, and depth associated with the pleat or dart.

**Notch type of outside border** — Selecting this option allows the same notch type to be used for the outside border whether plotting or cutting.

**Offset point/offset line** — Accessed by holding Shift, clicking a key point, and right-clicking with the Intelligent Pen (or simply pressing Enter for a quick offset point); creates an offset copy of a point or line, with right-click toggling whether the original point/line is kept.

**One way extend** — Accessed by marquee-selecting one or more lines then clicking on another (reserve) line and right-clicking it with the Intelligent Pen; extends the selected line(s) in a single direction to meet the target line.

**Only display one piece** — When enabled, shows and locks only one selected piece full-screen on the work area so that only that piece can be operated on, preventing accidental changes to other pieces. Selecting a different piece and clicking the icon again locks the new piece; clicking the icon up cancels the lock.

**Only group basic size** — When enabled, only the base size of each group is displayed; when disabled, all sizes are shown.

**Open** — Opens the formula editor for the currently selected grading point in the Rule Grade Table, allowing the grading formula to be edited; clicking Grade afterward applies grading using the current formula.

**Open AAMA/ASTM Format file** — Opens pattern files in the international AAMA/ASTM format. Accessed via File > Open AAMA/ASTM format file, then selecting the save path and double-clicking the file name to open it.

**Open TIIP format file** — Opens Japanese .dxf pattern files saved in the TIIP (Japan) format. Accessed via File > Open TIIP format file, selecting the save path and double-clicking the file name.

**Opened Assistant Line** — Tool for adding an internal open assistant line to a pattern: after the border line is read, it is automatically selected, and the user inputs one side, a middle point (marked as straight or curve), and the other side, finishing with the Close/Finish key.

**Outside border** — Sets the line type used for the outside border when plotting.

**Outside border notch use same type** — When selected, applies the same notch property for both plotting and cutting of the outside border.

**Overlap** — A plot mode used to print graded pieces overlapping one another on the same output.

**Paper size** — A setup option used to select the paper size from a pull-down list, or define a custom paper size by entering values manually.

**Parallel Design** — Creates parallel lines on a pattern or design line. The user clicks the reference lines, right-clicks to open the Parallel Design dialogue, inputs the desired distance value (D), and clicks OK to generate the parallel line at that offset.

**Parallel grading** — Creates parallel grading lines on a pattern piece, offsetting border/assistant lines by set distances so each size shape resembles the base size. Operation: select or box-select the line(s) needing parallel grading, right-click to open the Parallel Grade dialog, input the distance for each parallel line, and click OK. In the dialog, D.EQ makes the distance equal between different sizes; 'All columns same' makes every column use the same value; 'Relatively' offsets relative to the neighboring size while 'Absolute' offsets relative to the base size; positive/negative values offset in the direction shown by the arrow on the pattern (or the opposite direction); a value of 0 keeps that size identical to the base size; and non-selected lines simply extend the current shape.

**Parallel modify** — Parallel-modifies one or more lines. Operation: click or drag one or more points, then click a blank area to open the Offset dialog and input the adjustment value and click OK; dragging onto a key point skips the dialog; holding Shift while dragging constrains movement to horizontal, vertical, or 45-degree directions.

**Parallel Move** — Adjusts a line so it moves in parallel relative to the pattern. The user selects the line(s) to adjust, drags to set direction, and inputs a distance value (positive to lengthen, negative to shorten) in the Distance dialog to complete the parallel adjustment.

**Parallel quadrangle** — Creates a parallel quadrangle shape, typically used for making bags, toys, etc. The user clicks a blank area, moves and clicks again to open the dialogue, inputs values, and clicks OK to finish.

**Parrallel grading** — Grades a border line and pattern assistant line to remain parallel; typically used for grading lingerie patterns.

**Paste grading** — Pastes previously copied grading values (both X and Y direction) onto the currently selected grading point(s).

**Paste grading value** — Pastes previously copied grading values onto selected grade line(s) that do not yet have grading values assigned.

**Paste pattern** — Used together with Cut/Copy pattern to paste the pattern held on the clipboard into the currently opened file. Operation: open the file to paste into, then click Edit - Paste pattern.

**Paste X** — Pastes only the copied Dx (X-direction) grading value onto the selected grading point(s).

**Paste Y** — Pastes only the copied Dy (Y-direction) grading value onto the selected grading point(s).

**Pattern** — A plot option that plots only the finished pattern, without draft/design lines.

**Pattern assist curve** — Toggles whether pattern assist curves are displayed.

**Pattern flip** — Flips a pattern piece horizontally or vertically. Pressing Shift toggles between horizontal and vertical flip, and clicking directly on the pattern performs the flip (with a confirmation prompt if the pattern has distinct left/right sides). A marquee selection of multiple patterns followed by a right-click flips them all horizontally or vertically.

**Pattern info (P)** — Edits detailed information for the currently selected pattern, including name, comment, material, and copy/fold orientation (left/right). Shortcut: double-click on the pattern. Operation: select a pattern, click Pattern - Pattern info, enter information, and click Apply; can continue to other patterns without closing the dialog.

**Pattern jion** — Joins two separate pattern pieces into one, using either a straight two-point connection line (Method A) or a curve (Method B), toggled with Shift. Joining can be done by clicking blank space between the patterns, clicking corresponding points on each pattern, clicking the border lines of each pattern, or dragging pairs of points from each pattern; Shift also toggles whether the joining line is retained or discarded. An alternate operation using Ctrl plus clicking four points merges the patterns visually while keeping them as two separate pieces internally.

**Pattern listbox** — Clicking the up, down, left, or right button moves the pattern list box to the corresponding position on the interface.

**Pattern qty and capture** — Configures two settings for digitizing: 'Capture' sets the capture point so that a circle is centered on the captured point with a radius controlled by pixel/dimension size (recommended between 5-15), and 'Pattern qty' sets the number of patterns to digitize.

**Pattern rotate** — Rotates one or more pattern pieces. Right-clicking rotates the pattern 90 degrees (or aligns the grainline to horizontal/vertical if it isn't already); clicking a pivot point and moving the mouse rotates the pattern to horizontal/vertical at that point; holding Ctrl and clicking two points allows free rotation, while Ctrl plus right-click rotates by a specified degree; a marquee selection of multiple patterns followed by a right-click rotates them all 90 degrees. The grainline rotates together with the pattern.

**Pattern symmetry** — Creates a mirrored (symmetric) copy of half a pattern across an axis, in either a 'relevant' mode (editing one half automatically updates the mirrored half) or an 'irrelevant' mode (editing one half leaves the other unchanged). Press Shift to activate the tool, then select the symmetry axis (e.g., front center) or two points defining it; for relevant symmetry, the mirrored link can be removed later by reselecting the axis and pressing Delete. If the two sides aren't already symmetric, the larger-area side should be kept when choosing the axis.

**Pattern temp assist curve** — Toggles whether temporary pattern assist curves are displayed.

**Pattern toolbar** — Toggles whether the pattern toolbar is displayed.

**Patternlist box** — Toggles whether the pattern list box is displayed.

**Pic lib** — Used to create a craft picture from selected drawn lines (via File > Save to picture lib), then open and adjust that craft picture, and copy the bitmap picture out to other office applications (e.g. Word, Excel). Adjustment of the picture's dashed frame supports moving it, stretching it horizontally or vertically, rotating it via the corner handles, and proportionally scaling it (via Ctrl-drag or by entering values in the Scale dialog after marquee-selecting the design and right-clicking twice). When opened on a pattern, the picture becomes a groupware object that can be moved/rotated like other craft pictures, and holding Shift while confirming converts it into assistant lines instead of a locked group.

**Pick up assistant line tool** — Extracts an assistant line from a design line already inside a pattern. After the Forfex tool is used and right-clicked (turning the cursor into this tool), click the pattern so its design lines turn blue, then click or box-select the needed line(s) and click right; if converting a border/scissor line to an assistant line, click two points for a straight line or three points for a curve. Holding Shift and clicking right opens the Pattern Info dialogue.

**Play demo** — Plays a video demonstration of how a tool is operated. After selecting this icon, clicking on any other tool plays a demo of that tool's operation.

**Pleat** — Adds or modifies box or knife pleats on a pattern border, and can convert a pleat marked on a design/assistant line into a pleat element. Adding a whole pleat changes the actual pattern size, while adding a half pleat only marks the pleat sign without altering the pattern size. Supports clicking an existing pleat line and using the Pleat dialog to combine and adjust it, adding even pleats along one or more selected lines by entering width and quantity, modifying an existing box or knife pleat by clicking it (turns red) and right-clicking to open the Pleat dialog, and converting two dragged assistant lines into a pleat element (with notches added automatically), where the right-click position determines the pleat's direction and orientation.

**Plot** — Plots the garment pieces at real size (1:1). The user arranges all pieces to be plotted within the plot border on the working area, clicks Plot, chooses actual or scaled size, selects which sizes to include, sets up the plotter parameters, and then plots.

**Plot parameter** — An options panel for configuring plot output settings, including line width, point size, and spacing for dashed and dash-dotted lines.

**Plot scale** — A plot option that lets the user input a proportion between the plotted output and the real size, instead of plotting at 1:1.

**Point** — Adds a point on a line or in blank space, for use on design lines and patterns. Click near the desired location on a line, then enter a value in the 'Point position' dialog to set the exact position; points can also be placed by dragging from a reference point to the target location.

**Point clean up** — Automatically deletes superfluous (redundant) points from a pattern. Operation: click Edit - Point clean up.

**Point Grading** — Method for grading a pattern piece (such as sleeve and collar) by assigning grading values to individual points.

**Point size** — Controls the display size of points on design lines or patterns, and serves as the reference point size when measuring distances.

**Portrait/Landscape** — Setup options used to set the orientation (portrait or landscape) of the plotted output.

**Presserline** — Sets a presser line for one or all sewing lines, indicating the position the machine head moves to before starting the needle point on an auto-sewing template machine. The user sets parameters in the Presser Line Setting dialogue and applies them, can click a sewing line to view/modify its parameters in the Current Template panel, and can select "Display all presser lines" to show all presser lines as dashed lines.

**Preview** — Option in the Open dialogue that displays the last-saved content/thumbnail of the selected file, along with style info such as a comment (e.g. 'shirt').

**Previous Grading Point** — Selects the previous grading point relative to the currently selected point, following the clockwise order of points around the piece contour.

**Print measure table---Preview** — Shows a preview of the measurement/size table before printing.

**Print measure table---print** — Prints the measurement (size) table. Accessed via File menu > Print measure table > Print.

**Print pattern info** — Prints detailed pattern data such as pattern name, comments, material, and quantity. Accessed via File menu > Print pattern info, which opens a dialog with options: 'All pattern of style' (default, prints all patterns and their info one by one), an option to print only work-area patterns (place needed patterns in the work area first), and 'Preview' to see a preview before printing.

**Print style info** — Prints information for all patterns belonging to a style, including global data such as area and perimeter. Options in the associated dialog include printing all sizes or a selected size, all materials or a selected material, previewing the data list, and exporting all pattern info to Excel. Accessed via File > Print style, then configuring the setup accordingly.

**Printer setup** — Sets up the printer name, paper direction, and paper size for printing. Accessed via File menu > Printer setup, where you select the printer name, print direction, and paper size.

**Proportion adjust** — Drags one or more lines proportionally, with the cursor changing appearance when Shift is held. Operation: select the tool, click a point on a curve and drag (or drag a group of control points, or click and drag a key point), then click a blank area to open the Offset dialog, input the adjustment value and click OK; dragging to a key point skips the dialog; holding Shift constrains the adjustment to horizontal, vertical, or 45-degree directions.

**Proportion Grade** — Grades a pattern's border lines and inner lines by inputting horizontal and vertical margin values for the whole pattern, commonly used by bedding product companies. After selecting size/measurement editing, the user clicks the pattern, right-clicks to input margins for each size (using Non-AVE.SIZE for different margins per size, or AVE.SIZE with a nearest basic size margin for uniform grading), and can optionally grade only assistant lines, circles, string tables, buttonholes, and drills instead of the outline by choosing the outline grade option.

**Proportion notch / Equal divide notch** — Dialogue options for the locate type of a notch: Proportion adds a notch at a set proportion along a line defined by two or more points, while Equal notch divides the distance between two points into equal segments (like a divider) and adds notches at those points. A 'Change Ref_p' button lets you switch the reference point used for proportion-based placement.

**Protractor** — Measures angles on pattern and design lines in several modes: the horizontal/vertical angle of one line, the angle between two lines, the angle formed by three clicked points, or (holding Shift) the horizontal/vertical angle between two points. After selecting the line(s) or points and clicking right (or Shift-clicking), a Measure Angle dialogue displays the result.

**q1,q2,q3 all equal** — When enabled, entering a grading value in any one of the q1, q2, q3 line groups makes all three groups equal; when disabled, each can have a different value.

**Qty** — Sets how many groups of notches are opened: selecting 1 opens one group of notches, 2 opens two groups, and 3 opens three groups.

**Quilt** — Creates quilted stitching lines on a pattern. The Type option lets you choose Cross (stitching lines cross at a specified angle) or Single (parallel quilted stitching lines). For straight lines you can choose three-line, two-line, or single-line configurations, setting distances (A, B) between lines and the distance between line groups (C); for curve line type you set curve width and curve height. An option lets the line extend into the seam allowance or stop short of it.

**Quilted stitching** — Adds or modifies a quilted stitching line on a pattern. The pattern (or a region of it selected clockwise) is highlighted, then a reference line (border line or assistant line) is chosen by its start and end points; the Quilt dialog is used to pick a line type and enter values to apply the stitching. Different stitching lines can be applied to different regions of the same pattern by repeating the process on other selected areas.

**Radius** — Field in the Drill Attribute dialog that sets the radius of the drill circle.

**Read New Pattern (Key B)** — Digitizer mouse button function used to start reading a new pattern piece, clearing the Input Pattern dialogue for the next piece.

**Recognize Background** — A one-time calibration step where a photo of the empty grid background (without any pattern on it) is taken first; afterward, a normal paper and then the pattern are placed on the background and photographed for actual digitizing/testing.

**Rectangle** — A shortcut tool (toolbar shortcut S) used to draw a rectangular design line, or as an assistant rectangle within a pattern piece. Operation: click on a blank spot or key point and type length/width values (pressing Enter to confirm each), or drag the mouse and click again to open a Rectangle dialog to input exact values; if the start and end points coincide on a key point, pressing Enter creates an offset, otherwise a position dialog appears to input the point's data.

**Redef grainline** — Resets the grainline of a selected pattern back to its original status/position. Select the pattern, use Pattern > Redefine grainline, choose the first option, and click OK; can be applied to all patterns at once.

**Redo** — Reapplies an operation that was previously undone; each press restores one more step. Activated via the Redo icon or Ctrl+Y.

**Ref End point** — Before clicking Notch 1, Notch 2, or Notch 3, this sets the starting point using the selected line's start point, then sets the end point using the selected line's end point.

**Relative /absolute value** — Controls whether line grading values are shown/entered as relative or absolute values, functioning similarly to the same option for point grading.

**Relevant or irrelevant** — Controls whether crossing lines move together when adjusted with the modify tool: 'relevant' makes lines adjust together, 'irrelevant' makes them adjust independently. Applies to both design lines and assistant lines, with cross points relevant by default; shift toggles between the two modes, and selecting two crossing lines applies the setting.

**Resmooth curve** — Redraws/smooths a selected curve while keeping its original key points in place. Clicking the curve creates a new curve overlaid on the original (a straight line if there are no grading points, or passing through grading points if present); clicking control points on the original line attaches the new curve to them; right-clicking on blank space finalizes the new curve.

**Rhombus Dart** — Tool/menu item for inputting a rhombus-shaped dart: after reading the border line, the user selects Rhombus dart from the menu, reads the dart point, waist point and tip point (marking curves as needed), and presses the finish key; only one side is read due to symmetry.

**Rotate** — Rotates, or rotates and copies, a selected group of points or lines, for use on design lines and assistant lines. Select the objects and click right to finish selection, then click an axis point and a reference point and drag to the target position; by default it rotates and copies, and pressing Shift switches it to rotate-only (move).

**Rotate dart** — Creates a dart while keeping the original line length unchanged. The user clicks a line and two points to open the Rotate Dart dialogue, then inputs a width value and clicks OK; dialogue parameters include W (dart width), D (dart length), Mode (dart style), Overlap (dart direction), Drill Attr. (drill attribute and distance), and Notch Attr. (notch type, width, and depth).

**Rule Grade Table** — Grades a pattern using size measurements from the Size menu's Edit Size & Measurement table, or from manually entered values, including formulas (e.g. Bust/4) accessible via a calculator by right-clicking the X or Y field. Operation: click or box-select a grading point, input a value (or formula), and click Grade; if the measurement table is later changed, affected points regrade automatically.

**Ruler bar** — Toggles whether the ruler bar is displayed.

**Safety restore** — Recovers a file that was not saved due to a power outage or similar interruption. Open the software, click File menu > Safety restore, select the appropriate recovered file, and click OK. Requires the 'Use Auto design' option to be enabled beforehand in Option > System setup.

**Save** — Saves the size table that has been created or edited.

**Save As** — Saves the current file (Ctrl+S). If saving for the first time, opens a Save As dialogue to choose a path and enter a filename; subsequent saves overwrite the original file. The icon appears greyed out/inactive if the file has not changed.

**Save each step** — When enabled, saves the file after each individual operation step is performed.

**Save interval** — Sets the time interval between automatic saves.

**Save patterns position** — Records the current position of patterns arranged in the work area so it can be restored later. Operation: arrange patterns in the work area, click Edit - Record pattern position in workarea, then save the position under a chosen name.

**Save to lib** — Saves a selected design line to a pattern library for later reuse. Used together with the 'pic lib' tool: marquee-select the design line, right-click, then use File menu > Save to lib to choose a save path and name for the saved item.

**Scale** — Zooms a draft line or pattern in or out to an appointed size or proportion. For a draft line, the user selects the line (or two points on it) and inputs a new length or proportion in the Scale dialog; for a pattern, the user selects border/assistant lines or control points and inputs a new length or proportion, choosing whether to scale just the selected curve/points, the whole workarea pattern, or all patterns in the style. Scaling a draft line does not affect the pattern's size, and scaling a pattern does not affect the draft line's size.

**Screen size** — Enter the actual physical screen size so that patterns can be displayed at true 1:1 scale.

**Seam val** — Adds a seam allowance value to a pattern; when the seam option is selected, the seam value appears on the pattern.

**Search File** — Button that opens a Search File dialogue, allowing the user to search for a file by entering keywords and clicking Start; matching files appear in a list and can be opened directly.

**Select line** — Selects a grade line (horizontal, vertical, or any-direction) so that a grading value can be entered for it in the Line Grade table and applied.

**Select pattern control point** — Selects whole patterns, border points of a pattern, or assistant line points, and allows modifying a point's parameters. Supports selecting single or multiple grading points and non-grading points (via click, marquee, or Ctrl+click), toggling selection with Ctrl, canceling selection with Esc or a click on blank space, and selecting a range between two points by dragging from one to another. Where assistant lines and border lines overlap, plain clicks select the border point, marquee selection selects both, and Shift+marquee selects the assistant line grading point; double-clicking a point opens the Control point attribute dialog for editing, and this tool is also used to select notches for grading.

**Select rotate Group** — An option used in Move and Rotate Adjust where, if the front and back rise are on the same side, selecting this item and a border causes the associated lines to rotate together automatically.

**Separate** — A plot mode used to print graded pieces separately by size; a size-selection panel lets the user choose which sizes (shown in blue) are output, with all sizes selected by default.

**Set assist curve output type** — Sets the output type of an assist curve as whole knife or half knife. After selecting the Set curve color and type tool and then this tool, clicking on a line marks one side of the assist line with a whole-knife or half-knife cut sign depending on the setting chosen.

**Set curve color and type** — A selection tool that must be activated before using the Set curve shape and Set assist curve output type sub-tools, allowing the user to then click those sub-tools and apply changes to a selected line.

**Set curve colour and type** — Modifies the color, line type, and output type of design lines and assistant lines — for example setting a solid line's thickness, switching between solid and dashed (or other styles such as a 'great wall' dashed pattern), and setting whether an inside line is for plotting, cutting, or half-blade cutting. Select the desired color/line type/output settings from the shortcut toolbar options, then click or box-select the line(s) to apply them to.

**Set curve shape** — Changes the line type by setting its width and height. After selecting the Set curve color and type tool and then this tool, the user inputs a width, presses enter, inputs a height, and clicks on the line to apply the change.

**Set square** — Creates a line parallel or perpendicular to an existing line, extending in any direction. Operation: click both ends (sides) of the reference line with the tool, then click another point and drag to make the new line either parallel or perpendicular to the selected line.

**setting** — Configures whether each pattern element (such as notches or drill holes) should be graded or not; clicking the button and selecting an element in the dialog marks it to be graded.

**Setup** — Opens the Plot dialogue where the user selects the current plotter, sets paper size, preserve border, work data path, and other plotting parameters.

**Setup Menu** — Configures the digitizer menu area the first time it is used or after it is moved. Operation: place the menu on the effective area, click Setup Menu, confirm with Yes, then click the menu's left-upper corner, left-bottom corner, and right-bottom corner to register its position.

**Sew line** — Adds and modifies sew (seam allowance) lines on a pattern's border. Supports adding a fixed-length sew line by clicking a border line and entering length/distance values in the Sew line dialog, applying a sew line to one or more selected lines at once, creating a sew line of unequal width between two chosen points along a line (by dragging from a first point to a second point and entering distance values), and deleting an existing sew line using the eraser by selecting a blank line type.

**Sewing Template** — A multi-function tool for preparing sewing templates: it can cut slots on inner (assistant) lines, modify template parameters, manually set or change the sewing order/line sequence, reverse a sewing line's direction, check sewing order numbers, and create regular sewing templates for either normal sewing machines or Richpeace automatic sewing machines, including setting temporary stop and start points. Pressing Shift cycles the cursor between slot-making mode, temporary-stop mode, and start-place mode.

**Sewing Template (modify parameter)** — Select the sewing template tool, move the cursor to a slot (blue line), and right-click to open the Sewing Template dialogue where slot parameters can be modified.

**Sewing template—Cut** — Dialogue for setting cutting template parameters, including engraving start/end parameters (similar to the Laser template dialogue), cut step (input step, width smaller than blade width), and cut speed (Speed0 fastest to Speed3 lowest, selected according to material); cut step and speed are only available for auto-sewing machines.

**Sewing template—Laser** — Dialogue for setting laser sewing template parameters, including engraving start/end parameters (similar to the Sewing template—Sewing dialogue), laser step (input step number, no more than 1mm), and laser speed (Speed0 fastest to Speed3 lowest, selected according to material); laser step and speed are only available for auto-sewing machines.

**Sewing template—Pen** — Dialogue for setting pen (drawing) template parameters, including engraving start/end parameters (similar to the Laser template dialogue), pen step (user-input step value), and pen speed (Speed0 fastest to Speed3 lowest, selected according to material); pen step and speed are only available for auto-sewing machines.

**Sewing Template—Sewing Dialogue: Engraving Parameter** — When engraving is enabled, the entered template width determines that all files have a slot; otherwise no slot is produced.

**Sewing Template—Sewing Dialogue: Extend to Length** — Allows specifying an extension length for the template slot; input 0 if no extension is needed, or a value to meet requirements when importing files not created in Richpeace.

**Sewing Template—Sewing Dialogue: Extend to Seam** — Automatically extends the template slot to the seam.

**Sewing Template—Sewing Dialogue: Repeat Count** — Select 'have repeat' and input a stitch count to set repeated stitching for use with a Richpeace auto-sewing machine; different repeat counts and stitch counts can be set for the start and end parameters. For start repeats, if the repeat count is even the needle starts from inside, if odd it starts from the start point; for end repeats, one needle length is shortened at the end to avoid thread showing after the line is cut.

**Sewing Template—Sewing Dialogue: Round Corner** — When selected, both sides of the template slot have rounded corners; otherwise they are right-angled.

**Sewing Template—Sewing Dialogue: Start Blank Length / End Blank Length** — Defines the distance from the start point of the sewing line to the head of the template slot, and from the end point of the sewing line to the end of the template slot; corresponds to the sewing machine's press foot length.

**Sewing Template—Sewing Dialogue: Template Width** — Sets the width of the template slot.

**Sewing Template—Sewing Dialogue: Type** — Sets the template output type; the system offers four kinds: Sewing (default), Laser, Cut, and Pen. If only making a plastic sewing template (not sewing), any of these can be selected to create the slot.

**Sewing Template—Sewing Dialogue: Use Stitch Length (Auto Sewing Parameter)** — Sets the stitch length in advance for use with an auto-sewing machine, ranging from 0.1 to 2.55 cm; multiple values can be entered to alternate stitch lengths (e.g. 0.25, 0.4 repeating) during sewing.

**Show or hide grade line** — Toggles the visibility of grade lines on the pattern - selecting it shows the lines, deselecting hides them.

**Show or hide shadow** — Toggles the visibility of a pattern's shadow, showing or hiding it. Accessed via Pattern menu > Show or hide shadow.

**Show pattern info at grain line** — When selected, displays the pattern information and style information text alongside the grainline on the pattern.

**Show/Hide assistant line** — Toggles the visibility of assistant lines on the pattern, shown or hidden by pressing Ctrl+U.

**Show/Hide design line** — Toggles the visibility of design (draft) lines on the pattern; clicking the icon down shows the design lines and clicking it up hides them.

**Shrink** — Applies shrinkage to a whole pattern based on material properties, or to a selected line/border for partial shrinkage. For whole-pattern shrink, select the tool, click the pattern, choose the material and input weft/warp shrink values in the Shrink dialog; shrink and scale values are linked and calculated automatically from each other. For partial shrink, select the border or assistant line, right-click, and input the shrink value in the Partial Shrink dialog.

**Shrink Dart** — Shrinks a dart by selecting the border line and dart line to open the Shrink Dart dialog, entering a width value, confirming the dart direction with a mouse click on the left or right, and then adjusting the dart (left-click) until the side seam is smooth, finishing with a right click.

**Single compasses** — Accessed by pressing on a key point and dragging with the Intelligent Pen until reaching another line; functions like a compass to mark a point at a fixed distance where the drag meets the target line.

**Size** — Dialog used when different sizes need different quantities of drills: checking the option for a size adds the drill to that size, leaving it unchecked means the drill is not added for that size.

**Size Align** — Aligns grading values of points or lines horizontally or vertically to a reference point/line, or restores the original alignment. Clicking a point aligns grading values to it; selecting a line aligns to the line connecting its two points; pressing X or Y before clicking forces horizontal or vertical alignment respectively; right-clicking on the pattern restores the original alignment.

**Size to pattern** — Displays nested pattern sizes separately (typically used for plotting), showing patterns from smallest to largest size or a chosen subset of sizes. Operation: click the nested pattern, then Edit - Size to pattern, and select All size or specific sizes.

**Sleeve crown and armhole notch** — Adds notches on the armhole and sleeve crown simultaneously: the front armhole and front sleeve crown each receive a single notch, while the back armhole and back sleeve crown each receive a double notch. Used by clicking near the relevant points on front armhole, front sleeve crown, back armhole and back sleeve crown in turn, then entering values (such as A.H.L, S.C.L, S.G, F.A.H.D, F.S.C.G, B.A.H.D, B.S.C.G, and 'Start from another endpoint') in the resulting dialogue table to control notch spacing and dispersion across graded sizes.

**Snip (connect) line** — Accessed by marquee-selecting a line with the right mouse button using the Intelligent Pen; cuts (snips) or connects the line.

**Snip curve** — Cuts a line at a specified point, turning it into two separate lines, or conversely connects multiple lines into one; also supports group-cutting several lines against a reference line. Shift toggles between snip/connect mode and group cut mode; clicking a key point (equal point, cross point, existing point) snips directly without a dialog, otherwise a 'point position' dialog lets you input the exact cut location.

**Solid line to dashed** — Converts a solid line into a dashed line by clicking or marquee-selecting the line to modify; affects wave lines, turn lines, and great wall lines. Also allows setting line size: select a line type, then type in length and width values (length first, then Enter, then width, then Enter) before clicking or marquee-selecting the line to apply the change.

**Split (drill, buttonhole)** — Splits a related drill hole or buttonhole group so that each buttonhole or drill hole can be graded separately, rather than all together. Operated by clicking the buttonhole or drill.

**Status bar** — Toggles whether the status bar is displayed on screen.

**Stitch Param** — Used to set sewing speed at points and stitch compensation. The user can click a corner point to set its speed or set speeds automatically for all corner points on the pattern, use the Adjust/Compensation button to configure Adjust, Length Compensation, Angle Compensation, or Offset for selected points, and select "Display stitch para" to show speed and compensation values near each point.

**Strip Info** — Field in the Drill Attribute dialog that sets a strip number for the drill; when selected, the strip is applied automatically when a marker is made.

**Style image** — Toggles whether the style image panel is displayed.

**Style info (S)** — Imports and stores style information for all patterns in the same file, such as style name, comment, customer, order, picture path, and material; this info can appear on the grainline and be exported with the pattern to the marker system. Operation: click Pattern - Style info, fill in the Style information dialog, set values, and confirm.

**Symmetry Adjust** — A shortcut toolbar (shortcut key M) tool used to adjust a line after a symmetry operation, commonly used for adjusting collars, by clicking or marquee-selecting the start and end points of the symmetry axis.

**Symmetry on 1** — Works the same way as Symmetry on 2, but applied with respect to border 1 instead of border 2.

**Symmetry on 2** — A cut-corner type often used for hemlines: the seam is tucked up according to border 2, and then the seam corner is modified according to seams 1 and 3.

**System setup** — Opens the System Setup dialogue, which contains eight option cards for configuring different system parameters; after changing settings on a card, the Apply button must be clicked.

**Tagent line of ARC** — Creates a tangent line from a point to a circle, or between two circles, by clicking the point/circle and then the other circle. Can be used on design lines and patterns.

**Temporary Stop Place** — A technique for finishing a pattern in two processes: after completing one part, open the sewing template, place another part's pattern, then close (cover) the template so the machine continues sewing. The template being repositioned should be easy to move while the underlying template stays closed.

**Text** — Adds, moves, modifies, or deletes text on a design line or pattern. Text can be entered via a Text dialog (set text content, angle, height, and font/color) or by dragging to set the angle relative to a line direction; existing text can be re-selected to edit or delete characters, and its placement direction can be adjusted by dragging. Text can also be set to appear differently (different wording) on different graded sizes using the Differ option and the size checkboxes, and text position can be graded using the pattern control point selection tool together with the grading table.

**Theme** — Lets the user select a previously saved interface theme; themes control which tools/buttons are shown, and multiple themes can be saved or deleted via a right-click menu in the work area.

**Toolbar** — Toggles whether the main toolbar is displayed.

**Transfer dart** — Transfers a dart within a pattern, whether the darts share the same circle center or not. It can transfer part or all of a dart, divide it equally among multiple new darts, and the new dart point can either stay at its original location or move, depending on whether a left or right click is used to select the combining side. Suitable for design lines.

**Trapezia** — Creates a trapezoid shape, typically used for making bags, toys, etc. The user clicks a blank area, moves and clicks again to open the dialogue, inputs values, and clicks OK to finish.

**Two point proportion grade** — Grades one pair of points proportionally based on the length proportion between another pair of points, or grades a point relative to a line based on another point's relation to that line. Operated by pressing Shift to switch cursor mode, then clicking the reference two points (or point and line) followed by the target two points (or point and line).

**Two way extend** — Accessed similarly to one-way extend but by clicking two other lines with the Intelligent Pen; extends the selected line(s) in both directions to meet the two target lines.

**UI Setup** — A settings panel for configuring interface options including the pattern list box position, screen size, display language, line thickness, and interface theme.

**Undo** — Cancels the previous command in sequence; each press undoes one more step. Activated via the Undo icon, Ctrl+Z, or right-click menu. The icon appears gray when there is nothing left to undo.

**Undo (Key C)** — Digitizer mouse button function used to undo the previous input action.

**Unit file** — Combines multiple named files together into one. Open a base file, then use File > Unit file to select and combine another file, provided the combined file is the same size as the basic size.

**Use Auto save** — When selected, enables the automatic saving feature.

**Use Motif** — Loads a stitch pattern from the Motif library into a template slot; the needle point (shown in red) marks one repeat's length and height.

**V Dart** — Adds or modifies a V-shaped dart on a pattern border, and can convert a design/assistant line into a dart element. If a dart line already exists, click it to open the V Dart dialog, enter values, confirm, then adjust the dart bottom. If no dart line exists, click the border line to set the dart placement, drag and click to set direction, then enter values in the dialog. An existing V dart can be modified by clicking it (line turns red) and right-clicking to reopen the dialog. Two assistant lines (dart bottom points and dart tip) can be converted directly into a dart element, with notches and drill holes added automatically.

**Vertical line** — Inputs a grade line in the vertical direction on a pattern, using the same operation as inputting a horizontal line.

**Vertical to 1, 2 sewing lines** — Draws perpendicular lines from the corner formed by borders 1 and 2 to the seam, then cuts the corner along the direction of the line connecting the resulting intersection points.

**View exact values a compare length dialogue when use inch fraction format** — When selected, the compare-length dialogue shows both decimal and fraction formats together; when not selected, only the fraction format is shown.

**View grading point** — Toggle (Ctrl+F) that shows grading points on the pattern when selected; otherwise they are hidden.

**View non grading point** — Toggle (Ctrl+K) that shows non-grading points on the pattern when selected; otherwise they are hidden.

**View Pattern** — Toggles the visibility of the finished pattern; clicking the icon down shows the pattern and clicking it up hides it.

**View same material pattern** — Brings pattern pieces onto the work area based on a chosen pattern name or material, to make checking pieces easier. Offers a "match whole word only" option to restrict matches to the exact pattern name, and a "show pattern base material" option to bring in pieces by material name, material copies, or pieces with no material assigned.

**View seam line** — Toggle (F7) that shows the seam line on the pattern when selected; otherwise it is hidden.

**W1, W2, D1, D2** — Parameters in the Fastigiate Dart dialog: W1 is the dart bottom width, W2 is the dart waist width, D1 is the length from the dart waist width to the dart bottom width, and D2 is the total length. If no fastigiate or rhombus dart is added on the assigned line, D1 and D2 become active/editable.

**Width 1** — Field in the Pleat dialog used when every size has an equal pleat value; selecting it lets you input the pleat value once, and Width 2 and pleat length are treated the same way.

**Work Data Path** — Specifies the data path of the plotcenter connected to the current plotter, used so that a networked computer without a direct plotter connection can send plot jobs to the computer that has the plotter attached.

**X Equal to 0** — Sets all X-direction grading values of a selected grading point to zero, meaning no grading occurs in the X direction for that point.

**X Equal Y** — Applies equal grading increments in both the X and Y directions simultaneously to the selected grading point(s).

**X non equal grading** — Allows entry of different (non-uniform) grading values per size in the X direction for a selected grading point, then applies them by clicking this icon.

**X、Y non equal** — Applies grading using values entered in the grade table that can be either equal or different (non-uniform) for both X and Y directions at once.

**Y Equal to 0** — Sets all Y-direction grading values of a selected grading point to zero, meaning no grading occurs in the Y direction for that point, operated the same way as X Equal to 0.

**Y non equal grading** — Allows entry of different (non-uniform) grading values per size in the Y direction for a selected grading point, operated the same way as X non equal grading.

**Zipper window** — Adds a zipper opening to a bag, glove, or other style, available for both design lines and patterns. The user clicks on a line or point to open the zipper window dialogue, inputs values, and clicks OK; the blade shown on the pattern indicates the cutting line.

**Zoom in** — Shortcut space. Zooms into or fits the work area objects to full screen. Operation: drag a rectangle around the area to be zoomed and click to zoom in; right-click in the work area for full screen view. Skill: holding space while using any other tool temporarily switches to the zoom tool, with the mouse wheel scrolling forward to zoom in and backward to zoom out, centered on the cursor location.
